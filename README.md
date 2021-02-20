# Tweets Search Engine
*******************************

This project includes a search engine from A to B.
The search engine includes all the components of a real search engine: inverted index, postings, parser etc.


********************************

_The search method that was used is the GloVe method_ 
The GloVe model was trained with a corpus of 10000000 tweets about Corona virus and the trained model is in the model folder.
_For more information about the GloVe model please refer to: https://github.com/stanfordnlp/GloVe

********************************

To run the search engine:
  1) In the main you can change the query that will be searched. There is a list of queries in the queries.txt file
  2) Run the main module to start the program

********************************
The merger module is implementing the BSBI algorithm to merge posting files.
It is not used in the corrent project but you can use see how it implemented and use it in your project.
_For more information about the BSBI algorithm please refer to:
https://nlp.stanford.edu/IR-book/html/htmledition/blocked-sort-based-indexing-1.html#:~:text=BSBI%20%28i%29%20segments%20the%20collection%20into%20parts%20of,the%20pairs%20in%20memory%20until%20a%20block%20
