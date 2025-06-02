import streamlit as st 
from PIL import Image

img = Image.open("images/oeg.jpg")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(img, width=300)
    if st.session_state.logged_in:
        st.success("You are already logged in.")
        return

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "password":
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials. Please try again.")

def logout():
    st.session_state.logged_in = False
    st.success("You have been logged out.")
    st.rerun()

login_page = st.Page(login, title = "Login", icon="🔑")
logout_page = st.Page(logout, title = "Logout", icon="🚪")

dashboard_page = st.Page(
   "dashboard.py", 
   title="Dashboard",
   icon="📊",
   default=True
)

sample_data_page = st.Page(
    "sample_data.py", 
    title="Sample Data Generation",
    icon="📈"
    )

image_center_page = st.Page(
    "image_center.py", 
    title="Image Center",
    icon="🖼️"
)   

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Data Hub": [dashboard_page, sample_data_page, image_center_page],
            "Logout": [logout_page]
        }
    )
else:
    pg = st.navigation(
        {
            "Login": [login_page]
        }
    )
pg.run()