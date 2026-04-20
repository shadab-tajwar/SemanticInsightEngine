# Semantic Insight Engine

A production-ready NLP tool designed to transform unstructured technical documentation into structured insights. 

## Overview
This engine uses a **frequency-weighted ranking algorithm** for extractive summarization and **spaCy's transformer-based models** for Named Entity Recognition (NER). It is designed to help developers and researchers quickly parse high-density text.

## Tech Stack
* **NLP Framework:** spaCy (en_core_web_md)
* **Web Interface:** Streamlit
* **Deployment:** Streamlit Cloud

## Key Features
* **Extractive Summarization:** Calculates sentence significance based on normalized word frequency.
* **NER Filtering:** Specifically tuned to extract Organizations, Products, and Technical Entities.
* **Dynamic Scaling:** User-controlled summary density via a sidebar interface.

## Engineering Reflection
During development, I utilized `en_core_web_md` over the small model to leverage **word vectors** for better semantic accuracy. One noted edge case involves scientific nomenclature (e.g., *Viridiplantae*), which highlights the potential for future implementation of a custom Knowledge Base (KB) to refine entity resolution.
