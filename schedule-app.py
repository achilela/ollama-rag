import streamlit as st
import json
from typing import Dict, List, Any
from transformers import AutoModelForCausalLM, AutoTokenizer
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

if __name__ == "__main__":
    st.set_page_config(page_title="Schedule Management App", page_icon="📅")

# Load schedule
def load_schedule() -> Dict[str, Any]:
    try:
        with open('schedule.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Schedule file not found. Please make sure 'schedule.json' exists in the same directory.")
        return {}
    except json.JSONDecodeError:
        st.error("Error decoding the schedule file. Please make sure it's valid JSON.")
        return {}

schedule = load_schedule()

# Load LLM model
@st.cache_resource
def load_llm_model():
    try:
        tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
        model = AutoModelForCausalLM.from_pretrained("distilgpt2")
        return tokenizer, model
    except Exception as e:
        st.error(f"Error loading the LLM model: {str(e)}")
        return None, None

tokenizer, model = load_llm_model()

# Load sentence transformer model
@st.cache_resource
def load_sentence_transformer():
    try:
        return SentenceTransformer('all-MiniLM-L6-v2')
    except Exception as e:
        st.error(f"Error loading the sentence transformer model: {str(e)}")
        return None

model_bert = load_sentence_transformer()

# Create FAISS index for RAG
@st.cache_resource
def create_faiss_index(schedule: Dict[str, Any]) -> faiss.IndexFlatL2:
    # Assuming model_bert.encode() returns a 768-dimensional vector, adjust if different
    index = faiss.IndexFlatL2(384)
    
    for pair, weeks in schedule.items():
        for week, days in weeks.items():
            for employee, day_list in days.items():
                embedding = model_bert.encode(f"{pair} {week} {employee} {' '.join(day_list)}")
                # Debug: Print shape to ensure it matches index dimension
                print(f"Embedding shape for {employee}: {embedding.shape}")
                if embedding.shape[0] == 384:
                    index.add(np.array([embedding]))
                else:
                    st.error(f"Dimension mismatch for {employee}. Expected 768, got {embedding.shape[0]}")
    return index

index = create_faiss_index(schedule)

# Sidebar for pair and week selection
pair = st.sidebar.selectbox("Select a Pair", list(schedule.keys()))
week = st.sidebar.selectbox("Select Week", ["Week 1", "Week 2", "Week 3", "Week 4"])

# Display selected schedule
st.write(f"Schedule for {pair} in {week}:")
for employee, days in schedule[pair][week].items():
    st.write(f"{employee}: {', '.join(days)}")

# Chat Interface
st.header("Ask about the Schedule")
user_input = st.text_input("Type your question here:")

def query_schedule(user_input: str) -> str:
    # Use RAG for retrieval
    query_embedding = model_bert.encode(user_input)
    _, I = index.search(np.array([query_embedding]), 1)
    
    # Construct context from retrieved information
    context = ""
    for idx in I[0]:
        for pair, weeks in schedule.items():
            for week, days in weeks.items():
                for employee, day_list in days.items():
                    context += f"{pair} {week} {employee}: {', '.join(day_list)}\n"
    
    # Use LLM for generating response
    prompt = f"Context:\n{context}\n\nQuestion: {user_input}\nAnswer:"
    inputs = tokenizer.encode(prompt, return_tensors='pt')
    outputs = model.generate(inputs, max_length=500, do_sample=True, top_p=0.95)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return response

if st.button("Ask"):
    if user_input:
        with st.spinner("Thinking..."):
            response = query_schedule(user_input)
            st.write(response)


    


