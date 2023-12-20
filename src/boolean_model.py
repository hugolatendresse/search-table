import re

# TODO this was built by chatgpt and does not really achieve what I'm trying to do.
#  however, would be a good idea to have AND/OR/NOT implemented in final solution

class BooleanModel:
    def __init__(self, documents):
        self.documents = documents
        self.inverted_index = self.build_inverted_index(documents)

    def build_inverted_index(self, documents):
        inverted_index = {}
        for doc_id, doc in enumerate(documents):
            terms = set(re.findall(r'\w+', doc.lower()))  # Tokenize and lower-case
            for term in terms:
                if term not in inverted_index:
                    inverted_index[term] = set()
                inverted_index[term].add(doc_id)
        return inverted_index

    def search(self, query):
        tokens = re.findall(r'(\w+|AND|OR|NOT)', query.upper())
        stack = []

        for token in tokens:
            if token == "AND":
                set2 = stack.pop()
                set1 = stack.pop()
                stack.append(set1.intersection(set2))
            elif token == "OR":
                set2 = stack.pop()
                set1 = stack.pop()
                stack.append(set1.union(set2))
            elif token == "NOT":
                set1 = stack.pop()
                stack.append(set(range(len(self.documents))) - set1)
            else:
                stack.append(self.inverted_index.get(token.lower(), set()))

        return stack[0] if stack else set()

# Example usage:
documents = [
    "The sky is blue.",
    "The sun is bright.",
    "The sun in the sky is bright.",
    "We can see the shining sun, the bright sun."
]

bm = BooleanModel(documents)
query = "shining sun AND bright"
result_doc_ids = bm.search(query)

print("Matching Documents:")
for doc_id in result_doc_ids:
    print(documents[doc_id])
