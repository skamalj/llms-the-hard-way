"""Run one of this repo's notebooks headless on a Modal GPU.

The local notebook file is sent to Modal and runs with papermill in its own folder on the Modal volume `jepa-runs`
(/runs/<name>), so its checkpoints and the output notebook live on the volume, and a rerun with the same name resumes
from them. The volume is committed every 10 minutes and at the end. Settings reach the notebook as environment
variables. The `huggingface` secret (HF_TOKEN) is always attached: `modal secret create huggingface HF_TOKEN=<token>`.

  # Signpost-D on Qwen3.5-9B, one seed; then its evaluation in the same run folder
  MODAL_GPU=L40S modal run --detach modal/modal_run.py --notebook 01_train.ipynb --name sd-9b \
      --settings "BASE_MODEL=Qwen/Qwen3.5-9B;SEEDS=42;GPUS=1"
  MODAL_GPU=L40S modal run --detach modal/modal_run.py --notebook 02_evaluate.ipynb --name sd-9b \
      --settings "BASE_MODEL=Qwen/Qwen3.5-9B;SEEDS=42"
  modal volume get jepa-runs sd-9b/02_evaluate_out.ipynb .

GPU: MODAL_GPU, one type or a comma list tried in order (default L4,A10,L40S).
If the container is lost or preempted, Modal retries it (twice); an error inside the notebook is not retried.
"""
import os
import subprocess
import threading

import modal

GPU = os.environ.get("MODAL_GPU", "L4,A10,L40S")
GPU = GPU.split(",") if "," in GPU else GPU          # a list: Modal takes the first type that is free
# Fixed, not read from the environment: the container re-imports this file without the local environment, and its
# function definition (secrets included) must match the one that was sent.
SECRETS = ["huggingface"]

image = (modal.Image.debian_slim(python_version="3.12")
         .apt_install("git")
         .pip_install("torch", "transformers>=4.48", "peft", "datasets", "huggingface_hub>=1.5,<2.0", "pandas",
                      "pyarrow", "psutil", "papermill", "ipykernel", "einops", "matplotlib", "tqdm",
                      "httpx", "accelerate"))   # httpx: what transformers 5.17 (pinned without deps) needs
volume = modal.Volume.from_name("jepa-runs", create_if_missing=True)
app = modal.App("jepa-notebooks")


@app.function(image=image, gpu=GPU, volumes={"/runs": volume},
              secrets=[modal.Secret.from_name(s) for s in SECRETS], timeout=12 * 60 * 60,
              retries=modal.Retries(max_retries=2, initial_delay=10.0))
def run(name: str, notebook: str, source: str, settings: dict):
    volume.reload()                         # see what other runs have committed (e.g. caches)
    work = f"/runs/{name}"
    os.makedirs(work, exist_ok=True)
    path = os.path.join(work, notebook)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(source)
    out = path.replace(".ipynb", "_out.ipynb")
    os.environ.update(settings)             # the kernel inherits them
    stop = threading.Event()

    def commit_every(seconds=600):          # checkpoints reach the volume during the run
        while not stop.wait(seconds):
            volume.commit()

    threading.Thread(target=commit_every, daemon=True).start()
    try:
        result = subprocess.run(["papermill", path, out, "-k", "python3", "--log-output", "--cwd", work], cwd=work)
        if result.returncode != 0:
            # A failure inside the notebook is not retried (that would only repeat it); the output notebook
            # on the volume shows the error. Modal's retries still cover a lost or preempted container.
            print(f"NOTEBOOK FAILED (exit {result.returncode}): see {out}")
            return
    finally:
        stop.set()
        volume.commit()
    print(f"done: {out}")


@app.local_entrypoint()
def main(notebook: str = "08_jepa_lora_predictor.ipynb", name: str = "", settings: str = ""):
    with open(notebook, encoding="utf-8") as fh:
        source = fh.read()
    pairs = dict(kv.split("=", 1) for kv in settings.split(";") if kv)
    run.remote(name or os.path.splitext(os.path.basename(notebook))[0], os.path.basename(notebook),
               source, pairs)
