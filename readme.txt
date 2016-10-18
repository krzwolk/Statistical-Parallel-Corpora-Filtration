Installation
1. Install MongoDB as described here: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/

2. Install latest version of Python 3

3. Install MongoDB library for Python:
pip install pymongo

4. Get a phrase table with translation from some language into English (e.g. Czech to English) and load it to MongoDB using phrases_to_mongo.py script:
python phrases_to_mongo.py phrase-table.17 cs_en 
(where "phrase-table.17" is a phrase table file, "cs_en" is a collection name in MongoDB; for another pair of languages collection name should be changed, e.g. for Russian to English it should be ru_en)

5. Now everything is ready to filter a parallel corpus:
python main.py Wikipedia.cs-en.cs Wikipedia.cs-en.en data/output
where "Wikipedia.cs-en.cs" and "Wikipedia.cs-en.en" are files containing a parallel corpus and "data/output" is a directory where output files should be saved. Extensions of input files should indicate their languages: ".cs" for Czech, ".en" for English and so on.

To add another language repeat step 4 with a file containing this language and English phrases. The tool converts everything to English before calculating Levenstein distance. 
For example, if files cz_en and ru_en are loaded into the database, the tool will be able to compare the following parallel corpora: cz_en, ru_en, ru_cz. Then, if the corpus pl_en added, the tool will be able to filter the following pairs: cz_en, ru_en, pl_en, ru_cz, ru_pl, pl_cz, and so on. Note, that adding specific corpora like ru_cz, ru_pl, and pl_cz is not needed, everything works through transforming input data into English.