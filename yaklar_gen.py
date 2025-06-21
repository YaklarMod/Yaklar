import streamlit as st

st.set_page_config(page_title="מחולל הודעות", layout="centered")

# RTL styling
st.markdown(
    """
    <style>
    body, .stTextInput, .stTextArea, .stButton {
        direction: rtl;
        text-align: right;
        font-family: Arial, sans-serif;
    }
    .css-1cpxqw2 {
        direction: rtl !important;
        text-align: right !important;
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

    # איש קשר line
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

        st.markdown(
            f"""
            <button onclick="navigator.clipboard.writeText(`{message}`)" 
                    style="margin-top:10px; padding:10px; font-size:16px;">
                📋 העתק ללוח
            </button>
            """,
            unsafe_allow_html=True
        )
