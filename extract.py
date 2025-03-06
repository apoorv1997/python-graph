"""
Extract text from PDF files.
Created by: Haoyang Zhang (hz333)
Used in: Rutgers CS512 taught by Prof. James Abello
"""

from pypdf import PdfReader

import re
import loguru  # for logging purposes, you can use print instead
import glob
import pathlib
import os


def extract_text(fileName):
    """
    Extract text from a PDF file, and remove any text in [] or () with trailing .
    IN: fileName: str
    OUT: text: str
    """
    reader = PdfReader(fileName)
    textList = []
    for page in reader.pages:
        text = page.extract_text()
        textList.append(text)
    text = " ".join(textList)

    # find all text in [] or () with trailing . and remove them
    pattern = r"\[.*?\]|\(.*?\)\.?"
    matched = re.findall(pattern, text)
    for match in matched:
        loguru.logger.debug(f"Matched: {match}")
        text = text.replace(match, "")
    return text


def remove_header(text):
    """
    Remove headers in the text
    IN: text: str
    OUT: text: str
    """
    # if there is any leading "StreamBox", remove it
    if text.startswith("StreamBox"):
        # loguru.logger.debug(f"Found StreamBox in the beginning")
        text = text[text.find("StreamBox") + len("StreamBox") :]

    # if there is any **********DISCLAIMER**********, find the matched end, and remove it
    if "**********DISCLAIMER**********" in text:
        # loguru.logger.debug(f"Found **********DISCLAIMER**********")
        # loguru.logger.debug(
        #     f"It contains: {text[text.find('**********DISCLAIMER**********') + len('**********DISCLAIMER**********') : text.find('**********DISCLAIMER**********', text.find('**********DISCLAIMER**********') + 1)]}"
        # )
        # find the second one
        end = text.find(
            "**********DISCLAIMER**********",
            text.find("**********DISCLAIMER**********") + 1,
        )
        text = text[end + len("**********DISCLAIMER**********") :]

    return text


def remove_speaker(text):
    """
    Remove any speaker notations in the text
    IN: text: str
    OUT: text: str
    """
    # remove any text that is in the format of ">> INSTRUCTOR: "
    pattern = r">>.*?:"
    matched = re.findall(pattern, text)
    for match in matched:
        # loguru.logger.debug(f"Matched: {match}")
        text = text.replace(match, "")
    return text


if __name__ == "__main__":
    fileList = glob.glob("./data/pdf/*.pdf")

    for fileName in fileList:
        baseName = pathlib.Path(fileName).stem
        # loguru.logger.info(f"Processing file: {baseName}")

        text = extract_text(fileName)
        text = remove_header(text)
        text = remove_speaker(text)

        if not os.path.exists("./data/txt"):
            os.makedirs("./data/txt")

        with open(f"./data/txt/{baseName}.txt", "w") as f:
            f.write(text)
