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

    # insta_id = ""
    # snap_id = ""
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
    
    if insta_id and insta_id.strip():
    
        st.markdown("### 🎉 Extra Fun Section 😄")
    
        fun_col1, fun_col2 = st.columns(2)
    
        # 🎬 Movie Type
        with fun_col1:
            movie_type = st.selectbox(
                "🎬 Favorite Movie Type",
                ["Action 💥", "Comedy 😂", "Romantic ❤️", "Horror 😱", "Sci-Fi 🚀"]
            )
    
            movie_msg = {
                "Action 💥": "🔥 Full power! Hero entry guaranteed 😎",
                "Comedy 😂": "😂 Stress-free life unlocked!",
                "Romantic ❤️": "❤️ Emotions running high 😉",
                "Horror 😱": "😱 Brave choice! Lights ON please 😜",
                "Sci-Fi 🚀": "🚀 Big brain energy 🤯"
            }
            st.caption(movie_msg[movie_type])
    
        # 👯 Best Friend
        with fun_col2:
            best_friend = st.text_input("👯 Best Friend Name")
    
            if best_friend.strip():
                st.caption(f"🤝 {best_friend} = permanent support system 😄")
    
        # 💍 Engagement Status (full width)
        engaged = st.radio(
            "💍 Relationship Status (no judgement 😜)",
            ["😅 Single", "❤️ Engaged", "🤫 It’s complicated"]
        )
    
        if engaged == "😅 Single":
            st.caption("😎 Single = peace + freedom!")
        elif engaged == "❤️ Engaged":
            st.caption("💖 Congratulations! Shaadi reels loading 😂")
        else:
            st.caption("🤫 Complicated… system respects privacy 😜")

    gender = st.selectbox("🚻 Gender", ["Male", "Female", "Other"])
    city = st.text_input("🏙️ City")
    dob = st.date_input("📅 Date of Birth", max_value=date.today())



    if st.button("🔐 Lock It & Send"):
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

    st.markdown("## 🎊 DATA SAVED!!! 🎊")
    st.success("Relax 😎 the system didn’t crash this time 😂")
    # st.success("💾 Data saved successfully!")
    st.balloons()

    if st.button("👯 Add Another Friend")::
        st.session_state.step = "form"
        st.rerun()

    if st.button("🚪 Take Me Home"):
        st.session_state.step = "home"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# =================================================
# 🔐 ADMIN LOGIN PAGE (SEPARATE)
# =================================================
elif st.session_state.step == "admin_login":
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    st.header("Restricted Area ☠")
    password = st.text_input("🔐 Prove you’re the AJ 😎", type="password")

    if st.button("😎 Trust Me, I’m AJ"):
        if password == ADMIN_PASSWORD:
            st.session_state.admin_logged_in = True
            st.session_state.step = "admin_panel"
            st.rerun()
# ❌ WRONG PASSWORD → FUNNY QUOTE 
        elif password != "": 
            st.error("Nice Try AJ 😜")
            
            funny_quotes = [ 
                "Ladleeeeeeeeeeeeeee 🥴", 
                "Meowwwwwwww 🐱", 
                "Ghopppp 😵‍💫, Ghopppp 🤪, Ghopppp 🥵"
            ]
            for quote in funny_quotes:
                st.markdown(
                    f""" <div style="text-align: center; font-size: 28px; font-weight: bold; margin: 10px;">
                    {quote} 
                    </div> """,
                    unsafe_allow_html=True 
                )
    if st.button("⬅ Back"):
        st.session_state.step = "home"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# =================================================
# 🛠️ ADMIN PANEL PAGE (COMPLETELY SEPARATE)
# =================================================
elif st.session_state.step == "admin_panel" and st.session_state.admin_logged_in:
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    st.markdown("## 😎 Welcome, Boss!")
    st.success("🔓 Secret access unlocked successfully")
    st.subheader("📊 Behold… the sacred data 📂")
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

    if st.button("Nikal La**e"):
        st.session_state.admin_logged_in = False
        st.session_state.step = "home"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("🧠 SPPU brain | AJ code | 5E6N3 support ✌︎㋡ ")
