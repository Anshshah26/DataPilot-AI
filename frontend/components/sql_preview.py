"""
SQL Preview — DataPilot AI
Sticky/floating status bar + collapsible SQL panel.
"""
import streamlit as st


_CSS = """
<style>
/* ── Floating SQL status toast (always visible at top of main area) ── */
.sql-status-toast {
    display: flex;
    align-items: center;
    gap: 10px;
    background: linear-gradient(135deg, rgba(16,185,129,0.12), rgba(16,185,129,0.06));
    border: 1px solid rgba(16,185,129,0.3);
    border-radius: 10px;
    padding: 8px 14px;
    margin-bottom: 14px;
    font-size: 0.82rem;
    font-weight: 600;
    color: #10B981;
    position: sticky;
    top: 0;
    z-index: 100;
    backdrop-filter: blur(8px);
}
.sql-status-dot {
    width: 7px; height: 7px;
    background: #10B981;
    border-radius: 50%;
    box-shadow: 0 0 6px rgba(16,185,129,0.6);
    flex-shrink: 0;
    animation: pulse-green 2s infinite;
}
@keyframes pulse-green {
    0%, 100% { box-shadow: 0 0 4px rgba(16,185,129,0.4); }
    50%       { box-shadow: 0 0 10px rgba(16,185,129,0.8); }
}
/* ── SQL preview card ── */
.sql-preview-card {
    background: linear-gradient(135deg, rgba(11,17,32,0.95), rgba(15,23,42,0.95));
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 14px;
    padding: 16px 18px;
    margin-bottom: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
.sql-preview-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 10px;
}
.sql-preview-label {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #6366F1;
}
.sql-explanation-box {
    background: rgba(99,102,241,0.06);
    border: 1px solid rgba(99,102,241,0.15);
    border-radius: 8px;
    padding: 10px 14px;
    margin-top: 10px;
    font-size: 0.82rem;
    color: #94A3B8;
    line-height: 1.55;
}
</style>
"""


def render_sql_preview(sql_query: str, explanation: str = None) -> None:
    """Render a premium SQL preview card."""
    st.markdown(_CSS, unsafe_allow_html=True)

    # ── SQL code card ─────────────────────────────────────────────── #
    st.markdown("<div class='sql-preview-card'>", unsafe_allow_html=True)
    st.markdown("""
    <div class='sql-preview-header'>
        <span class='sql-preview-label'>Generated SQL</span>
    </div>
    """, unsafe_allow_html=True)

    st.code(sql_query, language="sql")

    if explanation:
        st.markdown(
            f"<div class='sql-explanation-box'>\n\n{explanation}\n\n</div>",
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)