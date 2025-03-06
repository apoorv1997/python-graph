"""
Preprocess the text data generated by extract.py
Created by: Haoyang Zhang (hz333)
Used in: Rutgers CS512 taught by Prof. James Abello
"""


import spacy

import loguru # for logging purposes, you can use print instead
import glob
import pathlib
import os

nlp = spacy.load("en_core_web_sm")
# add blah to stop words
nlp.Defaults.stop_words.add("blah")


def split_sentences(text):
    '''
    Split text into sentences
    IN: text: str
    OUT: sentenceList: List[str]
    '''
    doc = nlp(text)
    return [sent.text for sent in doc.sents]


def tokenize(sentence):
    '''
    Tokenize a sentence
    IN: sentence: str
    OUT: tokens: List[str]
    '''
    doc = nlp(sentence)
    return [
        token.lemma_
        for token in doc
        if not token.is_punct
        and not token.is_digit
        and not token.is_space
        and not token.like_num
    ]


def remove_stopwords(tokens):
    '''
    Remove stop words from tokens
    IN: tokens: List[str]
    OUT: tokens: List[str]
    '''
    return [token for token in tokens if not nlp.vocab[token].is_stop]


if __name__ == "__main__":
    fileList = glob.glob("./data/txt/*.txt")
    for fileName in fileList:
        baseName = pathlib.Path(fileName).stem
        # loguru.logger.info(f"Processing file: {baseName}")

        with open(fileName, "r") as f:
            lines = f.readlines()
            text = " ".join(lines)

        sentenceList = []
        sentences = split_sentences(text)
        for sentence in sentences:
            tokens = tokenize(sentence)
            # print(tokens)
            tokens = remove_stopwords(tokens)
            # print(tokens)
            sentenceList.append(tokens)

        if not os.path.exists("./data/token"):
            os.makedirs("./data/token")

        with open(f"./data/token/{baseName}.txt", "w") as f:
            for sentence in sentenceList:
                f.write(",".join(sentence))
                f.write("\n")
