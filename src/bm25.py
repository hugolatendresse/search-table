# TODO
"""
Okapi BM25 is a ranking function used by search engines to score and rank documents based on their relevance to a user's query. It is a variation of the tf-idf weighting scheme that takes into account both term frequency and document length.

The name "Okapi" comes from the Okapi Information Retrieval System, which was developed at City University, London in the 1980s. BM25 stands for "Best Match 25", which refers to the fact that the function selects the 25 best matching documents for a given query.

The Okapi BM25 function calculates a score for each document based on the following formula:

score(D,Q) = ∑(i=1 to n) IDF(qi) * ((k+1)f(qi,D))/(f(qi,D) + k(1-b+b*(|D|/avgdl)))

where:

D is a document
Q is a query
n is the number of query terms
qi is the ith query term
f(qi,D) is the frequency of the ith query term in the document D
IDF(qi) is the inverse document frequency of the ith query term
k and b are tuning parameters
|D| is the length of the document D in words
avgdl is the average document length in the corpus
The first part of the formula, IDF(qi), is the same as in the standard tf-idf weighting scheme. It measures the importance of a query term based on how often it appears in the corpus.

The second part of the formula, ((k+1)f(qi,D))/(f(qi,D) + k(1-b+b*(|D|/avgdl))), takes into account the frequency of the query term in the document and the length of the document. The parameter k controls the impact of term frequency on the score, while the parameter b controls the impact of document length on the score.

Overall, the Okapi BM25 function is a more sophisticated weighting scheme than the standard tf-idf scheme, as it takes into account both term frequency and document length. It has been shown to be effective in improving the accuracy of search results in a wide range of applications.
"""