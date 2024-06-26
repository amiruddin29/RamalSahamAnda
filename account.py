import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth

# Initialize Firebase Admin SDK if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate('ramalsahamanda-ef9e255aa6e7.json')
    firebase_admin.initialize_app(cred)

def app():
    st.title('Welcome to RamalSahamAnda')

    # Initialize session state variables
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ""
    if 'signedout' not in st.session_state:
        st.session_state.signedout = False
    if 'signout' not in st.session_state:
        st.session_state.signout = False

    # Define login and signout functions
    def login():
        try:
            user = auth.get_user_by_email(email)
            st.success('Login Successful')
            st.session_state.username = user.display_name if user.display_name else user.uid
            st.session_state.useremail = user.email
            st.session_state.signout = True
            st.session_state.signedout = True
        except Exception as e:
            st.warning(f'Login Failed: {e}')

    def signout():
        st.session_state.signout = False
        st.session_state.signedout = False
        st.session_state.username = ""
        st.session_state.useremail = ""

    # Display login/signup form or user info based on session state
    if not st.session_state.signedout:
        st.subheader('Sign Up')
        choice = st.selectbox('Choose an action', ['Sign up'])

        if choice == 'Login':
            email = st.text_input('Email Address')
            password = st.text_input('Password', type='password')
            st.button('Login', on_click=login)

        elif choice == 'Sign up':
            email = st.text_input('Email Address')
            password = st.text_input('Password', type='password')
            username = st.text_input('Enter your unique username')

            if st.button('Create my account'):
                try:
                    user = auth.create_user(email=email, password=password, display_name=username)
                    st.success('Account created successfully! Please log in.')
                    st.balloons()
                except Exception as e:
                    st.warning(f'Account creation failed: {e}')

    else:
        st.subheader('User Information')
        st.write(f"**Name:** {st.session_state.username}")
        st.write(f"**Email:** {st.session_state.useremail}")
        st.button('Sign out', on_click=signout)

# Run the application
if __name__ == "__main__":
    app()
