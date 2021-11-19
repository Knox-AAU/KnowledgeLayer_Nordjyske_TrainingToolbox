# KL_NJ_TrainingToolbox
Toolbox for creating training data for training spacy models.

## Traning toolboks
[Link to repo](https://github.com/Knox-AAU/KL_NJ_TrainingToolbox)

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

The scraper will per default scrape one page with 25 articles of each topic on all sites. In total:  7+42*25 = 1225 articles per page

To run the scraper, run main.py with scrape as argument:
```
python3 main.py scrape *number of page to scrape*(default=1)
```

The output of the scraper is a .txt file with line separated text. The file will be placed in the root folder with name "ScrapeData.txt"



### Auto annotator
The auto annotator uses the default danish Spacy model. The Auto annotator is meant to be used in conjunction with [Doccano](https://github.com/doccano/doccano).

After scraping, the auto annotator can be used on the scraped data to auto annotate the text and output it in a format that can be understood by Doccano. this is done in order to minimise the work of labelling words, so that only the new labels is needs to be labelled.

If not specified the annotator will use the output from the scraper.
Run the annotator with:
```
python3 main.py annotate "file path(default="ScrapeData.txt")"
```
The annotator outputs a jsonl file to the root folder called "autoAnnotated.jsonl"

### Scrambler
The scrambler takes a file and scramble the lines in the files

Per default the scrambler will use the output from the annotator called "autoAnnotated.jsonl"
Run the scrambler with:
```
python3 main.py scramble "file path(default="autoAnnotated.jsonl")"
```
The scrambler outputs a file in josnl format called "autoAnnotated_scrambled.jsonl"

### Converters
The converter is used to convert data from a JSONL(doccano) format into a JSON(SpaCy) format and then seperate that data into two sets of data. One for the training and one for verification. It will be exactly 70\% training data and 30\% verification data. Additionally it strips annotations for white-spaces and corrects the label spans.

You can run the converter by the following command:
```
python3 main.py convert "file path(default="autoAnnotated_scrambled.jsonl") new file path(default=converted.json)"
```
