import sys

import spacy_streamlit


def visualize_model(
        models=[],
        default_models=["./output/model-last", "./output/model-best", "da_core_news_lg"]):
    spacy_streamlit.visualize(models + default_models, "Lorem Ipsum", visualizers=["ner"])


if __name__ == '__main__':
    if len(sys.argv) > 1:
        visualize_model(sys.argv[1:])
    else:
        visualize_model()
