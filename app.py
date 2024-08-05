import os
import streamlit as st
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain_openai import ChatOpenAI
from read_files import read_files

load_dotenv()

# Define templates
template_with_context_and_ai_agents = """
        Act as an experienced maintenance specialist of industrial products who has the task of answering maintenance
        questions based on provided maintenance documents. The document provided contains some information about 
        maintenance and troubleshooting, as well as further technical reference. Note that the original tables 
        in the document have now been converted into text. At the end of the document you will find a table with 
        sensor data for the sensor Pt100.

        Your task is now to answer the following question of the user, always answer in a structured way in enumerated steps. 
        The answer must always come directly from the document provided below. If you cannot find the answer in the document, 
        just return "I do not find the answer."

        {context}

        "This is the data table for sensor Pt100"
        
        {sensor_data}
        
        Question: {question}

        Useful Answer:
"""

template_with_context = """
        Act as an experienced maintenance specialist of industrial products who has the task of answering maintenance 
        questions based on provided maintenance documents. The document provided contains some information about maintenance 
        and troubleshooting, as well as further technical reference. Note that the original tables in the document have now
        been converted into text. At the end of the document you will find a table with sensor data for the sensor Pt100.
        
        Your task is now to answer the following question of the user, always answer in a structured way in enumerated steps. 
        The answer must always come directly from the document provided below. If you cannot find the answer in the document, 
        just return "I do not find the answer."

        {context}

        Question: {question}

        Useful Answer:
"""

# Create PromptTemplates
custom_rag_prompt_with_context_and_ai_agents = PromptTemplate.from_template(template_with_context_and_ai_agents)
custom_rag_prompt_with_context = PromptTemplate.from_template(template_with_context)

# Initialize LLM
llm = ChatOpenAI(
    model='deepseek-chat', 
    openai_api_key=os.getenv('DEEPSEEK_API_KEY'), 
    openai_api_base='https://api.deepseek.com/beta',
    max_tokens=8192, # 8192 4096
    temperature=0.0,
)

# Read documents
retrieved_doc = read_files("data/extracted_pages.md")
sensor_data = read_files("data/Realistic_Pt100_Sensor_Data.txt")

def main():
    st.set_page_config(page_title="Maintenance Chatbot", layout="centered")
    st.title("Maintenance Chatbot")

    # Sidebar for mode selection
    mode = st.sidebar.selectbox("Select Mode", ["LLM", "LLM with context", "LLM with context and AI agents"])

    if "message" not in st.session_state:
        st.session_state.message = []

    for message in st.session_state.message:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Please enter a question."):
        st.session_state.message.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if mode == "LLM":
                response = st.write_stream(llm.stream(prompt))
            elif mode == "LLM with context":
                rag_chain = (
                    {"context": lambda x: retrieved_doc, "question": RunnablePassthrough()}
                    | custom_rag_prompt_with_context
                    | llm
                )
                response = st.write_stream(rag_chain.stream(prompt))
            elif mode == "LLM with context and AI agents":
                rag_chain = (
                    {"context": lambda x: retrieved_doc, "sensor_data": lambda x: sensor_data, "question": RunnablePassthrough()}
                    | custom_rag_prompt_with_context_and_ai_agents
                    | llm
                )
                response = st.write_stream(rag_chain.stream(prompt))
        
        st.session_state.message.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
