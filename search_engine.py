import pandas as pd
from parser_module import Parse
from indexer import Indexer
from searcher import Searcher
import math
import numpy as np
import os
from reader import Reader
from configuration import ConfigClass

# DO NOT CHANGE THE CLASS NAME
class SearchEngine:

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation, but you must have a parser and an indexer.
    def __init__(self, config=None):
        self._config = config

        if self._config:
            if not hasattr(self._config, 'toStem'):
                self._config.toStem = False
            if not hasattr(self._config, 'toLemm'):
                self._config.toLemm = False

        self._parser = Parse()
        self._indexer = Indexer(config)
        self._model = {}
        self.load_precomputed_model(config.model_dir)
        self.corpus_size = 0
        self.reader = Reader(config.get_corpusPath())

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def build_index_from_parquet(self, fn):
        """
        Reads parquet file and passes it to the parser, then indexer.
        Input:
            fn - path to parquet file
        Output:
            No output, just modifies the internal _indexer object.
        """

        documents_list = self.reader.read_file(fn)
        # Iterate over every document in the file
        number_of_documents = 0
        for idx, document in enumerate(documents_list):
            # parse the document
            parsed_document = self._parser.parse_doc(document)
            number_of_documents += 1
            # index the document data
            self._indexer.add_new_doc(parsed_document)

        self._indexer.save_index(self._config.get_output_path())  # Save the inverted_index to disk
        self.corpus_size = self._indexer.get_docs_count()
        self.calculate_doc_weight()

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def load_index(self, fn):
        """
        Loads a pre-computed index (or indices) so we can answer queries.
        Input:
            fn - file name of pickled index.
        """
        self._indexer.load_index(fn)

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def load_precomputed_model(self, model_dir=None):
        """
        Loads a pre-computed model (or models) so we can answer queries.
        This is where you would load models like word2vec, LSI, LDA, etc. and
        assign to self._model, which is passed on to the searcher at query time.
        """

        model_vector_path = os.path.join(model_dir, "model.txt")

        # Load the model's embedding vectors
        # Each word is represented by a np.array
        with open(model_vector_path, 'r') as f:
            line_count = 0
            for line in f:
                if line_count == 100000:
                    break
                values = line.split(" ")
                word = values[0]

                vector = np.asarray(values[1:], "float32")
                self._model[word] = vector

                line_count += 1

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def search(self, query):
        """
        Executes a query over an existing index and returns the number of
        relevant docs and an ordered list of search results.
        Input:
            query - string.
        Output:
            A tuple containing the number of relevant search results, and
            a list of tweet_ids where the first element is the most relavant
            and the last is the least relevant result.
        """
        searcher = Searcher(self._parser, self._indexer, model=self._model)
        return searcher.search(query)

    def calculate_doc_weight(self):
        """
        The method calculates the TF-IDF for each document
        :return:
        """
        for word in self._indexer.inverted_idx:
            for doc_id in self._indexer.inverted_idx[word]['posting_list']:
                normalized_term_tf = self._indexer.inverted_idx[word]["posting_list"][doc_id][0]
                term_df = self._indexer.inverted_idx[word]['df']
                term_idf = math.log10(self.corpus_size / term_df)
                # calculate doc's total weight
                term_weight = normalized_term_tf * term_idf
                self._indexer.inverted_idx[word]["posting_list"][doc_id].append(term_weight)
                term_weight_squared = math.pow(term_weight, 2)
                self._indexer.docs_index[doc_id][0] += term_weight_squared
                self._indexer.docs_index[doc_id][0] = round(self._indexer.docs_index[doc_id][0], 3)

                self.get_doc_distance(doc_id, word)

        for doc in self._indexer.docs_index:
            self._indexer.docs_index[doc][5] = self._indexer.docs_index[doc][5] / self._indexer.docs_index[doc][2]

    def get_doc_distance(self, doc, word):
        """
        The function will calculate the document vector composed of all the words embedding.
        If the word does not recognized by the model
        :param doc: String. Tweet id - the key to the docs_index
        :param word: String. Word that lives in the document.
        :return: None
        """
        if self._indexer.docs_index[doc][5].any() and word in self._model:
            self._indexer.docs_index[doc][5] = self._indexer.docs_index[doc][5] + self._model[word]

        elif not self._indexer.docs_index[doc][5].any() and word in self._model:
            self._indexer.docs_index[doc][5] = self._model[word]

def main():
    model_dir = os.path.join('.', 'model')

    config = ConfigClass()
    if hasattr(config, 'model_dir'):
        config.model_dir = model_dir


    se = SearchEngine(config)
    se.build_index_from_parquet(r'C:\Users\Owner\Desktop\TweetsSearchEngine\training set')
    n_res, res, docs = se.search(
        'Children are “almost immune from this disease.”')

    to_return = pd.DataFrame(columns=["query", "tweet_id"])

    for r in res:
        to_return = to_return.append({"query": 5, "tweet_id": r}, ignore_index=True)
        print(r)


