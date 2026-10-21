# Python/NLP version (scikit-learn)

The Pages demo runs a compact model fully in your browser. This folder is the
proper training pipeline with a larger vocabulary and full holdout +
cross-validation reporting.

```bash
pip install -r requirements.txt
python pipeline.py [--data corpus.jsonl]
```

`corpus.jsonl` ships the project corpus (`{"text","label"}` per line).
Point `--data` at a larger JSONL export (e.g. from the UCI YouTube Spam
Collection) for serious training. Metrics land in `metrics.json`; the model
in `model.joblib`.
