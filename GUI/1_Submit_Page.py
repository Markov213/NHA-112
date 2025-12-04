import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os

# ============================================================
# STREAMLIT CONFIG
# ============================================================
st.set_page_config(
    page_title="Citizens Issues Submission",
    layout="wide",
    page_icon="📝"
)

# ============================================================
# GOOGLE SHEETS AUTHENTICATION (PORTABLE)
# ============================================================
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Path relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
creds_path = os.path.join(BASE_DIR, "credentials.json")  # Put your credentials.json here

try:
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)

    # Open the Google Sheet
    SHEET_NAME = "citizen_issues"  # Change if needed
    sheet = client.open(SHEET_NAME).sheet1

except Exception as e:
    st.error("❌ Google Sheets authentication failed. Check your credentials.json or API permissions.")
    st.error(str(e))
    st.stop()  # Stop execution if credentials fail

# ============================================================
# BACKGROUND CSS
# ============================================================
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://www.tripsavvy.com/thmb/-tzBp8Gy4A2v7-XK07TYecZXWfk=/2286x1311/filters:fill(auto,1)/GettyImages-200478089-001-06db86e7b540494a807a46af6c6c7f11.jpg");
    background-size: cover;
    animation: moveBackground 120s linear infinite alternate;
}
@keyframes moveBackground {
    0% { background-position: 0 0; }
    100% { background-position: 100% 0; }
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# ============================================================
# PAGE TITLE
# ============================================================
st.title("Citizen Issues Submission")

# ============================================================
# FORM
# ============================================================
with st.form("citizen_form"):
    name = st.text_input("Client Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    comment = st.text_area("Describe the problem in detail")
    submitted = st.form_submit_button("Submit")

# ============================================================
# HANDLE FORM SUBMISSION
# ============================================================
if submitted:
    # Validation
    if not name or not email or not comment:
        st.error("Please fill in all required fields.")
    else:
        # Save to session_state
        st.session_state['Citizen'] = [name, email, phone, comment]

        # Prepare row for Google Sheets
        row = [name, email, phone, comment, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]

        # Save to Google Sheets with error handling
        try:
            sheet.append_row(row)
            st.toast("Form saved successfully!", icon="💾")
        except Exception as e:
            st.error("Failed to save to Google Sheets. Please try again.")
            st.write(e)

# ============================================================
# FEEDBACK SECTION
# ============================================================
st.markdown("---")
col1, col2, col3 = st.columns([2, 2, 1])
with col2:
    st.markdown("###### Was this submission helpful?")

col1, col2, col3, g, t = st.columns([2, 3, 1, 3, 2])
with col3:
    selected = st.feedback("thumbs")
