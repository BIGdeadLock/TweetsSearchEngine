from reader import ReadFile
from parser_module import Parse
import pandas as pd
import string

preprocessed_file = "model/preprocessed_supervised.txt"
corpus_path = r"C:\Users\Owner\Desktop\SearchEngine\Data"
reader = ReadFile(corpus_path)
parser = Parse()
#documents_list = reader.read_file("covid19_08-05.snappy.parquet")

documents_list = []
# files_to_process = [
#     r"C:\Users\Owner\Desktop\SearchEngine\Data\date=07-08-2020\covid19_07-08.snappy.parquet",
#     r"C:\Users\Owner\Desktop\SearchEngine\Data\date=07-09-2020\covid19_07-09.snappy.parquet",
#     r"C:\Users\Owner\Desktop\SearchEngine\Data\date=07-10-2020\covid19_07-10.snappy.parquet",
#     r"C:\Users\Owner\Desktop\SearchEngine\Data\date=07-11-2020\covid19_07-11.snappy.parquet",
#     r"C:\Users\Owner\Desktop\SearchEngine\Data\date=07-12-2020\covid19_07-12.snappy.parquet",
#     r"C:\Users\Owner\Desktop\SearchEngine\Data\date=07-13-2020\covid19_07-13.snappy.parquet",
#     r"C:\Users\Owner\Desktop\SearchEngine\Data\date=07-15-2020\covid19_07-15.snappy.parquet",
#     r"C:\Users\Owner\Desktop\SearchEngine\Data\date=07-16-2020\covid19_07-16.snappy.parquet",
#     r"C:\Users\Owner\Desktop\SearchEngine\Data\date=07-18-2020\covid19_07-18.snappy.parquet",
#     r"C:\Users\Owner\Desktop\SearchEngine\Data\date=07-20-2020\covid19_07-20.snappy.parquet",
#     r"C:\Users\Owner\Desktop\SearchEngine\Data\date=08-04-2020\covid19_08-04.snappy.parquet",
#     r"C:\Users\Owner\Desktop\SearchEngine\Data\date=07-27-2020\covid19_07-27.snappy.parquet",
# ]

files_to_process = [
    # r"C:\Users\Owner\Desktop\SearchEngine\Data\date=70-30-2020\covid19_08-07.snappy.parquet",
    # r"C:\Users\Owner\Desktop\SearchEngine\Data\date=08-06-2020\covid19_08-06.snappy.parquet",
    #r"C:\Users\Owner\Desktop\SearchEngine\Data\date=07-23-2020\covid19_07-23.snappy.parquet",
    r"C:\Users\Owner\Desktop\SearchEngine\Part C\data\benchmark_data_train.snappy.parquet"
]
df1 = pd.read_csv("data\\benchmark_lbls_train.csv")
df1 = df1.loc[df1['y_true'] == 1.0]
tweets = df1.tweet.tolist()
for file in files_to_process:
    documents_list += reader.read_file(file)

new_doc_list = []
for doc in documents_list:
    if int(doc[0]) in tweets:
        new_doc_list.append(doc)

with open(preprocessed_file, "a+") as f:
    for idx, document in enumerate(new_doc_list):
        # parse the document
        parsed_document = parser.parse_doc(document)
        doc = ""
        for i, word in enumerate(parsed_document.term_doc_dictionary):
            if word == "#" or "#_" in word:
                continue

            if i == len(parsed_document.term_doc_dictionary) - 1:
                doc = doc.replace('\n', "")
                doc+="\n"
                break

            doc+= f"{word} "
        try:
            f.write(doc)
        except UnicodeEncodeError:
            for char in doc:
                if char not in string.printable:
                    doc = doc.replace(char, "")

                if word == "#" or "#_" in word:
                    continue

            f.write(doc)
