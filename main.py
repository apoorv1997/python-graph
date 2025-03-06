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

    # for i in range(len(counterList)):
    #     print(f"Counter {i}: {list(counterList[i].keys())}")
    
    edgeWeightDict = {}

    for i in range(len(counterList)):
        edgeWeightDict[i] = []
        for j in range(len(counterList)):
            if i != j:
                commonwords = set(counterList[i].keys()) & set(counterList[j].keys())
                if commonwords:
                    edgeWeightDict[i].append((j, len(commonwords)))

    for key, value in edgeWeightDict.items():
        print(f"counter {list(counterList[key].keys())}")
        for idx, words in value:
            print(f" common words with counter {list(counterList[idx].keys())}: {words}")       


if __name__ == "__main__":
    # calling the main function
    main()