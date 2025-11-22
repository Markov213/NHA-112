import streamlit as st
import pandas as pd
import os

# ============================================================
# ELT NEW DATA
# ============================================================
new_data_path = os.path.join(
    os.path.dirname(__file__),
    "../data/new/new_data.csv"
)
# ============================================================
# STREAMLIT CONFIG
# ============================================================
st.set_page_config(
    page_title="Citizens Issues Submission",
    layout="wide",
    page_icon="📝"
)

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
with st.form("client_form"):
    name = st.text_input("Client Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    comment = st.text_area("Describe the problem in detail")

    submitted = st.form_submit_button("Submit")

# ============================================================
# HANDLE FORM SUBMISSION
# ============================================================
if submitted:

    # Store form data
    st.session_state['Citizen'] = [name, email, phone, comment]
    st.toast("Form submitted successfully!", icon="✅")

    # Create a dictionary for new data
    new_data = {"Name": name, "Email": email,"Phone": phone, "Comment": comment}

    # Then we check that if the file exists, if it does we read it, if not we create a new df to store data
    if os.path.exists(new_data_path) and os.path.getsize(new_data_path) > 0:
        df = pd.read_csv(new_data_path)
    else:
        df = pd.DataFrame(columns=["Name", "Email", "Phone", "Comment"])

    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    df.to_csv(new_data_path, index=False)

    
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


