import os
from llama_index.llms.groq import Groq
import streamlit as st

def chat_qa():
    llama_api_key = os.getenv("LLAMA_API_KEY")
    # Initialize the LLM
    llm = Groq(model="Llama3-8b-8192", api_key=llama_api_key, temperature=0.7)
    
    # Hardcoded prompt for initialization
    #promt = "What is Generative AI? give one sentence"
    
    # Display the title
    st.title(f"**My AI :green[Chatbot]** :sparkles:")  # Add emojis and colors to the title
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # React to user input
    if prompt := st.chat_input("Ask any question here!"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Generate the assistant's response using the user's prompt instead of hardcoded promt
        response = llm.complete(prompt)  # Replacing promt with prompt
        
        # Display assistant's response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        
        # Add assistant's response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

chat_qa()
