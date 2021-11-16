import random


def scramble():

    with open("autoAnnotated.jsonl", encoding='utf-8') as file:
        lines = file.readlines()
        random.shuffle(lines)

    with open("autoAnnotated_scrambled.jsonl", 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line)




if __name__ == '__main__':
    scramble()