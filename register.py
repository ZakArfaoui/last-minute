import streamlit as st
import os
import json
from datetime import datetime

st.set_page_config(page_title="Auth System", page_icon="🔐", layout="centered")

# -----------------------------
# FILE STORAGE SETUP
# -----------------------------
USERS_FILE = "users.txt"

def load_users():
    """Load users from text file"""
    if not os.path.exists(USERS_FILE):
        return {}
    
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return {}
            return json.loads(content)
    except Exception as e:
        st.error(f"Error loading users: {e}")
        return {}

def save_users(users):
    """Save users to text file"""
    try:
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        st.error(f"Error saving users: {e}")
        return False

def init_session():
    """Initialize session state"""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user = None

# -----------------------------
# AUTH PAGE
# -----------------------------
def auth_page():
    init_session()
    
    # Load users from file
    users = load_users()
    
    st.title("🔐 Credit AI - Authentication")

    menu = st.radio("Choose option", ["Login", "Register"])

    # ---------------- REGISTER ----------------
    if menu == "Register":
        st.subheader("📝 Create account")

        first_name = st.text_input("First Name", key="reg_fname")
        last_name = st.text_input("Last Name", key="reg_lname")
        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_pass")
        confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")

        role = st.selectbox("Select role", ["User 👤", "Bank 🏦"], key="reg_role")

        if st.button("Create account"):
            # Validation
            missing_fields = []
            if not first_name or first_name.strip() == "":
                missing_fields.append("First Name")
            if not last_name or last_name.strip() == "":
                missing_fields.append("Last Name")
            if not email or email.strip() == "":
                missing_fields.append("Email")
            if not password or password.strip() == "":
                missing_fields.append("Password")
            
            if missing_fields:
                st.error(f"Please fill: {', '.join(missing_fields)} ❌")
            elif password != confirm_password:
                st.error("Passwords do not match ❌")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters ❌")
            elif email in users:
                st.error("Account already exists ❌")
            else:
                # Create new user
                users[email] = {
                    "first_name": first_name.strip(),
                    "last_name": last_name.strip(),
                    "password": password,
                    "role": role,
                    "created_at": datetime.now().isoformat()
                }
                
                if save_users(users):
                    st.success("Account created successfully ✅")
                    st.info("Please login with your new account")

    # ---------------- LOGIN ----------------
    if menu == "Login":
        st.subheader("🔑 Login")

        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            user = users.get(email)

            if user and user["password"] == password:
                st.session_state.logged_in = True
                st.session_state.user = user
                
                # FIXED: Use pages/ prefix for correct path
                if "Bank" in user["role"]:
                    st.switch_page("pages/banker_dashboard.py")
                else:
                    st.switch_page("pages/client_portal.py")
            else:
                st.error("Invalid email or password ❌")

    # Show debug info in sidebar
    with st.sidebar:
        st.header("Debug Info")
        st.write(f"Users file: {USERS_FILE}")
        st.write(f"Exists: {os.path.exists(USERS_FILE)}")
        st.write(f"Total accounts: {len(users)}")
        if users:
            st.write("Registered emails:")
            for email in users.keys():
                st.write(f"- {email}")


# -----------------------------
# RUN APP
# -----------------------------
init_session()

if st.session_state.logged_in:
    # FIXED: Use pages/ prefix for correct path
    user = st.session_state.user
    if "Bank" in user["role"]:
        st.switch_page("pages/banker_dashboard.py")
    else:
        st.switch_page("client_portal.py")
else:
    auth_page()