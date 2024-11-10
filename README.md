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
- Any LLM for RAG implementation (Gemini is used here)
- CSV (for storing user data)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Naveen-Kumar-AM/RAG-Chatbot.git
