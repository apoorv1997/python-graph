from collections import Counter
from extract import extract_text, remove_header, remove_speaker
from preproc import remove_stopwords, split_sentences, tokenize


def utility():
    text = extract_text("text.pdf")
    text = remove_header(text)
    text = remove_speaker(text)
    listStr = split_sentences(text)
    # print(listStr)
    mainTokenList = []
    for sentence in listStr:
        tokens = tokenize(sentence)
        tokens = remove_stopwords(tokens)
        # print(tokens)
        if tokens != []:
            mainTokenList.append(tokens)

    # print(mainTokenList)
    counterList = []
    for tokenList in mainTokenList:
        counter = Counter(tokenList)
        counterList.append(counter)

    return counterList