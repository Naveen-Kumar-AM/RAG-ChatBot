# Vehicle Diagnosis Chatbot

## Overview
This project implements a **Vehicle Diagnosis Chatbot** using **Streamlit** and **Retrieval-Augmented Generation (RAG)**, designed to collect user details, authenticate users, and provide a chatbot interface for vehicle-related queries. The application allows users to upload a PDF, and the chatbot can extract information from it to assist in vehicle diagnostics. Users can either create a new account, log in to an existing one, or interact with the chatbot for diagnosis assistance.

## Features
- **User Authentication**: Users can create an account or log in using their name and phone number.
- **Data Collection**: The application collects user information (name, phone, and vehicle model) and stores it in a CSV file.
- **Retrieval-Augmented Generation (RAG)**: The chatbot can retrieve information from uploaded PDF files to augment its responses, providing context-specific advice or guidance based on the content of the document.
- **PDF Uploading**: Users can upload a PDF related to their vehicle's manual or diagnostic report, and the chatbot can use this data for more accurate responses.
- **Profile Slider UI**: Once authenticated, users can view and edit their profile using a user-friendly slider interface.
- **Chatbot Interface**: After logging in or registering, users are redirected to a chatbot where they can ask vehicle diagnosis-related questions.

## Requirements
- Python 3.7 or higher
- Streamlit (for the UI)
- PDF extraction library 
- Large Language Model (LLM) for RAG implementation (e.g., Gemini)
- CSV (for storing user data)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Naveen-Kumar-AM/RAG-ChatBot.git

2. Navigate to the project directory:
   ```bash
   cd RAG-ChatBot

3. (Optional): Use a virtual environment to manage dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

4. Install the required packages:
   ```bash
   pip install -r requirements.txt

5. Run the application:
   ```bash
   streamlit run main.py

## How It Works

1. **User Registration and Login**:
   - The app presents options to Log In or Create an Account.
   - New users enter their details (name, phone number, vehicle model), which are validated and saved in mydata.csv.
   - Returning users log in with their name and phone number, and if authenticated, are redirected to the chatbot.

2. **Profile Slider UI**:
   - After login, users can view and edit their profile details using an interactive slider.

3. **PDF Uploading and RAG**:
   - PDF Uploading: Users can upload PDFs containing vehicle information, such as manuals or diagnostic reports.
   - Retrieval-Augmented Generation (RAG): The chatbot extracts relevant information from these PDFs to provide context-aware responses during interaction.

4. **Chatbot Interaction**:
   - After login, users are redirected to the chatbot where they can ask vehicle diagnosis questions. 
   - The chatbot leverages RAG to provide responses based on PDF content as well as general knowledge.

## Contributions & Collaboration
I’m open to collaborating on this project or exploring new ideas! If you’re interested in contributing or have a project in mind, feel free to reach out. I’m always eager to develop and learn alongside others, schedule permitting.
