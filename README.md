# Signpost-D

Decision models, in a 4B and a 9B. Given a piece of state (a JSON record or text) and typed questions about it, the
model answers each question with a probability for every option: true/false statements, choices between named
options, and levels on ordered scales. It doesn't generate text: each question is one forward pass, read from the
answer tokens, and it serves unchanged through vLLM's `/v1/systemone`.

| Model | Base | Typed Decisions zero-shot table |
|---|---|---|
| [skamalj/signpost-d-9b](https://huggingface.co/skamalj/signpost-d-9b) | Qwen3.5-9B | #16, accuracy 0.7345 |
| [skamalj/signpost-d-4b](https://huggingface.co/skamalj/signpost-d-4b) | Qwen3.5-4B | #24, accuracy 0.712 |

[skamalj/signpost-jev-4b](https://huggingface.co/skamalj/signpost-jev-4b) is a sibling tuned for JevBench instead: accuracy 0.827 on JevBench's 231 public items (our own run; submitted to the board).

## Result

[LocalLLaMA/typed-decisions](https://huggingface.co/datasets/LocalLLaMA/typed-decisions), `test` split (400 cases,
2,000 decisions), general mode, scored with the benchmark's own scorer:

| Model | Accuracy | KL from gold | Brier | ECE | Latency per case |
|---|---|---|---|---|---|
| Signpost-D-9B | 0.7345 [0.713, 0.756] | 0.159 | 0.082 | 0.101 | 214 ms (one L40S) |
| Signpost-D-4B | 0.712 | 0.1615 | 0.0853 | 0.0914 | 62 ms (RTX PRO 6000) |

By type, the 9B scores 0.818 on true/false, 0.735 on choices and 0.670 on scales.

The maintainers rescored both models' published predictions and got the same numbers. The 9B was chosen among four
candidates on the benchmark's `train` split (0.7315 there); `train` is never trained on.

## How it is built

- **Fine-tuning:** LoRA in fp16, in exactly the prompt vLLM's `/v1/systemone` builds: one question per sequence, the
  answer read from the first reply token over the option labels. No extra head.
- **Data:** our own generated records in invented domains (2,575 to train on, 200 as dev), with soft gold from three
  simulated judges. Both models use the same data.
- **Final model:** several LoRA runs trained alike; the mean of their weight changes is added to the base at 0.75.
  - **4B:** three seeds at rank 16.
  - **9B:** rank 16 at learning rate 1e-4 with seeds 42 and 1042, and rank 32 at learning rate 5e-5 with seed 42.

## Notebooks

| Notebook | What it does |
|---|---|
| [01_train.ipynb](01_train.ipynb) | trains the LoRA runs, resuming from checkpoints (4B: about 37 minutes per seed on a Colab G4 GPU; 9B: about 100 minutes per run on an L40S) |
| [02_evaluate.ipynb](02_evaluate.ipynb) | merges the adapters, serves each model with vLLM nightly and scores it as the benchmark does; with `PUBLISH`, uploads the final model |
| [03_jevbench.ipynb](03_jevbench.ipynb) | runs both models on [JevBench](https://github.com/fstandhartinger/jevbench)'s 231 public items with its own CLI, and estimates its Intelligence score by family and by length |
| [learn_losses_and_clipping.ipynb](learn_losses_and_clipping.ipynb) | a learning notebook: loss functions and gradient clippers for decision models, compared on a small network (CPU) |

They run on Colab, Kaggle or Modal and install their own pinned packages. They need a Hugging Face token in
`HF_TOKEN` (the environment, a Kaggle or Colab secret, or the Modal secret `huggingface`).

**Settings** come from the environment, and the defaults reproduce Signpost-D-4B exactly:

| Setting | Default | Used for |
|---|---|---|
| `BASE_MODEL` | `Qwen/Qwen3.5-4B` | the base model |
| `SEEDS` | `42,1042,2042` | one LoRA run per seed |
| `LORA_R`, `LR` | `16`, `1e-4` | LoRA rank and learning rate |
| `GPUS`, `DTYPE` | `2` (fewer if fewer are visible), `fp16` | data-parallel training, and precision |
| `RUNS_JSON` | (02 only) | the runs to score and merge, instead of one run per seed |
| `DATA_V2` | off | add the signpost_d_v2 records (a pinned commit, tag `data/signpost_d_v2`) to train and dev |
| `JEV`, `JEV_FROM`, `JEV_TAG`, `JEV_LR_END`, `JEV_V1_EXTRA` | off | (01 only) Signpost-Jev: one more epoch from a `DATA_V2` run, for JevBench |
| `SCORE_TD`, `KEEP_EXPORT` | on, off | (02 only) whether to score Typed Decisions, and whether to keep the merged model |
| `PUBLISH`, `PUBLISH_RUN`, `MODEL_REPO` | off | (02 only) which model to upload, and where |

## Running on Modal

[modal/](modal/) holds the scripts used for the 9B:

- **[modal_run.py](modal/modal_run.py)** runs a notebook headless on a Modal GPU, with its checkpoints on a Modal volume
  so a rerun resumes:

  ```
  MODAL_GPU=L40S modal run --detach modal/modal_run.py --notebook 01_train.ipynb --name sd-9b \
      --settings "BASE_MODEL=Qwen/Qwen3.5-9B;SEEDS=42;GPUS=1"
  MODAL_GPU=L40S modal run --detach modal/modal_run.py --notebook 02_evaluate.ipynb --name sd-9b \
      --settings "BASE_MODEL=Qwen/Qwen3.5-9B;SEEDS=42"
  ```

- **[modal_upload_checkpoints.py](modal/modal_upload_checkpoints.py)** backs up runs' adapters and results to a private
  Hugging Face repo.
- **[modal_publish_export.py](modal/modal_publish_export.py)** publishes a merged model kept by `02_evaluate` (`KEEP_EXPORT=1`), with its
  adapter and a card, and makes the repo public.
- **[modal_release.py](modal/modal_release.py)** replaces a published model's card, makes it public and, optionally,
  posts the benchmark submission.
