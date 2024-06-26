import streamlit as st
from streamlit_option_menu import option_menu
import firebase_admin
from firebase_admin import credentials

# Import your page modules
import home
import about
import account
import predict

# Set Streamlit page configuration
st.set_page_config(
    page_title="RamalSahamAnda",
    page_icon="🔮",
    layout="wide",
)

# Initialize Firebase Admin SDK if not already initialized
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(r"C:\Users\ASUS\stock\ramalsahamanda-ef9e255aa6e7.json")
        firebase_admin.initialize_app(cred)
        st.sidebar.success("Firebase initialized successfully")
    except Exception as e:
        st.sidebar.error(f"Failed to initialize Firebase: {e}")

# Custom CSS for enhanced styling including background image
st.markdown("""
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-image: url('https://www.w3schools.com/w3images/fjords.jpg');
        background-size: cover;
        background-attachment: fixed;
        background-color: #f4f4f9;
    }
    .sidebar .sidebar-content {
        background-color: #333;
        color: white;
    }
    .sidebar .sidebar-content a {
        color: white;
        text-decoration: none;
    }
    .sidebar .sidebar-content a:hover {
        color: #ffa;
    }
    .main .block-container {
        padding: 1rem;
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }
    .stButton>button {
        background-color: #007bff;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    </style>
    """, unsafe_allow_html=True)

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })

    def run(self):
        with st.sidebar:
            st.sidebar.image(r"c:/Users/ASUS/Pictures/Capture.JPG", use_column_width=True)
            st.sidebar.title("RamalSahamAnda")
            app = option_menu(
                menu_title="Main Menu",
                options=['E-learning', 'Stock Prediction', 'Sign Up', 'Chat'],
                icons=['book', 'graph-up', 'person', 'chat'],
                menu_icon='cast',
                default_index=0,
                orientation="vertical",
            )
            st.sidebar.markdown("---")
            st.sidebar.markdown("## Contact Us")
            st.sidebar.info("Email: A187996@siswa.ukm.edu.my")

        if app == 'Chat':
            home.app()
        elif app == 'Sign Up':
            account.app()
        elif app == 'Stock Prediction':
            predict.app()
        elif app == 'E-learning':
            about.app()

# Create an instance of MultiApp and run it
app_manager = MultiApp()
app_manager.run()
