import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
from cryptography.fernet import Fernet
st.set_page_config(page_title="Signal Debug Dashboard", layout="wide")
st.title("Signal Debug Dashboard")

st.markdown("""
Welcome to the **Signal Debug Dashboard**. This interface visualizes recent secure signal packets ingested by the system.  
Use this tool to:
- Monitor signal structure
- Understand signal frequency and timing
- Debug and verify ingestion flow

Each signal contains:
- A **timestamp**
- 8 simulated **EEG-like channel values**

You can toggle between viewing raw encrypted bytes or decrypted signal contents below.
""")
SIGNAL_ENCRYPTION_KEY = b'cXdOWnRHRVB6N3pjQ3R5cXNUbEFwZlAyRzhQb1ZqV0Y=' 
cipher = Fernet(SIGNAL_ENCRYPTION_KEY)
view_mode = st.radio("Select View Mode", ["Decrypted (JSON)", "Raw Encrypted Bytes"])
DATA_DIR = "data"
files = sorted(os.listdir(DATA_DIR), reverse=True)

signals = []
errors = []

for f in files[:10]:
    file_path = os.path.join(DATA_DIR, f)
    try:
        with open(file_path, "rb") as jf:
            encrypted = jf.read()
            if view_mode == "Raw Encrypted Bytes":
                signals.append({
                    "__file__": f,
                    "encrypted_bytes": encrypted.hex()
                })
            else:
                decrypted = cipher.decrypt(encrypted)
                data = json.loads(decrypted.decode())
                data["__file__"] = f
                signals.append(data)
    except Exception as e:
        errors.append((f, str(e)))

if signals:
    st.subheader("Signal Summary")
    st.markdown(f"""
    - **Total Signals Displayed**: `{len(signals)}`
    - **Channels per Signal**: `8`
    - **Most Recent File**: `{signals[0]['__file__']}`
    - **Oldest File**: `{signals[-1]['__file__']}`
    - **Mode**: `{view_mode}`
    """)
if not signals:
    st.info("No signal data available.")
else:
    if view_mode == "Raw Encrypted Bytes":
        st.subheader("Raw Encrypted Signals")
        st.dataframe(pd.DataFrame(signals))
    else:
        df = pd.DataFrame(signals)
        st.subheader("Recent Signals (Decrypted)")
        st.dataframe(df[["__file__", "timestamp", "channels"]])
        st.subheader("Channel Breakdown (Stacked Bar per Signal)")
        st.markdown("Each bar shows all 8 EEG-like channel values for one signal. Color = channel index.")

        try:
            channel_matrix = pd.DataFrame(df["channels"].tolist())
            channel_matrix.columns = [f"Ch-{i}" for i in range(channel_matrix.shape[1])]
            channel_matrix["Signal #"] = list(range(len(channel_matrix)))
            channel_matrix.set_index("Signal #", inplace=True)
            st.bar_chart(channel_matrix)
        except:
            st.warning("Could not process channel breakdown.")
        st.subheader("Signal Timing Between Signals (in seconds)")
        st.markdown("Visualizes the time difference between consecutive signals.")

        try:
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df = df.sort_values("timestamp")
            df["delta_sec"] = df["timestamp"].diff().dt.total_seconds()
            st.line_chart(df["delta_sec"])
        except:
            st.warning("Timestamp formatting issue.")
if errors:
    st.warning("Some files could not be decrypted:")
    for f, e in errors:
        st.text(f"{f} → {e}")
with st.expander("Signal Format & Help"):
    st.markdown("""
    **Signal Structure**:
    ```json
    {
        "timestamp": "2025-06-10T12:00:00Z",
        "channels": [0.12, -0.88, ..., 1.43]  // 8 floats
    }
    ```

    **Usage Tips**:
    - Use *"Decrypted (JSON)"* mode to inspect real signal values.
    - Use *"Raw Encrypted Bytes"* to verify encryption correctness.
    - Refer to *Channel Breakdown* and *Signal Timing* to debug irregularities.
    """)
