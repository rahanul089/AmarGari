import streamlit as st
from utils.db import init_db, database_has_data, get_session, Vehicle, Violation, Payment
from utils import auth
from styles.theme import apply_theme, theme_toggle_control
from styles.components import page_header, metric_card, badge, stat, vehicle_card

st.set_page_config(page_title="AmarGari - Smart Driver & Vehicle Portal", page_icon="🚗", layout="wide")

init_db()

# --- AUTO-SEED BLOCK ---
if not database_has_data():
    with st.spinner("Setting up demo data for first run..."):
        from utils.seed import generate
        generate()
# ------------------------

apply_theme()

top_l, top_r = st.columns([6, 1])
with top_l:
    st.markdown("### 🚗 AmarGari <span style='font-size:0.9rem; opacity:0.55; font-weight:500;'>আমার গাড়ি</span>", unsafe_allow_html=True)
with top_r:
    theme_toggle_control(top_r)

if auth.is_logged_in():
    user = auth.current_user()
    page_header("Welcome back", f"Signed in as {user['name']}")
    st.markdown("")

    col1, col2, col3 = st.columns(3)
    with col1:
        metric_card("Role", user["role"].title())
    with col2:
        metric_card("Email", user["email"])
    with col3:
        if st.button("Log out"):
            auth.logout()
            st.rerun()

    st.divider()
    st.subheader("Quick Links")
    qc1, qc2, qc3, qc4 = st.columns(4)
    qc1.page_link("pages/1_Dashboard.py", label="📊 Dashboard")
    qc2.page_link("pages/2_Vehicles.py", label="🚙 Manage Vehicles")
    qc3.page_link("pages/3_Violations.py", label="🚨 View Violations")
    qc4.page_link("pages/4_Payments.py", label="💳 Make Payment")

else:
    db = get_session()
    vehicle_count = db.query(Vehicle).count()
    violation_count = db.query(Violation).count()
    fines_settled = sum(p.amount for p in db.query(Payment).filter(Payment.status == "completed").all())
    db.close()

    left, right = st.columns([1.15, 1])

    with left:
        badge("Citizen platform · not affiliated with BRTA or Police")
        st.markdown("")
        st.markdown(
            '<p class="main-header">Your vehicle, your fines,<br>'
            '<span class="accent">your papers</span> — in one place.</p>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p class="sub-header">AmarGari helps drivers and owners across Bangladesh track violations, '
            'store documents, catch renewal deadlines before they lapse, and pay fines without standing '
            'in a line.</p>',
            unsafe_allow_html=True,
        )
        st.markdown("")

        s1, s2, s3 = st.columns(3)
        with s1:
            stat(f"{vehicle_count}+" if vehicle_count else "0", "Vehicles tracked")
        with s2:
            stat(f"{violation_count}+" if violation_count else "0", "Violations logged")
        with s3:
            stat(f"৳{fines_settled/100000:.1f}L+" if fines_settled else "৳0", "Fines settled")

        st.markdown("")
        vehicle_card(
            reg_number="DHK · METRO · GA 11-2481",
            owner_name="Rafiq Ahmed",
            vehicle_type="Private Car",
            valid_till="Dec 2026",
        )
        st.caption("Every registered vehicle gets a digital card like this one.")

    with right:
        st.markdown('<div class="db-card">', unsafe_allow_html=True)
        tab_login, tab_register = st.tabs(["Sign in", "Create account"])

        with tab_login:
            st.caption("Sign in to your AmarGari account")
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Sign in", use_container_width=True)
                if submitted:
                    if auth.login(email, password):
                        st.rerun()
                    else:
                        st.error("Invalid email or password.")

            st.caption("Quick demo logins")
            d1, d2 = st.columns(2)
            with d1:
                if st.button("🧑‍💼 Owner demo", use_container_width=True):
                    if auth.login("demo@amargari.gov.bd", "Demo@123"):
                        st.rerun()
            with d2:
                if st.button("🛡️ Admin demo", use_container_width=True):
                    if auth.login("admin@amargari.gov.bd", "Admin@123"):
                        st.rerun()

        with tab_register:
            st.caption("Takes less than two minutes")
            with st.form("register_form"):
                name = st.text_input("Full name")
                email_r = st.text_input("Email", key="reg_email")
                phone = st.text_input("Phone number")
                nid = st.text_input("NID number")
                role = st.selectbox("I am registering as", ["driver", "owner"])
                password_r = st.text_input("Password", type="password", key="reg_pw")
                submitted_r = st.form_submit_button("Create account", use_container_width=True)
                if submitted_r:
                    if not (name and email_r and password_r):
                        st.error("Name, email and password are required.")
                    else:
                        ok, msg = auth.register_user(name, email_r, password_r, role, nid=nid, phone=phone)
                        if ok:
                            st.success(msg)
                        else:
                            st.error(msg)
        st.markdown('</div>', unsafe_allow_html=True)

st.divider()
st.caption("AmarGari Capstone Project · Built with Streamlit · Not affiliated with BRTA · All data is mock/demo data")
