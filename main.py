#main.py

import streamlit as st
from data_collection import show_data_collection_form, show_login_form
from chatbot import run_chatbot

# Custom CSS for styling
st.markdown("""
    <style>
    /* Body */
    .css-1y4n7zi {
        background-color: #f5f5f5; /* Light grey background similar to ChatGPT */
    }
    .css-1v0mbdj {
        font-family: 'Arial', sans-serif;
    }
    .css-1rf5w0f {
        background-color: #ffffff; /* White background for main content */
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    }
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #333333; /* Dark text color */
        text-align: center;
        margin-bottom: 40px;
    }
    .welcome-message {
        text-align: center;
        font-size: 20px;
        color: #cccccc;
        margin-bottom: 30px;
    }
    button[title="Login"] {
        background-color: #007bff; /* Primary button color */
        color: white;
        border: none;
        border-radius: 5px;
        padding: 12px 24px;
        font-size: 16px;
        margin: 10px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    button[title="Login"]:hover {
        background-color: #0056b3; /* Darker blue on hover */
    }
    button[title="Create Account"] {
        background-color: #007bff; /* Primary button color */
        color: white;
        border: none;
        border-radius: 5px;
        padding: 12px 24px;
        font-size: 16px;
        margin: 10px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    button[title="Create Account"]:hover {
        background-color: #0056b3; /* Darker blue on hover */
    }
    .container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 80vh;
        padding: 20px;
    }
    .button-container {
        display: flex;
        justify-content: center;
        margin-top: 30px;
    }
    </style>
""", unsafe_allow_html=True)

def navigate_to_login():
    st.session_state['page'] = 'login'

def navigate_to_create_account():
    st.session_state['page'] = 'create_account'

def main():
    # Initialize session state variables
    if 'data_collected' not in st.session_state:
        st.session_state['data_collected'] = False
    if 'user_authenticated' not in st.session_state:
        st.session_state['user_authenticated'] = False
    if 'page' not in st.session_state:
        st.session_state['page'] = 'main'  # Default to main page

    # Main Page: Display main menu with enhanced styling
    if st.session_state['page'] == 'main':
        st.markdown('<div class="title">Vehicle Diagnosis Chatbot</div>', unsafe_allow_html=True)
        st.markdown('<div class="welcome-message">Welcome to the Vehicle Diagnosis Chatbot!</div>', unsafe_allow_html=True)

        # Main content container
        col1, col2 = st.columns([1, 1])

        with st.container():
            with col1:
                st.button("Login", key="login_button", on_click=navigate_to_login, help="Log into your account", use_container_width=True)
            
            with col2:
                st.button("Create Account", key="create_account_button", on_click=navigate_to_create_account, help="Create a new account", use_container_width=True)

    elif st.session_state['page'] == 'login':
        show_login_form()
        if st.session_state['user_authenticated']:
            st.session_state['page'] = 'chatbot'

    elif st.session_state['page'] == 'create_account':
        show_data_collection_form()
        if st.session_state['data_collected']:
            st.session_state['page'] = 'chatbot'

    elif st.session_state['page'] == 'chatbot':
        run_chatbot()

if __name__ == "__main__":
    main()
