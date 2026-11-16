"""Back up runs from the Modal volume to a private Hugging Face repo: adapters, results and vLLM evaluations.

  modal run modal/modal_upload_checkpoints.py --repo skamalj/signpost-d-9b-checkpoints \
      --runs "9b-r16-lr1e-4-seed42=sd-9b,9b-r32-lr5e-5-seed42=sd-9b-r32"

Each `name=run` uploads /runs/<run>/checkpoints to <name>/ in the repo. Runs on a CPU container with the
`huggingface` secret; the token stays in Modal. Resume files (*.pt) are left out, and merged full-model exports
(outside checkpoints/) are not uploaded: the adapters rebuild them.
"""
import modal

app = modal.App("signpost-d-upload-checkpoints")
volume = modal.Volume.from_name("jepa-runs")
image = modal.Image.debian_slim(python_version="3.12").pip_install("huggingface_hub>=1.5,<2.0")


@app.function(image=image, volumes={"/runs": volume}, secrets=[modal.Secret.from_name("huggingface")], timeout=3600)
def upload(repo: str, runs: dict):
    import os
    from pathlib import Path

    from huggingface_hub import HfApi

    api = HfApi(token=os.environ["HF_TOKEN"])
    api.create_repo(repo, private=True, exist_ok=True)
    for name, run in runs.items():
        folder = f"/runs/{run}/checkpoints"
        files = [p for p in Path(folder).rglob("*") if p.is_file() and p.suffix not in (".pt", ".tmp")]
        print(f"{name}: {len(files)} files, {sum(p.stat().st_size for p in files) / 1e9:.2f} GB from {folder}", flush=True)
        api.upload_folder(folder_path=folder, path_in_repo=name, repo_id=repo, ignore_patterns=["*.pt", "*.tmp"],
                          commit_message=f"{name}: adapters, results, vLLM evaluation")
    info = api.model_info(repo)
    print(f"uploaded to {repo} (private={info.private}): {len(info.siblings)} files", flush=True)


@app.local_entrypoint()
def main(repo: str, runs: str):
    upload.remote(repo, dict(pair.split("=", 1) for pair in runs.split(",") if pair))
