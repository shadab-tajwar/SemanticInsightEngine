import streamlit as st
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

# Load the model globally to cache it for performance
@st.cache_resource
def load_model():
    return spacy.load("en_core_web_md")

def run_nlp_analysis(text, summary_length=3):
    nlp = load_model()
    doc = nlp(text)
    
    keyword_tokens = [
        token.text.lower() for token in doc 
        if not token.is_stop and not token.is_punct and not token.is_space
    ]
    
    word_frequencies = {}
    for word in keyword_tokens:
        word_frequencies[word] = word_frequencies.get(word, 0) + 1
    
    sentence_scores = {}
    for sent in doc.sents:
        for word in sent:
            if word.text.lower() in word_frequencies:
                sentence_scores[sent] = sentence_scores.get(sent, 0) + word_frequencies[word.text.lower()]
                
    summary_sentences = nlargest(summary_length, sentence_scores, key=sentence_scores.get)
    summary = " ".join([s.text for s in summary_sentences])
    
    relevant_labels = {'ORG', 'PRODUCT', 'GPE', 'PERSON', 'NORP'}
    entities = [
        {"text": ent.text, "label": ent.label_} 
        for ent in doc.ents if ent.label_ in relevant_labels
    ]
    
    return summary, entities

# --- Streamlit UI ---
st.set_page_config(page_title="Semantic-Insight-Engine", layout="wide")

st.title("🔍 Semantic Insight Engine")
st.markdown("Automated Extractive Summarization & Named Entity Recognition (NER)")

with st.sidebar:
    st.header("Settings")
    sent_count = st.slider("Summary Sentence Count", 1, 10, 3)
    st.info("This engine uses a frequency-weighted scoring algorithm to identify key technical insights.")

text_input = st.text_area("Paste documentation, news, or technical text below:", height=350)

if st.button("Generate Insights"):
    if text_input.strip() == "":
        st.warning("Please enter some text to analyze.")
    else:
        with st.spinner("Analyzing text..."):
            summary, entities = run_nlp_analysis(text_input, sent_count)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📝 Extractive Summary")
                st.success(summary)
            
            with col2:
                st.subheader("🏷️ Identified Entities")
                if entities:
                    for ent in entities:
                        st.write(f"**{ent['text']}** — `{ent['label']}`")
                else:
                    st.write("No major entities identified.")
