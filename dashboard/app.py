import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
st.set_page_config(page_title="Signal Debug Dashboard", layout="wide")
st.title("📡 Real-Time Signal Ingestion Dashboard")
DATA_DIR = "data"
files = sorted(os.listdir(DATA_DIR), reverse=True)
signals = []
for f in files[:10]:
    try:
        with open(os.path.join(DATA_DIR, f)) as jf:
            d = json.load(jf)
            d["__file__"] = f
            signals.append(d)
    except Exception as e:
        st.warning(f"Failed to load {f}: {e}")
if signals:
    df = pd.DataFrame(signals)
    st.subheader("🧠 Recent Signals (Last 10)")
    st.dataframe(df[["__file__", "timestamp", "channels"]])
    st.subheader("📊 Channel Stats")
    try:
        channel_matrix = pd.DataFrame(df["channels"].tolist())
        st.bar_chart(channel_matrix)
    except Exception as e:
        st.error("Could not render channel breakdown: " + str(e))
    st.subheader("⏱ Signal Interval Check")
    try:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp")
        df["delta_sec"] = df["timestamp"].diff().dt.total_seconds()
        st.line_chart(df["delta_sec"])
    except Exception as e:
        st.error("Timestamp delta plot error: " + str(e))
else:
    st.info("No signals found yet in `data/`.")
st.subheader("⚙️ Diagnostics")
st.write(f"📁 Files scanned: {len(files)}")
st.write(f"✅ Valid signals loaded: {len(signals)}")
st.write(f"⚠️ Missing channels: {sum(1 for s in signals if len(s.get('channels', [])) != 8)}")
