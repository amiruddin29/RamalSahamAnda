import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, auth
from datetime import datetime

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate(r"C:\Users\ASUS\stock\ramalsahamanda-ef9e255aa6e7.json")
    firebase_admin.initialize_app(cred)

def authenticate_user():
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        try:
            user = auth.get_user_by_email(email)
            # This is a placeholder for actual password verification
            # Firebase Admin SDK doesn't support sign-in with password, so use Firebase client SDK instead
            st.session_state.user = user
            st.success("Login successful")
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Login failed: {e}")

def signout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()

def chat_app():
    st.title("Professional Chat Page")

    # Initialize Firestore
    if 'db' not in st.session_state:
        st.session_state.db = firestore.client()
    db = st.session_state.db

    # Welcome message
    st.subheader(f"Welcome, {st.session_state.user.email}!")
    if st.button('Sign out'):
        signout()

    st.write("### Post a new message")
    post = st.text_area(label=':orange[+New Post]', placeholder='Share your thoughts...', height=100, max_chars=500)

    if st.button('Post'):
        if post.strip() != '':
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data = {
                "Username": st.session_state.user.email,
                "Content": post,
                "Timestamp": timestamp
            }
            db.collection('Posts').add(data)
            st.success('Post uploaded!')
            st.experimental_rerun()
        else:
            st.warning('Post cannot be empty.')

    st.write("---")
    st.header('Recent Posts')

    # Fetch and display posts
    posts = db.collection('Posts').order_by('Timestamp', direction=firestore.Query.DESCENDING).stream()
    for post in posts:
        post_data = post.to_dict()
        st.markdown(f"**{post_data['Username']}** *{post_data['Timestamp']}*")
        st.text(post_data['Content'])
        st.write("---")

def app():
    if 'user' not in st.session_state:
        authenticate_user()
    else:
        chat_app()

# Run the application
if __name__ == "__main__":
    app()
