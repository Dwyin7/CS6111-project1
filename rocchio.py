import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# download 'stopwords' package
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('stopwords')


from string import punctuation
import re


class Rocchio:

    def __init__(self, relevant_docs, unrelevant_docs, query) -> None:
        """
        relevant_docs: list of str
        unrelevant_docs: list of str
        query: str
        """
        self.num_relevant_docs = len(relevant_docs)
        self.num_unrelevant_docs = len(unrelevant_docs)
        self.relevant_docs = " ".join(relevant_docs)
        self.unrelevant_docs = " ".join(unrelevant_docs)
        self.query = query
        self.vocab = None
        self.get_vocab()
        self.vec_rel = None
        self.vec_unrel = None
        self.vec_query = None
        self.get_vec()

    @staticmethod
    def tokenizer(text):
        text = text.lower()
        text = re.sub(f"[{re.escape(punctuation)}]", "", text)  # Remove punctuation
        text = re.sub("[^a-z]+", " ", text)
        res = text.split()  # Remove spaces, tabs, and new lines
        res = [word for word in res if word not in stopwords.words('english')]

        # res = word_tokenize(text)
        return res

    def get_vocab(self):
        raw_vocabs = self.relevant_docs + " " + self.unrelevant_docs + " " + self.query
        self.vocab = list(set(self.tokenizer(raw_vocabs)))

    @staticmethod
    def map_vec(vocab, tokens):
        mp = {k: 0 for k in set(vocab)}
        for t in tokens:
            mp[t] += 1
        return mp

    def get_vec(self):
        rel_docs_mp = self.map_vec(self.vocab, self.tokenizer(self.relevant_docs))
        unrel_docs_mp = self.map_vec(self.vocab, self.tokenizer(self.unrelevant_docs))
        query_mp = self.map_vec(self.vocab, self.tokenizer(self.query))
        self.vec_rel = np.array([rel_docs_mp[k] for k in self.vocab])
        self.vec_unrel = np.array([unrel_docs_mp[k] for k in self.vocab])
        self.vec_query = np.array([query_mp[k] for k in self.vocab])
        # print(self.vec_query, self.vec_unrel)

    def run(self, alpha, beta, gamma):
        # return the new query
        print(self.vocab)

        query_prev = self.vec_query
        rel = self.vec_rel
        unrel = self.vec_unrel
        query_new = (
            alpha * query_prev
            + (beta / self.num_relevant_docs) * rel
            - (gamma / self.num_unrelevant_docs) * unrel
        )

        print(query_new)
        difference = (
            query_new - query_prev
        )  # get the diff and only find the positive increase tokens
        all_new_tokens = [
            (i, diff)
            for i, diff in enumerate(difference)
            if diff > 0 and query_prev[i] == 0
        ]
        top_new_tokens = sorted(all_new_tokens, key=lambda x: x[1], reverse=True)[:2]

        res = self.query + " " + " ".join([self.vocab[i] for i, _ in top_new_tokens])
        return res
