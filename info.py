import streamlit as st
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import os

# ---------------- CONFIG ----------------
st.set_page_config(page_title="ProfileBuilder 404 😅", page_icon="🧾", layout="centered")

ADMIN_PASSWORD = "jenne"
CSV_FILE = "personal_records.csv"

# ---------------- SESSION STATE ----------------
if "step" not in st.session_state:
    st.session_state.step = 1

# ---------------- LOAD / CREATE CSV ----------------
if os.path.exists(CSV_FILE):
    data = pd.read_csv(CSV_FILE)
else:
    data = pd.DataFrame(columns=[
        "ID", "Name", "Mobile", "Instagram_ID", "Snapchat_ID",
        "Gender", "City", "DOB", "Age"
    ])
    data.to_csv(CSV_FILE, index=False)

# ================= STEP 1 =================
if st.session_state.step == 1:
    st.title("Fill Carefully… No Extra Sheets 😂")
    st.caption("😄 Chill karo, system pe bharosa rakho")

    if st.button("🚀 Enter Website"):
        st.session_state.step = 2
        st.experimental_rerun()

# ================= STEP 2 =================
elif st.session_state.step == 2:
    st.header("📜 Website Rules & Regulations")

    st.markdown("""
    1. 👤 Users must provide **correct and genuine information**
    2. 📞 Mobile number must be **valid**
    3. ❌ Fake or duplicate entries will be deleted
    4. 🔒 Data is stored for **learning/demo purposes only**
    5. 🛑 Admin has full control over data
    """)

    agree = st.checkbox("✅ I agree to all Rules & Regulations")

    if agree and st.button("➡️ Continue"):
        st.session_state.step = 3
        st.rerun()

# ================= STEP 3 =================
elif st.session_state.step == 3:
    st.header("📝 Enter Your Details")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("👤 Name")
    with col2:
        mobile = st.text_input("📞 Mobile Number (10 digits)")

    col3, col4 = st.columns(2)
    with col3:
        insta_id = st.text_input("📸 Instagram ID")
    with col4:
        snap_id = st.text_input("👻 Snapchat ID")

    col5, col6 = st.columns(2)
    with col5:
        gender = st.selectbox("🚻 Gender", ["Male", "Female", "Other"])
    with col6:
        city = st.text_input("🏙️ City")

    dob = st.date_input(
        "📅 Date of Birth",
        min_value=date(1900, 1, 1),
        max_value=date.today()
    )

    if st.button("📡 Send Data to Server"):
        if name.strip() == "" or not mobile.isdigit() or len(mobile) != 10:
            st.error("❌ Please enter valid Name and Mobile number")
        elif mobile in data["Mobile"].astype(str).values:
            st.error("❌ This mobile number already exists!")
        else:
            today = date.today()
            years = relativedelta(today, dob).years

            new_id = 1 if data.empty else int(data["ID"].max()) + 1
            new_row = {
                "ID": new_id,
                "Name": name,
                "Mobile": mobile,
                "Instagram_ID": insta_id,
                "Snapchat_ID": snap_id,
                "Gender": gender,
                "City": city,
                "DOB": dob.strftime("%Y-%m-%d"),
                "Age": years
            }

            data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
            data.to_csv(CSV_FILE, index=False)

            st.session_state.step = 4
            st.experimental_rerun()

# ================= STEP 4 =================
elif st.session_state.step == 4:
    st.success("💾 Your information has been saved successfully!")
    st.info("🎉 Thank you for submitting your details")
    st.balloons()

    if st.button("➕ Add Another User"):
        st.session_state.step = 3
        st.experimental_rerun()

    if st.button("🏠 Go to Home"):
        st.session_state.step = 1
        st.experimental_rerun()

# ---------------- ADMIN PANEL ----------------
st.markdown("---")
st.header("🕵️ Secret Zone")

password = st.text_input("😈 Prove You're team Member", type="password")

if password == ADMIN_PASSWORD:
    st.success("✅ Admin Access Granted")

    st.subheader("📊 Stored Records")
    st.dataframe(data, use_container_width=True)

    st.markdown("---")
    st.subheader("🗑️ Remove User")

    delete_id = st.number_input("Enter User ID to Remove", min_value=1, step=1)

    if delete_id in data["ID"].values:
        record = data[data["ID"] == delete_id].iloc[0]
        st.warning("⚠️ You are about to delete:")
        st.write(record)

        if st.button("❌ Confirm Delete"):
            data = data[data["ID"] != delete_id]
            data.to_csv(CSV_FILE, index=False)
            st.success("✅ User removed successfully")
            st.experimental_rerun()
    else:
        st.info("ℹ️ Enter valid User ID")

    st.markdown("---")
    st.subheader("📈 Analytics Dashboard")

    if not data.empty:
        fig, ax = plt.subplots()
        ax.hist(data["Age"], bins=10)
        ax.set_xlabel("Age")
        ax.set_ylabel("Count")
        st.pyplot(fig)

elif password != "":
    st.error("Nice Try 😜")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("🔒 Admin-protected system | CSV backend | Streamlit App")
