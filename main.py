import json
import random
import spacy
from pathlib import Path


def auto_annotate():
    nlp = spacy.load("da_core_news_lg")
    with open("data.txt", encoding='utf8') as data_file:
        lines = data_file.readlines()
        line_id = 1
        for line in lines:
            line = line.strip();
            if line:
                doc = nlp(line)
                ent_list = []
                for ent in doc.ents:
                    ent_list.append([ent.start_char, ent.end_char, ent.label_])


                #{"id": ID, "data": line, "label": LABEL_LIST}
                with open("autoAnnotated.jsonl", 'a', encoding='utf8') as f:
                    f.write(str('{"id":' + str(line_id) + ', "data": "' + line.replace('\n', '').replace('"', "'") + '", "label": ' + str(ent_list).replace("'", '"') + '}\n'))

                line_id += 1


def fix_data():
    transformed_data = []
    with open("all.json", encoding='utf8') as json_file:
        annotations = json.load(json_file)
        for annotation in annotations:
            labels = annotation['label']
            if len(labels) > 0:
                entities = correct_labels(labels)
                transformed_data.append(tuple((annotation['data'], {'entities': entities})))

    # Randomize and split into training and verification datasets
    random.shuffle(transformed_data)
    transformed_data_len = len(transformed_data)
    training_data_len = int(round(0.7 * transformed_data_len))

    with open("train.json", 'w+', encoding='utf8') as f:
        f.write(str(json.dumps(transformed_data[0:training_data_len], ensure_ascii=False)))
    with open("dev.json", 'w+', encoding='utf8') as f:
        f.write(str(json.dumps(transformed_data[training_data_len:transformed_data_len], ensure_ascii=False)))


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
def correct_labels(label_list):
    return_entities = []
    for label in label_list:
        new_string: str = annotation['data'][label[0]: label[1]]
        old_length = len(new_string)

        new_string = new_string.rstrip()
        new_end_point = label[1] - (old_length - len(new_string))
        old_length = len(new_string)

        new_string = new_string.lstrip()
        new_start_point = label[0] + (old_length - len(new_string))

        return_entities.append(tuple((new_start_point, new_end_point, label[2])))
    return return_entities


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #fix_data()
    auto_annotate()
