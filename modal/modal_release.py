"""Release a published Signpost-D model repo: its card as README, merged.json with repo-relative adapter names, the repo
made public, and (optionally) the Typed Decisions submission posted.

  modal run modal/modal_release.py --repo skamalj/signpost-d-9b --card card.md [--post submission_post.md]

`02_evaluate.ipynb` with PUBLISH=1 uploads the model privately first; this is the second step, after the card and the
post are approved. The post's first line is "**Title:** <title>"; the rest is its body. Runs on a CPU container with
the `huggingface` secret; the card and post are read here and sent as text.
"""
import json
from pathlib import Path

import modal

BENCH = "LocalLLaMA/typed-decisions"

app = modal.App("signpost-d-release")
image = modal.Image.debian_slim(python_version="3.12").pip_install("huggingface_hub>=1.5,<2.0")


@app.function(image=image, secrets=[modal.Secret.from_name("huggingface")], timeout=1200)
def release(repo: str, card: str, post: str):
    import os
    import re
    import tempfile

    from huggingface_hub import HfApi, hf_hub_download

    api = HfApi(token=os.environ["HF_TOKEN"])
    files = [f.rfilename for f in api.model_info(repo).siblings]
    assert "typed_decisions_test_predictions.json" in files and "config.json" in files, files

    tmp = Path(tempfile.mkdtemp())
    (tmp / "README.md").write_text(card, encoding="utf-8")
    api.upload_file(path_or_fileobj=str(tmp / "README.md"), path_in_repo="README.md", repo_id=repo,
                    commit_message="Model card")
    print("README.md replaced with the model card", flush=True)

    if "merged.json" in files:                     # adapters by their folder in the repo, not by volume paths
        merged = json.load(open(hf_hub_download(repo, "merged.json")))
        merged["adapters"] = [f"adapters/{m.group(0)}" if (m := re.search(r"lr[^/]+-seed[0-9]+", a)) else a
                              for a in merged["adapters"]]
        (tmp / "merged.json").write_text(json.dumps(merged, indent=1), encoding="utf-8")
        api.upload_file(path_or_fileobj=str(tmp / "merged.json"), path_in_repo="merged.json", repo_id=repo,
                        commit_message="merged.json: adapters by their folder in this repo")

    api.update_repo_settings(repo, private=False)
    print("public:", not api.model_info(repo).private, flush=True)

    if not post:
        return
    title, body = post.split("\n", 1)
    title = title.replace("**Title:**", "").strip()
    if any(d.title == title for d in api.get_repo_discussions(BENCH, repo_type="dataset")):
        print("submission already posted", flush=True)
        return
    d = api.create_discussion(BENCH, title=title, description=body.strip(), repo_type="dataset")
    print(f"submission posted: https://huggingface.co/datasets/{BENCH}/discussions/{d.num}", flush=True)


@app.local_entrypoint()
def main(repo: str, card: str, post: str = ""):
    release.remote(repo, Path(card).read_text(encoding="utf-8"), Path(post).read_text(encoding="utf-8") if post else "")
