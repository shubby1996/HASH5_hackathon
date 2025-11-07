import streamlit as st
import boto3
import uuid
from dotenv import load_dotenv

load_dotenv()

AGENT_ID = 'HSSKM4JAUB'
AGENT_ALIAS_ID = 'TSTALIASID'
REGION = 'us-west-2'

def invoke_agent(prompt, session_id):
    """Invoke Bedrock Agent"""
    runtime = boto3.client('bedrock-agent-runtime', region_name=REGION)
    
    response = runtime.invoke_agent(
        agentId=AGENT_ID,
        agentAliasId=AGENT_ALIAS_ID,
        sessionId=session_id,
        inputText=prompt
    )
    
    completion = ""
    for event in response.get('completion', []):
        if 'chunk' in event:
            chunk = event['chunk']
            if 'bytes' in chunk:
                completion += chunk['bytes'].decode('utf-8')
    
    return completion

# Page config
st.set_page_config(
    page_title="HealthLake AI Assistant",
    page_icon="🏥",
    layout="wide"
)

# Initialize session state
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Header
st.title("🏥 HealthLake AI Assistant")
st.markdown("Ask questions about patient health data powered by AWS Bedrock & HealthLake")

# Sidebar
with st.sidebar:
    st.header("About")
    st.info("""
    This AI assistant can help you:
    - Search for patients
    - View medical conditions
    - Check vital signs & lab results
    - Query health records
    """)
    
    st.header("Sample Questions")
    sample_questions = [
        "Show me a list of patients",
        "What medical conditions are in the system?",
        "What vital signs are available?",
        "Find patients with COVID-19",
        "Show me lab results"
    ]
    
    for q in sample_questions:
        if st.button(q, key=q):
            st.session_state.messages.append({"role": "user", "content": q})
            with st.spinner("Thinking..."):
                response = invoke_agent(q, st.session_state.session_id)
                st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()

# Chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about patient health data..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Analyzing health data..."):
            response = invoke_agent(prompt, st.session_state.session_id)
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
