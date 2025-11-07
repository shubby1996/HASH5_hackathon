import streamlit as st
import boto3
import uuid
import requests
import json
import matplotlib.pyplot as plt
import numpy as np
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from dotenv import load_dotenv
import io

load_dotenv()

AGENT_ID = 'HSSKM4JAUB'
AGENT_ALIAS_ID = 'TSTALIASID'
REGION = 'us-west-2'
DATASTORE_ID = 'b1f04342d94dcc96c47f9528f039f5a8'

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

def search_healthlake(resource_type, params=None):
    """Search HealthLake"""
    endpoint = f"https://healthlake.{REGION}.amazonaws.com/datastore/{DATASTORE_ID}/r4/"
    session = boto3.Session(region_name=REGION)
    credentials = session.get_credentials()
    
    url = f"{endpoint}{resource_type}"
    if params:
        url += "?" + "&".join([f"{k}={v}" for k, v in params.items()])
    
    request = AWSRequest(method='GET', url=url)
    SigV4Auth(credentials, 'healthlake', REGION).add_auth(request)
    
    response = requests.get(url, headers=dict(request.headers))
    return response.json()

def extract_patient_id(text):
    """Extract patient ID from agent response"""
    import re
    # Look for UUID pattern
    pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
    matches = re.findall(pattern, text.lower())
    return matches[0] if matches else None

def get_patient_ecg_waveform(patient_id):
    """Get ECG waveform for patient"""
    waveform_obs = search_healthlake('Observation', {'patient': patient_id, 'code': '131328', '_count': '1'})
    
    if waveform_obs.get('entry'):
        obs = waveform_obs['entry'][0]['resource']
        if 'valueSampledData' in obs:
            sampled_data = obs['valueSampledData']
            data_string = sampled_data['data']
            period_ms = sampled_data['period']
            
            waveform = [float(x) for x in data_string.split()]
            time = np.arange(len(waveform)) * period_ms / 1000
            
            patient_name = obs.get('subject', {}).get('display', 'Unknown')
            return {'time': time, 'amplitude': waveform, 'patient': patient_name}
    
    return None

def plot_ecg_waveform(waveform_data):
    """Generate ECG plot"""
    fig, ax = plt.subplots(figsize=(12, 4))
    
    ax.plot(waveform_data['time'], waveform_data['amplitude'], 'b-', linewidth=1)
    ax.set_title(f"ECG Lead II - {waveform_data['patient']}", fontsize=14, fontweight='bold')
    ax.set_xlabel('Time (seconds)', fontsize=11)
    ax.set_ylabel('Amplitude (mV)', fontsize=11)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.axhline(y=0, color='r', linestyle='-', linewidth=0.5, alpha=0.5)
    
    plt.tight_layout()
    
    # Save to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    plt.close()
    
    return buf

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
if 'show_ecg' not in st.session_state:
    st.session_state.show_ecg = False
if 'current_patient_id' not in st.session_state:
    st.session_state.current_patient_id = None

# Header
st.title("🏥 HealthLake AI Assistant with ECG Visualization")
st.markdown("Ask questions about patient health data and view ECG waveforms")

# Sidebar
with st.sidebar:
    st.header("About")
    st.info("""
    This AI assistant can:
    - Search patient records
    - View medical conditions
    - Display ECG waveforms
    - Query health data
    """)
    
    st.header("Sample Questions")
    sample_questions = [
        "Show me cardiac patients",
        "List patients with ECG data",
        "Show me patient Sarah Johnson",
        "What conditions does patient 6df562fc have?",
        "Display ECG for patient 6df562fc-25a7-4e72-8753-9583e3259572"
    ]
    
    for q in sample_questions:
        if st.button(q, key=q):
            st.session_state.messages.append({"role": "user", "content": q})
            with st.spinner("Thinking..."):
                response = invoke_agent(q, st.session_state.session_id)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Check if response contains patient ID
                patient_id = extract_patient_id(response)
                if patient_id:
                    st.session_state.current_patient_id = patient_id
                    st.session_state.show_ecg = True
            st.rerun()
    
    st.divider()
    
    # ECG Controls
    st.header("ECG Visualization")
    
    if st.session_state.current_patient_id:
        st.success(f"Patient ID: {st.session_state.current_patient_id[:8]}...")
        if st.button("Show ECG Waveform"):
            st.session_state.show_ecg = True
            st.rerun()
        if st.button("Hide ECG"):
            st.session_state.show_ecg = False
            st.rerun()
    else:
        st.info("Ask about a specific patient to view their ECG")
    
    st.divider()
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.show_ecg = False
        st.session_state.current_patient_id = None
        st.rerun()

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Chat")
    
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
                
                # Check if response contains patient ID
                patient_id = extract_patient_id(response)
                if patient_id:
                    st.session_state.current_patient_id = patient_id
                    st.session_state.show_ecg = True
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

with col2:
    st.subheader("ECG Waveform")
    
    if st.session_state.show_ecg and st.session_state.current_patient_id:
        with st.spinner("Loading ECG data..."):
            waveform = get_patient_ecg_waveform(st.session_state.current_patient_id)
            
            if waveform:
                st.success(f"ECG for {waveform['patient']}")
                
                # Plot ECG
                ecg_plot = plot_ecg_waveform(waveform)
                st.image(ecg_plot, use_container_width=True)
                
                # Show stats
                st.metric("Duration", f"{max(waveform['time']):.1f} sec")
                st.metric("Samples", len(waveform['amplitude']))
                st.metric("Avg Amplitude", f"{np.mean(waveform['amplitude']):.3f} mV")
            else:
                st.warning("No ECG waveform data available for this patient")
    else:
        st.info("💡 Ask about a patient to view their ECG waveform")
        st.markdown("""
        **Try asking:**
        - "Show me patient Sarah Johnson"
        - "Display ECG for patient [ID]"
        - "List cardiac patients"
        """)
