#data_collection.py

import streamlit as st
import csv
import os
from datetime import datetime

#Function to create and access the csv
def excel(name, phone, vehicle_model):
        # Check if file already exists
        file_exists = os.path.isfile('mydata.csv')

        # Open file in append mode to update it without erasing past values
        with open('mydata.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            
            # Write the header only if the file is being created for the first time
            if not file_exists:
                writer.writerow(['Name', 'Phone', 'Vehicle_Name', 'Date', 'Time'])
            
            # Write the new entry along with date and time
            current_date = datetime.now().strftime('%Y-%m-%d')
            current_time = datetime.now().strftime('%H:%M:%S')
            writer.writerow([name, phone, vehicle_model, current_date, current_time])

# Function to check if phone number already exists
def phone_exists(phone):
    if os.path.isfile('mydata.csv'):
        with open('mydata.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if row[1] == phone:
                    return True
    return False

# Function to check if phone number already exists
def name_exists(name):
    if os.path.isfile('mydata.csv'):
        with open('mydata.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if row[0] == name:
                    return True
    return False

# To handle spaces
def normalize_name(name):
    return ' '.join(name.split())

def validate_name(name):
    name = normalize_name(name).strip()  # Normalize and remove leading/trailing spaces
    return all(part.isalpha() for part in name.split())

# Function to validate phone number (should be exactly 10 digits)
def validate_phone(phone):
    return phone.isdigit() and len(phone) == 10

# common_styles.py
def apply_common_css():
    st.markdown("""
        <style>
        /* General body styling */
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f5f5f5;
            color: #333;
            margin: 0;
            padding: 0;
        }

        /* Container for centering content */
        .content-container {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            height: 80vh;
            padding: 20px;
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        /* Title styling */
        h2 {
            text-align: center;
            color: #333333;
            margin-bottom: 20px;
        }

        /* Input field styling */
        input, select {
            border-radius: 5px;
            padding: 10px;
            border: 1px solid #ccc;
            width: 100%;
            margin-bottom: 10px;
        }

        /* Submit button styling */
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            width: 100%;
        }

        /* Button container styling */
        .submit-btn {
            margin-top: 20px;
        }

        /* Error message styling */
        .stError {
            color: red;
            font-size: 0.9em;
        }
        </style>
    """, unsafe_allow_html=True)


# Function to show the data collection form
def show_data_collection_form():
    
    apply_common_css()
    
    # Title
    st.markdown("<h2>Enter Your Details</h2>", unsafe_allow_html=True)

    # Directly show the form without requiring the "Enter Info" button
    with st.form(key='user_form'):
        st.markdown('<div class="form-container">', unsafe_allow_html=True)

        name = normalize_name(st.text_input("Enter your name", value="").strip())
        phone = st.text_input("Enter your phone number", value="").strip()
        
        # Dropdown for vehicle models
        vehicle_model = ['Toyota Corolla', 'Honda Civic', 'Ford Mustang', 'Chevrolet Camaro', 
                        'Tesla Model S', 'BMW 3 Series', 'Mercedes-Benz C-Class']
        
        vehicle_models = sorted(vehicle_model)
        vehicle_models.insert(0, 'Choose an Option')
        
        vehicle_model = st.selectbox("Select your vehicle model", vehicle_models)
        
        # Submit button centered
        st.markdown('<div class="submit-btn">', unsafe_allow_html=True)
        submit_button = st.form_submit_button(label="Submit")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Processing form submission with validation
    if submit_button:
        errors = False

        # Validate name (should not contain numbers)
        if not validate_name(name):
            st.error("Please enter a valid name. It should not contain numbers or symbols.")
            errors = True

        # Validate phone number (should be exactly 10 digits)
        if not validate_phone(phone):
            st.error("Please enter a valid phone number. It should contain exactly 10 digits.")
            errors = True

        # Ensure that a valid vehicle model is selected (excluding "Choose an Option")
        if vehicle_model == 'Choose an Option':
            st.error("Please select a valid vehicle model.")
            errors = True

        # Check if the phone number already exists
        if phone_exists(phone):
            st.error("This phone number is already registered. Please use a different number.")
            errors = True

        # If no errors, display success message and write data
        if not errors:
            excel(name, phone, vehicle_model)  # Insert data into the CSV
            st.success("All records inserted successfully!")  # Success message for record insertion
            st.session_state['data_collected'] = True
            st.session_state['user_details'] = {               # To ensure the details are passed to chatbot UI
                'name': name,
                'phone': phone
            }
            st.session_state['redirect'] = True
            st.success("Click Submit button once more to redirect to Chatbot.")
                
# Login form function
def show_login_form():
    
    apply_common_css()
    
    st.markdown("<h2>Login</h2>", unsafe_allow_html=True)

    with st.form(key='login_form'):
        name = st.text_input("Enter your name").strip()
        phone = st.text_input("Enter your phone number").strip()

        login_button = st.form_submit_button(label="Login")

        if login_button:
            errors = False
            
            # Check if phone number exists
            if not phone_exists(phone):
                st.error("This phone number is not registered. Please create an account first.")
                errors = True
                
            # Check if name exists
            if not name_exists(name):
                st.error("This name is not registered. Please create an account first.")
                errors = True

            if not errors:
                st.success(f"Welcome back, {name}!")
                st.session_state['logged_in'] = True
                st.session_state['user_authenticated'] = True
                st.session_state['user_details'] = {                  # To ensure the details are passed to chatbot UI
                    'name': name,
                    'phone': phone
                }
                st.session_state['redirect'] = True
                st.success("Click Submit button once more to redirect to Chatbot.")
