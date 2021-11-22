import json
import os
import random
import sys
from collections import defaultdict

import spacy

from MediaScraper.MediaScraper import scrape
from AnnotateScrambler.AnoScrambler import scramble
from Training.Training import train_model
from Visualiser import visualize_model

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


def split_data(path: str="autoAnnotated.jsonl", dest: str="./output", train_size: int = 0.66):
    data = open(path, encoding='utf8').readlines()
    train_len = int(len(data) * train_size)

    with open(f'{dest}/train.jsonl', 'w') as f:
        f.writelines(data[:train_len])

    with open(f'{dest}/dev.jsonl', 'w') as f:
        f.writelines(data[train_len:])

def convert_data(path="autoAnnotated_scrambled.jsonl", new_path="converted.json"):
    """
    Converts the doccano-formatted data to the spacy-data format.

    :param data:
    the data to be converted into training and verification data.
    The data is also corrected.
    """
    transformed_data = []

    __convert_to_json(path, new_path)

    with open(new_path, encoding='utf8') as json_file:
        annotations = json.load(json_file)
        for annotation in annotations:
            labels = annotation['label']
            if len(labels) > 0:
                entities = __correct_labels(labels, annotation)
                transformed_data.append(tuple((annotation['data'], {'entities': entities})))

    # Randomize and split into training and verification datasets
    random.shuffle(transformed_data)
    transformed_data_len = len(transformed_data)
    training_data_len = int(round(0.7 * transformed_data_len))

    with open("train.json", 'w+', encoding='utf8') as f:
        f.write(str(json.dumps(transformed_data[0:training_data_len], ensure_ascii=False)))
    with open("dev.json", 'w+', encoding='utf8') as f:
        f.write(str(json.dumps(transformed_data[training_data_len:transformed_data_len], ensure_ascii=False)))


def __correct_labels(label_list, annotation):
    """
    This function strips an annotation for white-spaces and corrects the label span

    :param label_list:
    A list of the lables from a given doccano-file.
    :param annotation:
    A single annotation as doccano-format
    :return:
    A list of the corrected entities.
    """
    return_entities = []

    # For each lable in the annotation the label is stripped of white-spaces from both sides of the sting.
    # The new span of the word is calculated and updated, and returned as en entity
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


# def __peek_next_argument(callback, arguments, options, args, index):
#     """
#     This is a generalization of a small function, that checks whether
#     an argument is a path or an option
#
#     :param callback:
#     The fucntion to be called
#     :param arguments:
#     The enumerated arguments
#     :param options:
#     The different possible options to be checked for
#     :param args:
#     The overall arguments
#     :param index:
#     The index from the outside loop
#     """
#     if len(args) == index + 1:
#         callback()
#     if args[index + 1] not in options:
#         _, parameter = next(arguments)
#         callback(parameter)
#     else:
#         callback()

def __convert_to_json(path, new_path):
    """
    Converts a jsonl file to json format

    :param path:
    The path of the .jsonl file
    :param new_path:
    The path to the .json file
    """
    with open(path, encoding='utf-8') as read_file:
        with open(new_path, 'wb') as file:
            file.write("[".encode('utf-8'))
            for line in read_file:
                file.write(line.replace("\n", ",").encode('utf-8'))

            file.seek(-1, 2)
            file.truncate()
            file.write("]".encode('utf-8'))


if __name__ == '__main__':
    args = sys.argv[1:]

    # options = ["--scape",
    #            "--scramble"]

    # Arguments for the function
    if len(args) == 0:
        print("Give arguments please")
    else:
        if args[0] == "scrape":
            scrape(int([args[1]])) if len(args) >= 2 else scrape()
        elif args[0] == "annotate":
            auto_annotate(args[1]) if len(args) == 2 else auto_annotate()
        elif args[0] == "scramble":
            scramble(args[1]) if len(args) >= 2 else scramble()
        elif args[0] == "split":
            argument_dict = dict()
            options = ['--path', '--dest', '--train_size']
            for _, arg in enumerate(args[1:]):
                if arg in options:
                    argument_dict[arg[2:]] = next(args)
            split_data(**argument_dict)
            #convert_data(args[1]) if len(args) == 2 else convert_data()
        elif args[0] == "train":
            argument_dict = dict()
            options = ['--model', '--dest', '--train', '--dev', '--config']
            for _, arg in enumerate(args[1:]):
                if arg in options:
                    argument_dict[arg[2:]] = next(args)
            train_model(**argument_dict)
        elif args[0] == "visualise":
            argument_dict = defaultdict(str)
            options = ['--models']
            if args[1] in options:
                argument_dict[args[1][2:]] = ' '.join(args[2:])
            os.system(f"streamlit run ./Visualiser/main.py {argument_dict['models']}")
