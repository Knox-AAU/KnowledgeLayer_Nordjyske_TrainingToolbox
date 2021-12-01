import json

import spacy
from spacy.tokens import DocBin
from spacy.cli.train import train as spacy_train


def train_model(model: str = "da_core_news_lg",
                rules: str = None,
                train: str = "./output/train.jsonl",
                dev: str = "./output/dev.jsonl",
                dest: str = "./output",
                config: str = "./Training/accuracy_config.cfg"):
    train_destination = f'{dest}/train.spacy'
    dev_destination = f'{dest}/dev.spacy'
    print("---Converting training set to spacy binary---")
    __convert_to_spacy_binary(model, train, train_destination)
    print("---Converting dev set to spacy binary---")
    __convert_to_spacy_binary(model, dev, dev_destination)
    print("---Training spacy model---")
    spacy_train(config, dest, overrides={"paths.train": train_destination, "paths.dev": dev_destination})
    if rules is not None:
        __add_entity_ruler(rules, dest)


def __add_entity_ruler(rules, dest):
    nlp = spacy.load(f'{dest}/model-best')
    ruler = nlp.add_pipe('entity_ruler', config={"overwrite_ents": True})
    ruler.from_disk(rules)
    nlp.to_disk(f'{dest}/finalised-model')


def __convert_to_spacy_binary(base_model: str, dataset_fp: str, destination: str):
    db = DocBin()
    nlp = spacy.load(base_model)
    with open(dataset_fp, encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
                doc = nlp.make_doc(data['data'])
                ents = []
                for start, end, label in data['label']:
                    span = doc.char_span(start, end, label=label)
                    ents.append(span)
                doc.ents = ents
                db.add(doc)
            except BaseException as e:
                print(f'Skipping: {data}. Message: {e}')
    db.to_disk(destination)
    return db


def split_data(path: str="autoAnnotated.jsonl", dest: str="./output", train_size: int = 0.66):
    data = open(path, encoding='utf8').readlines()
    train_len = int(len(data) * train_size)
    with open(f'{dest}/train.jsonl', 'w', encoding='utf-8') as f:
        f.writelines(data[:train_len])
    with open(f'{dest}/dev.jsonl', 'w', encoding='utf-8') as f:
        f.writelines(data[train_len:])
