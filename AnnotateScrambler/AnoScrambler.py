import random


def scramble(input_file="autoAnnotated.jsonl"):
    """
    This function scrambles the lines in a text document
    (Can be removed since doccano already has a scrambler,
    if doccano is run from a common server)
    """
    with open(input_file, encoding='utf-8') as file:
        lines = file.readlines()
        random.shuffle(lines)

    with open("autoAnnotated_scrambled.jsonl", 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line)
