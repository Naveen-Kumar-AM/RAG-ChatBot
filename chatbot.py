#chatbot.py

import streamlit as st
import time,os,dotenv,csv
from datetime import datetime
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

# Storing API Keys
dotenv.load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Function to retrieve car model based on phone number from the CSV file
def get_car_model(phone_number, file_path='mydata.csv'):
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Phone'] == phone_number:  # Assuming 'Phone' is the column for phone numbers
                return row['Vehicle_Name']  # Assuming 'Vehicle_Name' is the column for car models
    return 'N/A'  # Return 'N/A' if phone number is not found

def log_problem_to_csv(name, phone, vehicle_model, problem_description, file_path='problems_log.csv'):
    # Get the current date and time
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Get the car model using the phone number
    vehicle_model = get_car_model(phone)
    
    # Check if file already exists
    file_exists=os.path.isfile('problems_log.csv')
    
    # Open the CSV file in append mode
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header only if the file is being created for the first time
        if not file_exists:
            writer.writerow(['Time','Name', 'Phone', 'Vehicle_Name','Issues'])
        # Write a new row with the user details, problem description, and timestamp
        writer.writerow([timestamp, name, phone, vehicle_model, problem_description])

def run_chatbot():
    
    user_details = st.session_state.get('user_details', None)
    
    # Custom CSS and JavaScript for enhanced visuals and effects
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
            html, body, [class*="css"]  {
                font-family: 'Roboto', sans-serif;
                background-color: #1E1E1E;
                color: #F5F5F5;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
            }
            .stApp {
                background: linear-gradient(to bottom right, #0f0f0f, #2a2a2a);
                width: 100%;
            }
            .title-container, .welcome-container {
                position: relative;
                text-align: center;
            }
            h1 {
                color: gray;
                font-weight: 700;
                font-size: 32px;
                margin-bottom: 20px;
                white-space: nowrap;
                overflow: hidden;
                border-right: 4px solid gray;
                animation: typing 3.5s steps(40, end), fadeout 0.5s forwards 3.5s;
                display: inline-block;
                margin: 0;
            }
            .welcome-message {
                font-size: 18px;
                color: lightgray;
                margin-top: 10px;
                white-space: nowrap;
                overflow: hidden;
                border-right: 2px solid lightgray;
                animation: typing-welcome 3.5s steps(30, end), fadeout-welcome 0.5s forwards 4s;
                display: inline-block;
            }
            @keyframes typing {
                from { width: 0; }
                to { width: 100%; }
            }
            @keyframes typing-welcome {
                from { width: 0; }
                to { width: 100%; }
            }
            @keyframes fadeout {
                from { border-right-color: gray; }
                to { border-right-color: transparent; }
            }
            @keyframes fadeout-welcome {
                from { opacity: 1; }
                to { opacity: 0; }
            }
            .fadeout {
                opacity: 0;
                transition: opacity 0.5s ease-out;
            }
            .user-message {
                text-align: right;
                background-color: gray;
                color: white;
                padding: 10px;
                border-radius: 10px;
                display: inline-block;
                max-width: 60%;
            }
            .assistant-message {
                text-align: left;
                background-color: #333;
                color: white;
                padding: 10px;
                border-radius: 10px;
                display: inline-block;
                max-width: 60%;
            }
            .message-container {
                display: flex;
                flex-direction: column;
                gap: 20px;
            }
            .message-row {
                display: flex;
                justify-content: flex-start;
                align-items: center;
            }
            .message-row.user {
                justify-content: flex-end;
            }
            .assistant-label {
                font-size: 12px;
                color: gray;
                text-align: left;
                margin-bottom: 5px;
                margin-top: 5px;
            }
        </style>
        
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                const title = document.querySelector('h1');
                const welcomeMessage = document.querySelector('.welcome-message');

                title.style.width = '100%';
                welcomeMessage.style.width = '100%';

                function fadeOutWelcome() {
                    welcomeMessage.classList.add('fadeout');
                    setTimeout(() => {
                        welcomeMessage.style.display = 'none';
                    }, 500);
                }

                setTimeout(fadeOutWelcome, 4000);
            });
        </script>
    """, unsafe_allow_html=True)

    # Title of the Webpage with Typing Effect
    st.markdown("<div class='title-container'><h1>Vehicle Diagnosis Chatbot</h1></div>", unsafe_allow_html=True)

    # Welcome message that disappears after being fully typed
    st.markdown('<div class="welcome-container"><div class="welcome-message">Welcome to the Vehicle Diagnosis Chatbot</div></div>', unsafe_allow_html=True)
    
    vehicle_model = get_car_model(user_details['phone'])
    if user_details:
        st.sidebar.markdown(f'''
            <style>
                .user-icon {{
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    width: 50px;
                    height: 50px;
                    border-radius: 50%;
                    background-color: #1E1E1E;
                    color: white;
                    font-size: 20px;
                    text-align: center;
                    cursor: pointer;
                    margin-bottom: 20px; /* Add space between the icon and the following elements */
                }}
                .user-info {{
                    display: none;
                    padding: 10px;
                    border-radius: 5px;
                    background-color: #f5f5f5;
                    color: #333;
                }}
                .user-icon:hover + .user-info {{
                    display: block;
                }}
            </style>
            <div class="user-icon">
                {user_details['name'][:2].upper()}
            </div>
            <div class="user-info">
                <strong>Name:</strong> {user_details['name']}<br>
                <strong>Phone:</strong> {user_details['phone']}<br>
                <strong>Vehicle Model:</strong> {vehicle_model}<br>
            </div>
        ''', unsafe_allow_html=True)

    def get_conversational_chain():
        prompt_template = """
        You are an intelligent and conversational assistant. Engage in friendly, natural conversation when interacting with the user.

        When a user asks a specific problem-solving question related to vehicle diagnostics, refer to the context provided from the PDF.

        If a question is outside the PDF context or not related to vehicle diagnostics, respond naturally, providing the answer from your own knowledge.

        If no PDF is uploaded, and the user is asking about a vehicle problem, kindly ask them to upload the document for further assistance.

        Context:\n {context}?\n
        Question: \n{question}\n

        Answer:
        """
        model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.5, google_api_key=API_KEY)
        prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
        chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
        return chain

    def user_input_processing(user_question, api_key):
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
        new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        docs = new_db.similarity_search(user_question)
        chain = get_conversational_chain()
        response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
        return response["output_text"]

    # Updated response generator function
    def response_generator(response):
        response_text = ""
        for word in response.split():
            response_text += word + " "
            yield response_text
            time.sleep(0.1)  # Slightly increased delay for a more interactive feel

    # Function to handle response generation
    def get_response(user_input):
        # Keywords to trigger problem-solving mode
        problem_keywords = ["issue", "problem", "diagnostic", "trouble", "fault", "help", "repair", "malfunction"]
        
        # Check if the user is asking a problem-related query
        if any(keyword in user_input.lower() for keyword in problem_keywords):
            # If no PDF has been uploaded, ask the user to upload it
            if not st.session_state.get('pdf_processed', False):
                return "Please upload the PDF document so I can help you with the problem."
            else:
                if st.session_state.get('user_details'):
                    name = st.session_state['user_details']['name']
                    phone = st.session_state['user_details']['phone']
                    vehicle_model = st.session_state.get('user_vehicle_model', 'N/A')  # Fetch vehicle model from session state
                    
                    # Record the problem in CSV
                    log_problem_to_csv(name, phone, vehicle_model, user_input)
     
                # Process user input for problem-solving when PDF is uploaded
                return user_input_processing(user_input, API_KEY)
        else:
            # Handle non-problem conversations with a natural response from Gemini
            return user_input_processing(user_input, API_KEY)

    # Main application logic
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []

    def display_conversation():
        for message in st.session_state.conversation_history:
            role, content = message["role"], message["content"]
            if role == "user":
                st.markdown(f'''
                    <div class="message-row user">
                        <div class="user-message">{content}</div>
                    </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                    <div class="message-row">
                        <div class="assistant-label">Assistant</div>
                        <div class="assistant-message">{content}</div>
                    </div>
                ''', unsafe_allow_html=True)
    display_conversation()

    # Extract text from uploaded PDFs
    def get_pdf_text(pdf_file):
        text = ""
        pdf_reader = PdfReader(pdf_file)
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

    # Split the extracted text into chunks
    def get_text_chunks(text):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
        chunks = text_splitter.split_text(text)
        return chunks

    # Create and store embeddings in a vector store
    def get_vector_store(text_chunks, api_key):
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
        vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
        vector_store.save_local("faiss_index")
        return len(text_chunks), vector_store

    # PDF Analysis and State Management
    with st.sidebar:
        st.header("Upload PDF Document")
        
        pdf_file = st.file_uploader("Choose a PDF file", type="pdf", key="pdf_uploader")
        
        if pdf_file is not None and not st.session_state.get('pdf_processed', False):
            st.success("File Uploaded Successfully!")
            
            with st.spinner("Analyzing PDF..."):
                # Process PDF and store results in session state
                extracted_text = get_pdf_text(pdf_file)
                text_chunks = get_text_chunks(extracted_text)
                num_chunks, vector_store = get_vector_store(text_chunks, API_KEY)
                
                # Storing details in session state for persistence
                st.session_state['extracted_text'] = extracted_text
                st.session_state['text_chunks'] = text_chunks
                st.session_state['vector_store'] = vector_store
                st.session_state['pdf_processed'] = True
                st.session_state['pdf_analysis'] = True
                st.session_state['num_chunks'] = num_chunks
                st.session_state['vector_store_size'] = vector_store.index.ntotal
                
                #st.success("Analysis Completed! Ready to answer user queries.")
                st.success(f"**Extracted Text Length:** {len(st.session_state['extracted_text'])} characters")
                st.success(f"**Number of Chunks Created:** {st.session_state['num_chunks']}")
                st.success(f"**Vector Store Size:** {st.session_state['vector_store_size']} embeddings")
        
        # Display the stored PDF details
        if st.session_state.get('pdf_processed', False):
            st.success("Analysis Completed! Ready to answer user queries.")

        elif pdf_file is None:
            st.warning("No file uploaded yet.")

    # Handle user input
    if user_input := st.chat_input("Your Queries?"):
        st.session_state.conversation_history.append({"role": "user", "content": user_input})
        st.markdown(f'''
            <div class="message-row user">
                <div class="user-message">{user_input}</div>
            </div>
        ''', unsafe_allow_html=True)

        assistant_response = get_response(user_input)
        response_container = st.empty()
        for response_part in response_generator(assistant_response):
            response_container.markdown(f'''
                <div class="message-row">
                    <div class="assistant-label">Assistant</div>
                    <div class="assistant-message">{response_part}</div>
                </div>
            ''', unsafe_allow_html=True)
        
        st.session_state.conversation_history.append({"role": "assistant", "content": assistant_response})
