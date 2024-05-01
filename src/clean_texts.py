from functools import partial
from pathlib import Path
from typing import Optional

import dacy
import pandas as pd
from spacy.tokens import Doc
from tqdm import tqdm


def clean_doc(doc: Doc, extra_stopwords: Optional[set[str]] = None) -> str:
    """Outputs clean string based on SpaCy doc."""
    if extra_stopwords is None:
        extra_stopwords = set()
    lemmata = []
    for token in doc:
        if not token.is_stop and token.is_alpha and token.lower_ not in extra_stopwords:
            lemmata.append(token.lemma_.lower())
    return " ".join(lemmata)


def main():
    print("Collecting stop words.")
    with open("dataset/Stopord.txt", encoding="iso-8859-1") as in_file:
        custom_stop_words = set(in_file)
        custom_stop_words = {stop.strip() for stop in custom_stop_words}

    print("Collecting all text files.")
    files = Path("dataset/data").glob("*.txt")
    texts = []
    ids = []
    for file in files:
        with file.open("r", encoding="utf-8") as in_file:
            texts.append(in_file.read())
            ids.append(file.stem)

    nlp = dacy.load("small")
    progress = tqdm(texts, desc="Processing all texts with DaCy.")
    docs = nlp.pipe(progress)
    clean_texts = map(partial(clean_doc, extra_stopwords=custom_stop_words), docs)
    clean_texts = list(clean_texts)

    print("Saving clean texts.")
    data = pd.DataFrame({"id": ids, "text": texts, "clean_text": clean_texts})
    data.to_csv("dataset/clean_data.csv")


if __name__ == "__main__":
    main()
