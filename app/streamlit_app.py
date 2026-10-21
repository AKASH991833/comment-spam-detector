"""Comment Spam Detector — Streamlit UI over the trained TF-IDF + LogReg pipeline."""
import json
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
pipe = joblib.load(ROOT / "ml" / "model.joblib")
metrics = json.load(open(ROOT / "ml" / "metrics.json"))
CLASSES = list(pipe.classes_)
POS = classes_idx = CLASSES.index(1) if 1 in CLASSES else -1

st.set_page_config(page_title="Comment Spam Detector", page_icon="💬")
st.title("💬 Comment Spam Detector")
st.caption("TF-IDF + logistic regression, served live · [Browser demo](https://akash991833.github.io/comment-spam-detector/) · [Code](https://github.com/AKASH991833/comment-spam-detector)")

mode = st.tabs(["Single comment", "Batch (one per line)"])

with mode[0]:
    text = st.text_area("Comment", height=120, placeholder="Nice video! Check out my channel for free ...")
    if st.button("Check", type="primary") and text.strip():
        p = float(pipe.predict_proba([text])[0][POS])
        (st.error if p >= 0.5 else st.success)(
            f"{'🚫 Spam' if p >= 0.5 else '✅ Looks genuine'} — spam score **{p:.0%}**")
        st.progress(p)

with mode[1]:
    batch = st.text_area("Comments, one per line", height=180)
    if st.button("Screen all") and batch.strip():
        lines = [l.strip() for l in batch.splitlines() if l.strip()]
        probs = pipe.predict_proba(lines)[:, POS]
        df = pd.DataFrame({"comment": lines, "spam_score": probs.round(3),
                           "verdict": ["spam" if p >= 0.5 else "ok" for p in probs]})
        st.dataframe(df, use_container_width=True)
        st.download_button("Download CSV", df.to_csv(index=False), "spam-screening.csv")

with st.expander("Model & honest metrics"):
    st.json(metrics)
    st.warning(
        "Text-pattern model: it learns what spam **looks like**, not intent. "
        "Short or unusual genuine comments can be flagged — review before acting."
    )
