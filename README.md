# KL_NJ_TrainingToolbox
Toolbox for creating training data for training spacy models.

## Training toolboks

> Remember to install the packages listed in the requirements file and the danish spacy model

Install the danish spacy model with:
```
py -m spacy download da_core_news_lg
```

The traning toolbox is a series of "tools" that makes the process of training a spacy model easier.

The tools include a scraper, auto annotater, line scrambler and some convertes.

### Scraper

> The scraper may not work if watchmedier.dk have shut down or changed the structure of their websites.

The scraper was created to generate a lot of test/traning data fast. 
The scraper scrapes the sub sites of [watchmedier.dk](watchmedier.dk) 

These sites includes: 
mediawatch.dk, itwatch.dk, shippingwatch.dk, finanswatch.dk, medwatch.dk, energiwatch.dk, ejendomswatch.dk

Each site have between 5-8 topic sections, and each section have 25 articles.

The scraper will per default scrape one page with 25 articles of each topic on all sites. In total:  
1 as parameter * (42 topics * 25 articles) = 1050

To run the scraper, run main.py with scrape as argument:
```
python3 main.py scrape [numberOfPages]
```

numberOfPages defaults to 1 if not set. 

The output of the scraper is a .txt file with line separated text. The file will be placed in the root folder with name "ScrapeData.txt"



### Auto annotator
The auto annotator uses the default danish Spacy model. The Auto annotator is meant to be used in conjunction with [Doccano](https://github.com/doccano/doccano).

After scraping, the auto annotator can be used on the scraped data to auto annotate the text and output it in a format that can be understood by Doccano. this is done in order to minimise the work of labelling words, so that only the new labels is needs to be labelled.

If not specified the annotator will use the output from the scraper.
Run the annotator with:
```
python3 main.py annotate [filePath]
```
filePath defaults to "ScrapeData.txt" if not set.

The annotator outputs a jsonl file to the root folder called "autoAnnotated.jsonl"

### Scrambler
The scrambler takes a file and scramble the lines in the files

Per default the scrambler will use the output from the annotator called "autoAnnotated.jsonl"
Run the scrambler with:
```
python3 main.py scramble [filePath]
```
filePath defaults to "autoAnnotated.jsonl" if not set.

The scrambler outputs a file in josnl format called "autoAnnotated_scrambled.jsonl"

### Splitter
The command used to split the input dataset into a training and a dev dataset.

You can run the splitter by the following command:
```
python3 main.py split [OPTIONS]
```
```
[OPTIONS]:
--path (default="autoAnnotated.jsonl"): Filepath for the input jsonl
--dest (default="./output"): The destination folder
--train_size (default=0.66): Relative size of the training data
```

### Training a custom model
Based on the data provided by the converter, the toolbox can be used to train a custom SpaCy model.
```
python3 main.py train [OPTIONS]
```
The following options are available:
```
[OPTIONS]:
--model (default=da_core_news_lg): The base model used in the training 
    (NOT TO BE CONFUSED WITH THE MODEL PROVIDED IN THE CONFIG)
--train (default=./output/train.jsonl): Filepath to the training data
--dev (default=./output/dev.jsonl): Filepath to the dev data
--rules (default=None): Rules used for rule-based matching. If none are given, a matching step is not added.
--dest (default=./output): The output destination of the trained model
--config (default=./Training/accuracy_config.cfg): Filepath to the training configuation
```

### Visualising the model
The model can be visualised using the following command:
```
python3 main.py visualise [OPTIONS]
```
The following options are available:
```
[OPTIONS]:
--model (default=None): Additional models to visualise
```
