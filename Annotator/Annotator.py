import spacy


def auto_annotate(arg_data="ScrapeData.txt"):
    """
    Automatically annotates text in a line seperated file,
    automatically labeling the words using the specified spacy model,
    with the standards lables: ORG, LOC, PER, etc.

    :param arg_data:
    The name of the data-file (for use in the CLI)
    """
    # python -m spacy download da_core_news_lg
    nlp = spacy.load("da_core_news_lg")

    with open(arg_data, encoding='utf8') as data_file:
        lines = data_file.readlines()
        line_id = 1

        for line in lines:
            line = line.strip()
            if line:
                # "nlp" is a spacy function that tokenizes and lables the string "line"
                doc = nlp(line)
                ent_list = []
                for ent in doc.ents:
                    ent_list.append([ent.start_char, ent.end_char, ent.label_])
                # Preproccesing the text so that it can be read by the doccano-tool
                with open("autoAnnotated.jsonl", 'a', encoding='utf8') as f:
                    f.write(str('{"id":' + str(line_id) + ', "data": "' + line.replace('\n', '').replace('"', "'") +
                                '", "label": ' + str(ent_list).replace("'", '"') + '}\n'))
                line_id += 1
