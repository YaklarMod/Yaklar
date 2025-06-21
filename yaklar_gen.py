import streamlit as st
import requests

# ==== CONFIGURE THIS SECTION ====
TELEGRAM_BOT_TOKEN = "7797249295:AAHNEvN-pZUbTgPF9dldvIv22f_hczsU8n0"  # ← Replace this
TELEGRAM_CHANNEL_ID = "-1002786359228"      # ← Your channel ID
# ========================

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHANNEL_ID, "text": message, "parse_mode": "HTML"}
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            return True, "✅ ההודעה נשלחה לטלגרם"
        else:
            return False, f"❌ שגיאה מטלגרם:\n{response.text}"
    except Exception as e:
        return False, f"❌ שגיאה כללית: {e}"

st.set_page_config(page_title="מחולל הודעות", layout="centered")

# RTL styling
st.markdown("""
<style>
body, .stTextInput, .stTextArea, .stButton {
    direction: rtl;
    text-align: right;
    font-family: Arial, sans-serif;
}
textarea { direction: rtl !important; text-align: right !important; }
</style>
""", unsafe_allow_html=True)

st.title("📄 מחולל הודעות תרגיל")

with st.form("message_form", clear_on_submit=False):
    st.subheader("✏️ בחר אילו שדות לכלול בהודעה")

    use_date = st.checkbox("תאריך", True)
    use_subject = st.checkbox("נושא", True)
    use_details = st.checkbox("פירוט", True)
    use_status = st.checkbox("סטטוס", True)
    use_contact_name = st.checkbox("שם איש קשר", False)
    use_contact_phone = st.checkbox("טלפון", True)
    use_contact_role = st.checkbox("תפקיד", False)

    st.divider()
    st.subheader("📥 הזנת ערכים")

    date = st.text_input("תאריך (למשל 21/06/2025):")
    subject = st.text_input("נושא:")
    details = st.text_area("פירוט:")
    status = st.text_area("סטטוס:")
    contact_name = st.text_input("שם איש קשר:")
    contact_phone = st.text_input("טלפון:")
    contact_role = st.text_input("תפקיד:")

    submit_btn = st.form_submit_button("✍️ צור הודעה")

message = ""
if submit_btn:
    lines, errors = [], []

    if use_date:
        if date: lines.append(f"תאריך {date}")
        else: errors.append("חסר תאריך")

    if use_subject:
        if subject: lines.append(f"נושא :  {subject}")
        else: errors.append("חסר נושא")

    if use_details:
        if details: lines.append(f"פירוט : {details}")
        else: errors.append("חסר פירוט")

    if use_status:
        if status: lines.append(f"סטטוס : {status}")
        else: errors.append("חסר סטטוס")

    contact_parts = []
    if use_contact_name:
        if contact_name: contact_parts.append(contact_name)
        else: errors.append("חסר שם איש קשר")
    if use_contact_phone:
        if contact_phone: contact_parts.append(contact_phone)
        else: errors.append("חסר טלפון")
    if use_contact_role:
        if contact_role: contact_parts.append(contact_role)
        else: errors.append("חסר תפקיד")

    if contact_parts:
        lines.append(f"איש קשר : {' '.join(contact_parts)}")

    if errors:
        st.warning(" | ".join(errors))
    else:
        message = "\n".join(lines)
        st.session_state['message'] = message

if 'message' in st.session_state:
    st.text_area("📋 התוצאה:", value=st.session_state['message'], height=250)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📋 העתק ללוח"):
            st.markdown(f"<script>navigator.clipboard.writeText(`{st.session_state['message']}`)</script>", unsafe_allow_html=True)
            st.success("הועתק ללוח ✅")

    with col2:
        if st.button("📤 שלח לטלגרם"):
            success, feedback = send_to_telegram(st.session_state['message'])
            if success:
                st.success(feedback)
            else:
                st.error(feedback)
