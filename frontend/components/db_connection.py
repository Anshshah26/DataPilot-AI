import streamlit as st

from services.api_client import connect_db
from utils.db_context import load_database_context
from utils.icons import get_icon


def render_db_connection():

    st.markdown("""
    <style>
    .db-form-card {
        background: linear-gradient(135deg, rgba(15,23,42,0.95), rgba(30,41,59,0.8));
        border: 1px solid rgba(99,102,241,0.25);
        border-radius: 16px;
        padding: 28px 28px 20px 28px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.03);
        margin-top: 8px;
    }
    .db-form-header-row {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 4px;
    }
    .db-form-icon-pill {
        color: #8B5CF6;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .db-form-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #E2E8F0;
    }
    .db-form-caption {
        font-size: 0.82rem;
        color: #64748B;
        margin-bottom: 20px;
        padding-left: 0px;
    }
    </style>

    <script>
    // Periodically search for inputs and disable browser autofill/autocomplete recommendations
    const disableCredentialsAutofill = () => {
        const inputs = document.querySelectorAll('input');
        inputs.forEach(input => {
            input.setAttribute('autocomplete', 'new-password');
            input.setAttribute('autocorrect', 'off');
            input.setAttribute('spellcheck', 'false');
        });
    };
    
    // Run immediately and set intervals to handle dynamic Streamlit re-renders
    disableCredentialsAutofill();
    const autofillInterval = setInterval(disableCredentialsAutofill, 500);
    
    // Clear interval after 5 seconds to prevent unnecessary processing
    setTimeout(() => {
        clearInterval(autofillInterval);
    }, 5000);
    </script>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='db-form-header-row'>
        <div class='db-form-title'>Initialize Database Connection</div>
    </div>
    <div class='db-form-caption'>Enterprise-grade connectivity — MySQL &amp; PostgreSQL supported with encrypted sessions</div>
    """, unsafe_allow_html=True)

    # DB Type selector with icons at top
    db_type_col1, db_type_col2 = st.columns(2)
    with db_type_col1:
        db_type = st.selectbox(
            "Database Type",
            ["MySQL", "PostgreSQL"],
            format_func=lambda x: f"MySQL Database" if x == "MySQL" else f"PostgreSQL Database"
        )

    default_port = "3306" if db_type == "MySQL" else "5432"

    col1, col2 = st.columns(2)

    with col1:
        host = st.text_input(
            "Host",
            value="",
            placeholder="localhost or IP address"
        )

        username = st.text_input(
            "Username",
            value="",
            placeholder="Database username"
        )

        database = st.text_input(
            "Database Name",
            value="",
            placeholder="e.g. sales_db"
        )

    with col2:
        port = st.text_input(
            "Port",
            value="",
            placeholder=default_port
        )

        password = st.text_input(
            "Password",
            value="",
            type="password",
            placeholder="Enter database password"
        )

        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

    st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)

    if st.button("Initialize Database", type="primary", use_container_width=True):

        if not host or not username or not database or not port or not password:
            st.error("Please fill in all database connection details before connecting.")
        else:
            with st.spinner("Connecting to database..."):
                result = connect_db(host, port, username, password, database, db_type)

            if result.get("success") or result.get("status") == "ok":
                st.session_state["connected"] = True
                db_info = {
                    "host": host,
                    "port": int(port),
                    "username": username,
                    "password": password,
                    "database": database,
                    "database_type": db_type.lower(),
                }
                st.session_state["db_info"] = db_info

                with st.spinner("Loading schema and metrics..."):
                    ok, msg = load_database_context(db_info, force_refresh=True)

                if ok:
                    # Automatically store successfully connected database (passwords are NOT saved to .connections.json)
                    try:
                        from utils.connection_manager import save_connection, save_active_session
                        save_connection(
                            host=host,
                            port=int(port),
                            username=username,
                            database=database,
                            database_type=db_type
                        )
                        # Also persist the full connection (with password) for refresh restore
                        _uname = st.session_state.get("user_profile", {}).get("username", "default")
                        save_active_session(_uname, db_info)
                    except Exception:
                        pass
                    
                    try:
                        from utils.settings_manager import log_activity
                        log_activity(f"Connected to database: '{database}' ({db_type.upper()})")
                    except Exception:
                        pass
                    st.success(f"Connected to {db_type} database successfully!")
                    st.rerun()
                else:
                    st.session_state["connected"] = False
                    st.error(f"Connected but failed to load schema: {msg}")
            else:
                error_msg = result.get("message", "Unknown error occurred during connection.")
                st.error(f"Connection Failed: {error_msg}")