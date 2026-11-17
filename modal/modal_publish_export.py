"""Publish a model built by 02_evaluate.ipynb with KEEP_EXPORT=1: its merged weights, the adapter it was built from and a
model card, to a Hugging Face model repo, which is then made public.

  modal run modal/modal_publish_export.py --repo skamalj/signpost-jev-4b --card card.md \
      --export sd-4b-v2/exports/jev3 \
      --adapter sd-4b-v2/checkpoints/signpost-d-Qwen3.5-4B-jev-fromv2/lr5e-05-r16-ep1-seed42/adapter

Paths are on the Modal volume `jepa-runs`. Runs on a CPU container with the `huggingface` secret. The export's base
README is replaced by the card, its `.cache` is left out, and merged.json names the adapter by its folder in the repo.
"""
from pathlib import Path

import modal

app = modal.App("signpost-publish-export")
volume = modal.Volume.from_name("jepa-runs")
image = modal.Image.debian_slim(python_version="3.12").pip_install("huggingface_hub>=1.5,<2.0")


@app.function(image=image, volumes={"/runs": volume}, secrets=[modal.Secret.from_name("huggingface")], timeout=3600)
def publish(repo: str, card: str, export: str, adapter: str):
    import json
    import os
    import tempfile

    from huggingface_hub import HfApi

    api = HfApi(token=os.environ["HF_TOKEN"])
    api.create_repo(repo, private=True, exist_ok=True)
    export_dir = Path("/runs") / export
    assert (export_dir / "config.json").exists() and (export_dir / "model.safetensors").exists(), export_dir
    api.upload_folder(folder_path=str(export_dir), repo_id=repo, ignore_patterns=[".cache/*", "README.md", "merged.json"],
                      commit_message="Merged fp16 weights")
    api.upload_folder(folder_path=str(Path("/runs") / adapter), path_in_repo="adapter", repo_id=repo,
                      commit_message="The LoRA adapter the weights were merged from")
    tmp = Path(tempfile.mkdtemp())
    merged = json.load(open(export_dir / "merged.json"))
    merged["adapters"] = ["adapter"]
    (tmp / "merged.json").write_text(json.dumps(merged, indent=1), encoding="utf-8")
    (tmp / "README.md").write_text(card, encoding="utf-8")
    for name in ("merged.json", "README.md"):
        api.upload_file(path_or_fileobj=str(tmp / name), path_in_repo=name, repo_id=repo, commit_message=name)
    api.update_repo_settings(repo, private=False)
    info = api.model_info(repo)
    print(f"{repo}: public={not info.private}, {len(info.siblings)} files:", sorted(s.rfilename for s in info.siblings),
          flush=True)


@app.local_entrypoint()
def main(repo: str, card: str, export: str, adapter: str):
    publish.remote(repo, Path(card).read_text(encoding="utf-8"), export, adapter)
