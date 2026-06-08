"""
Recent Connections — DataPilot AI
Premium SaaS database history and quick reconnect workspace.
"""
import streamlit as st
from components.sidebar import render_sidebar
from utils.connection_manager import (
    get_saved_connections,
    delete_saved_connection,
    toggle_favorite,
    reconnect_database,
    get_relative_time
)
from utils.icons import get_icon

# ─────────────────────────────────────────────────────────────────────────────
# CSS Design tokens for premium cards
# ─────────────────────────────────────────────────────────────────────────────
_CONNECTIONS_CSS = """
<style>
/* ────────── STYLE STREAMLIT NATIVE CONTAINER AS THE CARD ────────── */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.conn-card-title):not(:has(div[data-testid="stVerticalBlockBorderWrapper"])) {
    background: linear-gradient(135deg, rgba(15,23,42,0.95), rgba(30,41,59,0.75)) !important;
    border: 1px solid rgba(99,102,241,0.18) !important;
    border-radius: 14px !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.25) !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    margin-bottom: 8px !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.conn-card-title):not(:has(div[data-testid="stVerticalBlockBorderWrapper"])):hover {
    border-color: rgba(99,102,241,0.45) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(99,102,241,0.22) !important;
}

.conn-badge {
    font-size: 0.68rem;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    display: inline-flex;
    align-items: center;
    gap: 4px;
}
/* Reduce native container padding to make card smaller */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.conn-card-title):not(:has(div[data-testid="stVerticalBlockBorderWrapper"])) > div > div[data-testid="stVerticalBlock"] {
    padding: 12px !important;
    gap: 0.25rem !important;
}
.conn-badge.mysql {
    background: rgba(0, 117, 143, 0.12);
    color: #38BDF8;
    border: 1px solid rgba(0, 117, 143, 0.35);
}
.conn-badge.postgresql, .conn-badge.postgres {
    background: rgba(51, 103, 145, 0.12);
    color: #60A5FA;
    border: 1px solid rgba(51, 103, 145, 0.35);
}
.conn-badge.sqlite, .conn-badge.file {
    background: rgba(139, 92, 246, 0.12);
    color: #A78BFA;
    border: 1px solid rgba(139, 92, 246, 0.35);
}
.conn-card-title {
    font-size: 1.15rem;
    font-weight: 800;
    color: #F8FAFC;
    margin-top: -12px;
    margin-bottom: 8px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    letter-spacing: -0.3px;
}
.conn-card-info {
    font-size: 0.8rem;
    color: #94A3B8;
    margin-bottom: 5px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.conn-card-footer {
    font-size: 0.72rem;
    color: #64748B;
    margin-top: 12px;
    border-top: 1px solid rgba(51, 65, 85, 0.25);
    padding-top: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.conn-usage-badge {
    background: rgba(99,102,241,0.08);
    border: 1px solid rgba(99,102,241,0.15);
    color: #A5B4FC;
    padding: 2px 6px;
    border-radius: 6px;
    font-size: 0.68rem;
    font-weight: 600;
}

/* ────────── NATIVE STAR BUTTON STRIPPED STYLING ────────── */
.star-button-marker {
    display: none !important;
}
/* Style star button inside its leaf column containing the star marker */
div[data-testid="stColumn"]:not(:has(div[data-testid="stColumn"])):has(.star-button-marker) button {
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    border-color: transparent !important;
    box-shadow: none !important;
    outline: none !important;
    padding: 0 !important;
    width: 32px !important;
    height: 32px !important;
    min-width: 32px !important;
    min-height: 32px !important;
    cursor: pointer !important;
    float: right !important;
    text-align: right !important;
    justify-content: flex-end !important;
    transform: none !important;
    transition: transform 0.2s ease !important;
    font-size: 1.45rem !important;
}
div[data-testid="stColumn"]:not(:has(div[data-testid="stColumn"])):has(.star-button-marker) button p,
div[data-testid="stColumn"]:not(:has(div[data-testid="stColumn"])):has(.star-button-marker) button span {
    font-size: 1.45rem !important;
}
div[data-testid="stColumn"]:not(:has(div[data-testid="stColumn"])):has(.star-button-marker) button:hover {
    transform: scale(1.2) !important;
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    border-color: transparent !important;
}
div[data-testid="stColumn"]:not(:has(div[data-testid="stColumn"])):has(.star-button-marker) button:active {
    transform: scale(0.95) !important;
    background: transparent !important;
}
/* Color for unfavorited star */
div[data-testid="stColumn"]:not(:has(div[data-testid="stColumn"])):has(.star-button-marker.unfavorited) button,
div[data-testid="stColumn"]:not(:has(div[data-testid="stColumn"])):has(.star-button-marker.unfavorited) button p,
div[data-testid="stColumn"]:not(:has(div[data-testid="stColumn"])):has(.star-button-marker.unfavorited) button span {
    color: #64748B !important; /* Grey/slate */
}
/* Color for favorited star */
div[data-testid="stColumn"]:not(:has(div[data-testid="stColumn"])):has(.star-button-marker.favorited) button,
div[data-testid="stColumn"]:not(:has(div[data-testid="stColumn"])):has(.star-button-marker.favorited) button p,
div[data-testid="stColumn"]:not(:has(div[data-testid="stColumn"])):has(.star-button-marker.favorited) button span {
    color: #F59E0B !important; /* Yellow/amber */
}
/* Optimize spacing for native columns in the header */
div[data-testid="stColumn"]:not(:has(div[data-testid="stColumn"])):has(.star-button-marker) {
    display: flex !important;
    justify-content: flex-end !important;
    align-items: center !important;
}

/* Hide the empty markdown blocks to prevent vertical gaps */
div.element-container:has(.delete-button-marker),
div.element-container:has(.star-button-marker) {
    display: none !important;
    margin: 0 !important;
    padding: 0 !important;
    height: 0 !important;
}

/* ────────── PREMIUM SAAS RED DELETE BUTTON ────────── */
.delete-button-marker {
    display: none !important;
}
div[data-testid="stColumn"]:not(:has(div[data-testid="stColumn"])):has(.delete-button-marker) button {
    color: #EF4444 !important;
    border-color: rgba(239, 68, 68, 0.4) !important;
    background: rgba(239, 68, 68, 0.08) !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stColumn"]:not(:has(div[data-testid="stColumn"])):has(.delete-button-marker) button p,
div[data-testid="stColumn"]:not(:has(div[data-testid="stColumn"])):has(.delete-button-marker) button span {
    color: #EF4444 !important;
    white-space: nowrap !important;
}
div[data-testid="stColumn"]:not(:has(div[data-testid="stColumn"])):has(.delete-button-marker) button:hover {
    color: #FFFFFF !important;
    background: #EF4444 !important;
    border-color: #EF4444 !important;
    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.35) !important;
    transform: translateY(-1px) !important;
}
div[data-testid="stColumn"]:not(:has(div[data-testid="stColumn"])):has(.delete-button-marker) button:hover p,
div[data-testid="stColumn"]:not(:has(div[data-testid="stColumn"])):has(.delete-button-marker) button:hover span {
    color: #FFFFFF !important;
}
div[data-testid="stColumn"]:not(:has(div[data-testid="stColumn"])):has(.delete-button-marker) button:active {
    transform: translateY(0px) !important;
}
</style>
"""

@st.dialog("Quick Reconnect to Database")
def render_reconnect_modal(conn):
    """Modern modal dialog requesting only the password to initiate reconnect."""
    
    # Inject capsule styling directly inside the modal dialog container
    st.markdown("""
    <style>
    /* Target ONLY the Connect button (the ultimate bulletproof selector list for stModal and role="dialog") */
    div[role="dialog"] button[data-testid*="primary"],
    div[role="dialog"] button[data-testid^="baseButton-primary"],
    div[role="dialog"] button[kind="primary"],
    [role="dialog"] button[data-testid*="primary"],
    [role="dialog"] button[data-testid^="baseButton-primary"],
    [role="dialog"] button[kind="primary"],
    div[role="dialog"] div[data-testid="column"]:nth-of-type(2) button,
    div[role="dialog"] div[data-testid="column"]:nth-child(2) button,
    div[data-testid="stModal"] div[data-testid="column"]:nth-of-type(2) button,
    [data-testid="stModal"] div[data-testid="column"]:nth-of-type(2) button,
    div[role="dialog"] button:nth-of-type(3),
    div[role="dialog"] button:nth-of-type(2),
    div[data-testid="stModal"] button:nth-of-type(3),
    div[data-testid="stModal"] button:nth-of-type(2),
    [role="dialog"] button:nth-of-type(3),
    [role="dialog"] button:nth-of-type(2) {
        background: linear-gradient(135deg, #8B5CF6, #7C3AED) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px !important;
        height: 46px !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 14px rgba(139,92,246,0.3) !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    div[role="dialog"] button[data-testid*="primary"]:hover,
    div[role="dialog"] button[data-testid^="baseButton-primary"]:hover,
    div[role="dialog"] button[kind="primary"]:hover,
    [role="dialog"] button[data-testid*="primary"]:hover,
    [role="dialog"] button[data-testid^="baseButton-primary"]:hover,
    [role="dialog"] button[kind="primary"]:hover,
    div[role="dialog"] div[data-testid="column"]:nth-of-type(2) button:hover,
    div[role="dialog"] div[data-testid="column"]:nth-child(2) button:hover,
    div[data-testid="stModal"] div[data-testid="column"]:nth-of-type(2) button:hover,
    [data-testid="stModal"] div[data-testid="column"]:nth-of-type(2) button:hover,
    div[role="dialog"] button:nth-of-type(3):hover,
    div[role="dialog"] button:nth-of-type(2):hover,
    div[data-testid="stModal"] button:nth-of-type(3):hover,
    div[data-testid="stModal"] button:nth-of-type(2):hover,
    [role="dialog"] button:nth-of-type(3):hover,
    [role="dialog"] button:nth-of-type(2):hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 22px rgba(139,92,246,0.5) !important;
        background: linear-gradient(135deg, #9333EA, #8B5CF6) !important;
        color: #FFFFFF !important;
    }
    </style>
    """, unsafe_allow_html=True)

    db_type = conn.get('database_type', '').lower()
    st.markdown(f"### Reconnect to **{conn.get('database', 'Database')}**")
    if db_type in ("sqlite", "sqlite3", "file"):
        meta_html = f"FILE &bull; {conn.get('file_path', 'Local File')}"
    else:
        meta_html = f"{conn.get('database_type', '').upper()} &bull; {conn.get('username', '')}@{conn.get('host', '')}:{conn.get('port', '')}"
        
    st.markdown(
        f"<div style='font-size:0.82rem; color:#64748B; margin-bottom:16px;'>"
        f"{meta_html}"
        f"</div>",
        unsafe_allow_html=True
    )

    # Use standard Streamlit form to support Enter key submission natively!
    with st.form(key="reconnect_password_form", clear_on_submit=False):
        password = st.text_input(
            "Enter Database Password",
            type="password",
            placeholder="••••••••",
            help="Please input the database authentication password."
        )
        
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        
        col_cancel, col_connect = st.columns(2)
        with col_cancel:
            # st.form_submit_button close the form but we handle cancel manually
            cancel_clicked = st.form_submit_button("Cancel", use_container_width=True)
        with col_connect:
            connect_clicked = st.form_submit_button("Connect", type="primary", use_container_width=True)

        if connect_clicked:
            if not password:
                st.error("Authentication failed: Password cannot be blank.")
            else:
                with st.spinner("Establishing secure connection..."):
                    success, msg = reconnect_database(conn, password)
                
                if success:
                    st.success("Connected successfully!")
                    st.toast("🚀 Database loaded! Redirecting to Dashboard...")
                    # Automatically redirect to main workspace dashboard
                    st.session_state["menu"] = "Dashboard"
                    st.query_params["page"] = "Dashboard"
                    st.rerun()
                else:
                    st.error(f"Connection Failed: {msg}")
                    
        if cancel_clicked:
            st.rerun()

def show_past_connections():
    """Renders the central Recent Connections page."""
    # Ensure sidebar is rendered first
    render_sidebar()
    
    # Inject CSS
    st.markdown(_CONNECTIONS_CSS, unsafe_allow_html=True)

    # ── Page Header ──
    st.title("Recent Connections")
    st.markdown(
        "Manage and reconnect to your configured enterprise data sources. "
        "For security and compliance, authentication credentials are not persisted locally."
    )

    st.markdown("<hr style='border:none; border-top:1px solid #1E293B; margin: 12px 0 20px 0;'>", unsafe_allow_html=True)

    # Load connections history list
    saved_connections = get_saved_connections()

    if not saved_connections:
        # Empty state screen
        st.markdown(
            "<div style='text-align:center; padding: 60px 20px; background: rgba(15,23,42,0.4); border-radius:16px; border: 1px dashed rgba(99,102,241,0.2);'>"
            "<h3 style='color: #94A3B8;'>No Database Connections History</h3>"
            "<p style='color: #64748B; font-size:0.9rem; margin-top:8px; margin-bottom:20px;'>"
            "Your database connections (MySQL and PostgreSQL) will automatically be saved here once initialized."
            "</p>"
            "</div>",
            unsafe_allow_html=True
        )
        if st.button("Connect New Database Now", type="primary"):
            st.session_state["menu"] = "Dashboard"
            st.query_params["page"] = "Dashboard"
            st.rerun()
        return

    # ── Search & Filter Controls bar ──
    ctrl_search, ctrl_sort = st.columns([3, 1])
    with ctrl_search:
        search_query = st.text_input(
            "Search connections",
            placeholder="Search by Database Name, Host, Port, Username...",
            label_visibility="collapsed"
        )
    with ctrl_sort:
        sort_by = st.selectbox(
            "Sort by",
            ["Recently Connected", "Most Used", "Database Name"],
            label_visibility="collapsed"
        )

    # ── Filter & Sort Logic ──
    filtered_connections = []
    for conn in saved_connections:
        match_parts = [
            conn.get('database', ''),
            conn.get('host', ''),
            conn.get('username', ''),
            conn.get('database_type', ''),
            conn.get('source_filename', ''),
            conn.get('file_path', '')
        ]
        match_str = " ".join(str(part) for part in match_parts if part).lower()
        if not search_query or search_query.lower() in match_str:
            filtered_connections.append(conn)

    # Re-sort list based on selectbox
    if sort_by == "Most Used":
        filtered_connections.sort(key=lambda x: x.get("usage_count", 0), reverse=True)
    elif sort_by == "Database Name":
        filtered_connections.sort(key=lambda x: x.get("database", "").lower())
    else:
        # Default: Recently Connected (Favorites pinned first, then recency)
        # The connection_manager get_saved_connections is already sorting favorites first, then recency
        # But if we did search/filter, let's keep that default sorting sequence
        pass

    if not filtered_connections:
        st.info("No connections match your search query.")
        return

    # ── Connections Cards Grid ──
    # Arrange cards in a beautiful 3-column layout
    cols = st.columns(3, gap="medium")
    
    for idx, conn in enumerate(filtered_connections):
        col_target = cols[idx % 3]
        
        with col_target:
            relative_time = get_relative_time(conn.get("last_connected"))
            is_fav = conn.get("is_favorite", False)
            fav_emoji = "★" if is_fav else "☆"
            fav_color = "#F59E0B" if is_fav else "#64748B"
            
            # HTML Card natively rendered inside st.container(border=True)
            with st.container(border=True):
                # Header row: Badge on left, native star button on right
                header_col1, header_col2 = st.columns([5, 1])
                with header_col1:
                    db_type = conn['database_type'].lower()
                    display_type = "FILE" if db_type in ("sqlite", "sqlite3", "file") else db_type.upper()
                    icon_svg = get_icon(db_type, size=14, color="currentColor")
                    st.markdown(f"<span class='conn-badge {db_type}'>{icon_svg} {display_type}</span>", unsafe_allow_html=True)
                with header_col2:
                    # Dynamically set active (yellow) vs inactive (grey) color using scoped classes
                    fav_class = "favorited" if is_fav else "unfavorited"
                    st.markdown(f'<div class="star-button-marker {fav_class}" id="star-marker-{conn["id"]}"></div>', unsafe_allow_html=True)
                    if st.button(fav_emoji, key=f"star_{conn['id']}", help="Pin connection to top"):
                        toggle_favorite(conn["id"])
                        st.rerun()

                # Card Content
                st.markdown(f"<div class='conn-card-title' title='{conn.get('database', 'Database')}'>{conn.get('database', 'Database')}</div>", unsafe_allow_html=True)
                if db_type in ("sqlite", "sqlite3", "file"):
                    file_svg = get_icon("file-text", size=14, color="#64748B")
                    loc_svg = get_icon("map-pin", size=14, color="#64748B")
                    st.markdown(f"<div class='conn-card-info'>{file_svg} &nbsp;File: {conn.get('source_filename') or conn.get('database', 'Local File')}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='conn-card-info'>{loc_svg} &nbsp;Location: Local Storage</div>", unsafe_allow_html=True)
                else:
                    globe_svg = get_icon("globe", size=14, color="#64748B")
                    user_svg = get_icon("user", size=14, color="#64748B")
                    st.markdown(f"<div class='conn-card-info'>{globe_svg} &nbsp;{conn.get('host', '127.0.0.1')}:{conn.get('port', 3306)}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='conn-card-info'>{user_svg} &nbsp;User: {conn.get('username', 'root')}</div>", unsafe_allow_html=True)
                
                # Card Footer
                clock_svg = get_icon("clock", size=13, color="#64748B")
                st.markdown(f"""
                <div class='conn-card-footer'>
                    <span>{clock_svg} &nbsp;{relative_time}</span>
                    <span class='conn-usage-badge'>{conn.get("usage_count", 1)} connects</span>
                </div>
                """, unsafe_allow_html=True)
            
                # Interactive Action Buttons row directly inside native card container
                st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
                btn_col1, btn_col2 = st.columns([5, 3])
                with btn_col1:
                    # Primary action: Connect Again
                    if st.button("Connect", key=f"btn_reconn_{conn['id']}", use_container_width=True, type="primary"):
                        if db_type == "sqlite":
                            with st.spinner("Connecting to SQLite file..."):
                                success, msg = reconnect_database(conn, "")
                            if success:
                                st.session_state["menu"] = "Dashboard"
                                st.query_params["page"] = "Dashboard"
                                st.rerun()
                            else:
                                st.error(f"Connection Failed: {msg}")
                        else:
                            st.session_state["reconnect_conn"] = conn
                            st.rerun()
                with btn_col2:
                    # Delete stored card metadata
                    st.markdown(f'<div class="delete-button-marker" id="del-{conn["id"]}"></div>', unsafe_allow_html=True)
                    if st.button("Delete", key=f"btn_del_{conn['id']}", use_container_width=True, help="Remove connection details"):
                        delete_saved_connection(conn["id"])
                        st.toast(f"🗑️ Removed connection: {conn['database']}")
                        st.rerun()
                    
            st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # ── Check & Trigger Reconnect Popup modal ──
    if "reconnect_conn" in st.session_state:
        reconnect_target = st.session_state.pop("reconnect_conn")
        if reconnect_target.get("database_type", "").lower() == "sqlite":
            with st.spinner("Connecting to SQLite file..."):
                success, msg = reconnect_database(reconnect_target, "")
            if success:
                st.success("Connected successfully!")
                st.toast("🚀 Database loaded! Redirecting to Dashboard...")
                st.session_state["menu"] = "Dashboard"
                st.query_params["page"] = "Dashboard"
                st.rerun()
            else:
                st.error(f"Connection Failed: {msg}")
        else:
            render_reconnect_modal(reconnect_target)
