import sys
import spacy
import streamlit as st
from spacy_streamlit import visualize_ner


def visualize_model(
        models=None,
        default_models=None):
    if models is None:
        models = []
    if default_models is None:
        default_models = ["./output/finalised-model", "./output/model-last", "./output/model-best", "da_core_news_lg"]
    spacy_model = st.sidebar.selectbox("Model name", models + default_models)
    text = st.text_area("Text to analyze", "This is a text")
    nlp = spacy.load(spacy_model)
    doc = nlp(text)
    try:
        labels = nlp.get_pipe("ner").labels + nlp.get_pipe('entity_ruler').labels
    except KeyError:
        labels = nlp.get_pipe("ner").labels
    visualize_ner(doc, labels=labels)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        visualize_model(sys.argv[1:])
    else:
        visualize_model()
