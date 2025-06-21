import streamlit as st
import requests

# ==== CONFIGURE THIS SECTION ====
TELEGRAM_BOT_TOKEN = "7797249295:AAHNEvN-pZUbTgPF9dldvIv22f_hczsU8n0"  # ← Replace this
TELEGRAM_CHANNEL_ID = "-100XXXXXXXXXX"      # ← Replace this once known
# =================================


def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHANNEL_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=payload)
    return response.ok


def get_chat_id():
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    try:
        response = requests.get(url)
        st.subheader("🔍 תוצאה מ-getUpdates:")
        st.json(response.json())
        st.info("🔍 שלח הודעה לערוץ ואז לחץ שוב כדי לראות את ה-ID")
    except Exception as e:
        st.error(f"שגיאה בקבלת Chat ID: {e}")



st.set_page_config(page_title="מחולל הודעות", layout="centered")

# RTL style
st.markdown(
    """
    <style>
    body, .stTextInput, .stTextArea, .stButton {
        direction: rtl;
        text-align: right;
        font-family: Arial, sans-serif;
    }
    textarea {
        direction: rtl !important;
        text-align: right !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📄 מחולל הודעות תרגיל")

st.subheader("✏️ בחר אילו שדות לכלול בהודעה")

# Field toggles
use_date = st.checkbox("תאריך", value=True)
use_subject = st.checkbox("נושא", value=True)
use_details = st.checkbox("פירוט", value=True)
use_status = st.checkbox("סטטוס", value=True)
use_contact_name = st.checkbox("שם איש קשר", value=False)
use_contact_phone = st.checkbox("טלפון", value=True)
use_contact_role = st.checkbox("תפקיד", value=False)

st.divider()
st.subheader("📥 הזנת ערכים")

# Inputs
date = st.text_input("תאריך (למשל 21/06/2025):")
subject = st.text_input("נושא:")
details = st.text_area("פירוט:")
status = st.text_area("סטטוס:")
contact_name = st.text_input("שם איש קשר:")
contact_phone = st.text_input("טלפון:")
contact_role = st.text_input("תפקיד:")

message = ""
if st.button("✍️ צור הודעה"):
    lines = []

    if use_date and date:
        lines.append(f"תאריך {date}")
    elif use_date:
        st.warning("🛑 חסר תאריך")

    if use_subject and subject:
        lines.append(f"נושא :  {subject}")
    elif use_subject:
        st.warning("🛑 חסר נושא")

    if use_details and details:
        lines.append(f"פירוט : {details}")
    elif use_details:
        st.warning("🛑 חסר פירוט")

    if use_status and status:
        lines.append(f"סטטוס : {status}")
    elif use_status:
        st.warning("🛑 חסר סטטוס")

    contact_parts = []
    if use_contact_name:
        if contact_name:
            contact_parts.append(contact_name)
        else:
            st.warning("🛑 חסר שם איש קשר")
    if use_contact_phone:
        if contact_phone:
            contact_parts.append(contact_phone)
        else:
            st.warning("🛑 חסר טלפון")
    if use_contact_role:
        if contact_role:
            contact_parts.append(contact_role)
        else:
            st.warning("🛑 חסר תפקיד")

    if contact_parts:
        lines.append(f"איש קשר : {' '.join(contact_parts)}")

    if lines:
        message = "\n".join(lines)
        st.text_area("📋 התוצאה:", value=message, height=250)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("📋 העתק ללוח"):
                st.markdown(
                    f"""
                    <script>
                    navigator.clipboard.writeText(`{message}`)
                    </script>
                    """,
                    unsafe_allow_html=True
                )
                st.success("הועתק ללוח ✅")

        with col2:
            if st.button("📤 שלח לטלגרם"):
                success = send_to_telegram(message)
                if success:
                    st.success("ההודעה נשלחה לטלגרם ✅")
                else:
                    st.error("שליחה לטלגרם נכשלה ❌")

# Optional tool: find your private channel's ID
with st.expander("🔍 לחץ כאן כדי למצוא את מזהה הערוץ שלך (לערוצים פרטיים בלבד)"):
    st.markdown("יש לשלוח הודעה לערוץ ואז ללחוץ על הכפתור:")
    if st.button("📡 קבל Chat ID"):
        get_chat_id()
