import json
import os
import random
import sys
from collections import defaultdict
import spacy
from MediaScraper.MediaScraper import scrape
from AnnotateScrambler.AnoScrambler import scramble
from Annotator.Annotator import auto_annotate
from Training.Training import train_model, split_data
from Visualiser import visualize_model


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
            enumerator = enumerate(args[1:])
            for _, arg in enumerator:
                if arg in options:
                    argument_dict[arg[2:]] = next(enumerator)[1]
            split_data(**argument_dict)
        elif args[0] == "train":
            argument_dict = dict()
            options = ['--model', '--dest', '--train', '--dev', '--config', '--rules']
            enumerator = enumerate(args[1:])
            for _, arg in enumerator:
                if arg in options:
                    argument_dict[arg[2:]] = next(enumerator)[1]
            train_model(**argument_dict)
        elif args[0] == "visualise":
            argument_dict = defaultdict(str)
            options = ['--models']
            if len(args) > 1 and args[1] in options:
                argument_dict[args[1][2:]] = ' '.join(args[2:])
            os.system(f"streamlit run ./Visualiser/main.py {argument_dict['models']}")
