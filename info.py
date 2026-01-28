import streamlit as st
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import os
import random

# ---------------- CONFIG ----------------
st.set_page_config(page_title="ProfileBuilder 404 😅", page_icon="🧾", layout="centered")

ADMIN_PASSWORD = "jenne"
CSV_FILE = "personal_records.csv"

st.title("Fill Carefully… No Extra Sheets 😂")
st.caption("😄 Chill karo, system pe bharosa rakho")

# ---------------- LOAD / CREATE CSV ----------------
if os.path.exists(CSV_FILE):
    data = pd.read_csv(CSV_FILE)
else:
    data = pd.DataFrame(columns=[
        "ID", "Name", "Mobile", "Instagram_ID", "Snapchat_ID",
        "Gender", "City", "DOB", "Age"
    ])
    data.to_csv(CSV_FILE, index=False)

# ---------------- USER INPUT SECTION ----------------
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

# ---------------- CALCULATE & SAVE ----------------
if st.button("📡 Send Data to Server"):
    if name.strip() == "" or not mobile.isdigit() or len(mobile) != 10:
        st.error("❌ Please enter valid Name and 10-digit Mobile number")
    else:
        today = date.today()
        age_full = relativedelta(today, dob)

        years = age_full.years
        months = age_full.months
        days = age_full.days

        # Next birthday
        next_bday = dob.replace(year=today.year)
        if next_bday < today:
            next_bday = next_bday.replace(year=today.year + 1)
        days_left = (next_bday - today).days

        # Age group
        if years < 13:
            group = "🧒 Child"
        elif years < 20:
            group = "🧑 Teenager"
        elif years < 60:
            group = "🧔 Adult"
        else:
            group = "👴 Senior"

        # Save to CSV
        new_id = 1 if data.empty else int(data["ID"].max()) + 1
        new_row = {
            "ID": new_id,
            "Name": name,
            "Mobile": mobile,
            "Instagram_ID": insta_id,
            "Snapchat_ID": snap_id,
            "Gender": gender,
            "City": city,
            "DOB": dob,
            "Age": years
        }
        data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
        data.to_csv(CSV_FILE, index=False)

        # -------- INTERACTIVE OUTPUT --------
        st.markdown("---")
        st.success("💾 Data stored successfully!")
        st.info(
            "🤓 Details received successfully!\n\n"
            "Relax, this information is safer than your exam answers 😜"
        )


        st.info(
            f"""
            **👤 Name:** {name}  
            **📞 Mobile:** {mobile}  
            **📸 Instagram:** @{insta_id}  
            **👻 Snapchat:** {snap_id}  
            **🚻 Gender:** {gender}  
            **🏙️ City:** {city}  
            **🧑 Age Group:** {group}  
            **🎈 Days left for next birthday:** **{days_left} days**
            """
        )

        st.success("✅ Your details have been saved successfully!")
        st.balloons()

# ---------------- ADMIN PANEL ----------------
st.markdown("---")
st.header("🔐 Admin Panel")

password = st.text_input("Enter Admin Password", type="password")

if password == ADMIN_PASSWORD:
    st.success("✅ Admin Access Granted")

    # -------- STORED RECORDS --------
    st.subheader("📊 Stored Records")
    st.dataframe(data, use_container_width=True)

    # -------- EDIT USER DATA --------
    st.markdown("---")
    st.subheader("🗑️ Remove User (Delete Record)")
    
    delete_id = st.number_input(
        "Enter User ID to Remove",
        min_value=1,
        step=1
    )
    
    if delete_id in data["ID"].values:
        record = data[data["ID"] == delete_id].iloc[0]
    
        st.warning("⚠️ You are about to permanently delete this user:")
        st.write({
            "Name": record["Name"],
            "Mobile": record["Mobile"],
            "Instagram_ID": record["Instagram_ID"],
            "Snapchat_ID": record["Snapchat_ID"],
            "Gender": record["Gender"],
            "City": record["City"],
            "DOB": record["DOB"]
        })
    
        if st.button("❌ Confirm Delete User"):
            data = data[data["ID"] != delete_id]
            data.to_csv(CSV_FILE, index=False)
    
            st.success("✅ User removed successfully")
            st.rerun()
    else:
        st.info("ℹ️ Enter a valid User ID to remove")


    # -------- ANALYTICS DASHBOARD --------
    st.markdown("---")
    st.subheader("📈 Analytics Dashboard")

    if not data.empty:
        fig, ax = plt.subplots()
        ax.hist(data["Age"], bins=10)
        ax.set_xlabel("Age")
        ax.set_ylabel("Count")
        st.pyplot(fig)

# ❌ WRONG PASSWORD → FUNNY QUOTE
elif password != "":
    st.error("❌ Access Denied")

    funny_quotes = [
        "Ladleeeeeeeeeeeeeeee!",
        "Meowwwwwwww 🐱",
        "Ghopppp, Ghopppp, Ghopppp 😂"
    ]

    for quote in funny_quotes:
        st.markdown(
            f"""
            <div style="text-align: center; font-size: 28px; font-weight: bold; margin: 10px;">
                {quote}
            </div>
            """,
            unsafe_allow_html=True
        )



# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("🔒 Admin-protected system | Personal Info + Age | CSV backend")
