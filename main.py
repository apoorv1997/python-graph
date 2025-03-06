from pypdf import PdfReader
from collections import Counter
from extract import extract_text, remove_header, remove_speaker
from preproc import remove_stopwords, split_sentences, tokenize

def main():
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
    print(counterList)

    edgeWeightDict = {}

    for i in range(len(counterList)):
        edgeWeightDict[counterList[i].keys()] = []
        for j in range(len(counterList)):
            if i != j:
                commonwords = set(counterList[i].keys()) & set(counterList[j].keys())
                if commonwords:
                    edgeWeightDict[i].append((j, len(commonwords)))

    for key, value in edgeWeightDict.items():
        print(f"{key}: {value}")        


if __name__ == "__main__":
    # calling the main function
    main()