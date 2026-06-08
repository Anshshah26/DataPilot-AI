"""
Export Buttons — DataPilot AI
Premium styled export panel with CSV download.
"""
import streamlit as st
import pandas as pd


_CSS = """
<style>
.export-bar {
    display: flex;
    align-items: center;
    gap: 10px;
    background: rgba(15,23,42,0.6);
    border: 1px solid rgba(51,65,85,0.4);
    border-radius: 10px;
    padding: 8px 14px;
}
.export-label {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #475569;
    margin-right: 4px;
}
[data-testid="stDownloadButton"] button {
    justify-content: center !important;
    text-align: center !important;
    min-width: 150px !important;
}
</style>
"""


def render_export_buttons(data) -> None:
    """Render a styled export bar with download options."""
    if not data:
        return

    st.markdown(_CSS, unsafe_allow_html=True)

    df = pd.DataFrame(data)
    csv = df.to_csv(index=False).encode("utf-8")

    # Use a tighter column layout so the button isn't massive
    col_csv, col_space = st.columns([2, 8])
    with col_csv:
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="query_results.csv",
            mime="text/csv",
            use_container_width=True, # Button will fill the smaller column, but text is now centered
        )