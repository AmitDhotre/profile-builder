import streamlit as st
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="ProfileBuilder 404 😅", page_icon="🧾", layout="centered")

ADMIN_PASSWORD = "jenne"
CSV_FILE = "personal_records.csv"

# ---------------- ANIMATION CSS ----------------
st.markdown("""
<style>
.fade-in {
    animation: fadeIn 0.6s ease-in-out;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(15px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "step" not in st.session_state:
    st.session_state.step = "home"

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# ---------------- LOAD / CREATE CSV ----------------
if os.path.exists(CSV_FILE):
    data = pd.read_csv(CSV_FILE)
else:
    data = pd.DataFrame(columns=[
        "ID", "Name", "Mobile", "Instagram_ID", "Snapchat_ID",
        "Gender", "City", "DOB", "Age"
    ])
    data.to_csv(CSV_FILE, index=False)

# =================================================
# 🏠 HOME PAGE
# =================================================
if st.session_state.step == "home":
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    st.title("CAMPUS FORM 🏦")
    st.caption("Crafted with care by AJ 🗿")

    if st.button("Start Application"):
        st.session_state.step = "rules"
        st.rerun()

    if st.button("Restricted Area ☠"):
        st.session_state.step = "admin_login"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# =================================================
# 📜 RULES PAGE
# =================================================
elif st.session_state.step == "rules":
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    st.header("📜 A Few Things to Know")
    st.markdown("""
    1. 👤 Enter correct information  
    2. 📞 Valid mobile number required  
    3. ❌ Fake entries will be deleted  
    4. 🔑 If you know the password, you may access the information ahead 
    5. 🛑 Interested? Then go ahead and fill in your details, No Pressure  
    """)

    agree = st.checkbox("ദ്ദി(ᵔᗜᵔ) I have read and agree to the rules")

    if agree and st.button("⏩ CONTINUE"):
        st.session_state.step = "form"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# =================================================
# 📝 USER FORM PAGE
# =================================================
elif st.session_state.step == "form":
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    st.header("📝 Time for your mini introduction ")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("👤 Name")
    with col2:
        mobile = st.text_input("📞 Mobile (10 digits)")

    st.subheader("📱 Social Media Check 😄")
    
    platform = st.radio(
        "So… where do you actually hang out online? 🤔",
        ["📸 Instagram", "👻 Snapchat", "😎 Both", "🙈 None (I’m mysterious)"]
    )
    
    col3, col4 = st.columns(2)
    
    insta_id = ""
    snap_id = ""
    
    if platform == "📸 Instagram":
        with col3:
            insta_id = st.text_input("📸 Instagram ID", placeholder="username_here")
        st.caption("😄 Insta it is! Reels gang spotted.")
    
    elif platform == "👻 Snapchat":
        with col4:
            snap_id = st.text_input("👻 Snapchat ID", placeholder="snap_username")
        st.caption("👻 Snap life! Streaks must continue 🔥")
    
    elif platform == "😎 Both":
        with col3:
            insta_id = st.text_input("📸 Instagram ID", placeholder="insta_username")
        with col4:
            snap_id = st.text_input("👻 Snapchat ID", placeholder="snap_username")
        st.caption("😎 Double apps, double fun!")
    
    elif platform == "🙈 None (I’m mysterious)":
        st.caption("So… where do you spend most of your screen time? 😜 ")


    gender = st.selectbox("🚻 Gender", ["Male", "Female", "Other"])
    city = st.text_input("🏙️ City")
    dob = st.date_input("📅 Date of Birth", max_value=date.today())

    # ---------- EXTRA FUN INFO (AFTER INSTAGRAM) ----------
if insta_id.strip() != "":
    st.markdown("### 🎬 Just for Fun 😄")

    # 🎥 Movie Type
    movie_type = st.selectbox(
        "🎥 What kind of movies do you like?",
        ["Action 💥", "Comedy 😂", "Romantic ❤️", "Horror 😱", "Sci-Fi 🚀"]
    )

    movie_reaction = {
        "Action 💥": "🔥 Full power! Slow movies not allowed 😎",
        "Comedy 😂": "😂 Laughter is mandatory, stress is banned!",
        "Romantic ❤️": "❤️ Ohooo… emotions unlocked 😉",
        "Horror 😱": "😱 Brave soul! Lights ON only 😜",
        "Sci-Fi 🚀": "🚀 Brainy choice! Multiverse approved 🤯"
    }
    st.caption(movie_reaction[movie_type])

    # 👯 Best Friend
    best_friend = st.text_input("👯 Your best friend’s name")

    if best_friend.strip() != "":
        st.caption(f"🤝 {best_friend} is officially certified as your partner-in-crime 😄")

    # 💍 Engagement Status
    engaged = st.radio(
        "💍 Relationship status (don’t panic 😜)",
        ["😅 Single", "❤️ Engaged", "🤫 It’s complicated"]
    )

    if engaged == "😅 Single":
        st.caption("😎 Single = peaceful + extra freedom!")
    elif engaged == "❤️ Engaged":
        st.caption("💖 Congratulations! Wedding reels incoming 😂")
    else:
        st.caption("🤫 Complicated huh… system will not ask further questions 😜")

    if st.button("📡 Send Data"):
        if name == "" or not mobile.isdigit() or len(mobile) != 10:
            st.error("❌ Invalid details")
        elif mobile in data["Mobile"].astype(str).values:
            st.error("❌ Mobile already exists")
        else:
            age = relativedelta(date.today(), dob).years
            new_id = 1 if data.empty else int(data["ID"].max()) + 1

            data.loc[len(data)] = [
                new_id, name, mobile, insta_id, snap_id,
                gender, city, dob.strftime("%Y-%m-%d"), age
            ]
            data.to_csv(CSV_FILE, index=False)

            st.session_state.step = "success"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# =================================================
# ✅ SUCCESS PAGE
# =================================================
elif st.session_state.step == "success":
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    st.success("💾 Data saved successfully!")
    st.balloons()

    if st.button("➕ Add Another User"):
        st.session_state.step = "form"
        st.rerun()

    if st.button("🏠 Go Home"):
        st.session_state.step = "home"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# =================================================
# 🔐 ADMIN LOGIN PAGE (SEPARATE)
# =================================================
elif st.session_state.step == "admin_login":
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    st.header("🔐 Admin Login")
    password = st.text_input("Enter Admin Password", type="password")

    if st.button("🔓 Login"):
        if password == ADMIN_PASSWORD:
            st.session_state.admin_logged_in = True
            st.session_state.step = "admin_panel"
            st.rerun()
        else:
            st.error("❌ Wrong Password")

    if st.button("⬅ Back"):
        st.session_state.step = "home"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# =================================================
# 🛠️ ADMIN PANEL PAGE (COMPLETELY SEPARATE)
# =================================================
elif st.session_state.step == "admin_panel" and st.session_state.admin_logged_in:
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    st.success("✅ Admin Access Granted")
    st.subheader("📊 Stored Records")
    st.dataframe(data, use_container_width=True)

    st.subheader("🗑️ Delete User")
    delete_id = st.number_input("User ID", min_value=1, step=1)

    if delete_id in data["ID"].values:
        if st.button("❌ Confirm Delete"):
            data = data[data["ID"] != delete_id]
            data.to_csv(CSV_FILE, index=False)
            st.success("User deleted")
            st.rerun()

    st.subheader("📈 Age Analytics")
    if not data.empty:
        fig, ax = plt.subplots()
        ax.hist(data["Age"], bins=10)
        st.pyplot(fig)

    if st.button("🚪 Logout Admin"):
        st.session_state.admin_logged_in = False
        st.session_state.step = "home"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("🔒 Admin-protected system | Separate Admin Page | Streamlit App")
