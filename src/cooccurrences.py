import json
from collections import Counter
from pathlib import Path
from typing import Iterable, Optional

import numpy as np
import pandas as pd
from radicli import Arg, Radicli
from sklearn.feature_extraction.text import CountVectorizer
from tqdm import tqdm

cli = Radicli()


def iterate_contexts(
    tokens: list[str], n_context: int
) -> Iterable[tuple[str, list[str]]]:
    """Iterates over targets and context words in a document."""
    n_tokens = len(tokens)
    for i_target in range(n_tokens):
        target = tokens[i_target]
        context = []
        for i_context in range(i_target - n_context, i_target + n_context + 1):
            if (i_context > 0) and (i_context < n_tokens) and (i_context != i_target):
                context.append(tokens[i_context])
        yield target, context


def mutual_information(
    seed_word: str, texts: list[str], n_context: int = 5
) -> dict[str, float]:
    """Returns Pointwise Mutual information scores with all context words
    in the corpus."""
    # Counting total frequencies of words.
    frequencies = Counter()
    # Counting all tokens that cooccur with the target word in any context window.
    cooccurrences = Counter()
    for text in texts:
        tokens = text.split(" ")
        for target, context in iterate_contexts(tokens, n_context):
            frequencies[target] += 1
            if target == seed_word:
                cooccurrences.update(Counter(context))
    # Calculating PMI scores for each context word.
    pmi = {}
    n_total = sum(frequencies.values())
    for word in frequencies.keys():
        p_context = frequencies[word] / n_total
        p_seed = frequencies[seed_word] / n_total
        p_cooccurrence = cooccurrences[word] / n_total
        pmi[word] = np.log2(p_cooccurrence / (p_context * p_seed))
    return pmi


def select_top_k(pmi: dict[str, float], top_k: int) -> dict[str, float]:
    """Selects top ranking entries from dictionary of PMI values."""
    words, scores = zip(*pmi.items())
    words, scores = np.array(words), np.array(scores)
    top_idx = np.argpartition(-scores, top_k)[:top_k]
    sorted_top_idx = top_idx[np.argsort(-scores[top_idx])]
    return dict(zip(words[sorted_top_idx], scores[sorted_top_idx]))


@cli.command(
    "run",
    seed_word=Arg(help="Seed word to start off from."),
    group_by=Arg("--group_by", "-g", help="Metadata column to group results by."),
    out_file=Arg("--out_file", "-o", help="JSON file to output results to."),
    top_k=Arg("--top_k", "-k", help="Top K ranking coocurring words to output."),
    n_context=Arg(
        "--n_context",
        "-n",
        help="Number of context words to consider in each direction.",
    ),
)
def run(
    seed_word: str,
    group_by: Optional[str],
    out_file: str = "results/coocurrences.json",
    top_k: int = 50,
    n_context: int = 5,
):
    print("Loading data and metadata.")
    data = pd.read_csv("dataset/clean_data.csv")
    metadata = pd.read_csv(
        "dataset/metadata_nordveck.csv", encoding="iso-8859-1", sep=";"
    ).rename(columns={"ID-dok": "id"})
    data = data.merge(metadata, on="id")
    if group_by is None:
        print("Calculating top PMI context words for the whole corpus.")
        texts = data["clean_text"].tolist()
        pmi = mutual_information(seed_word, texts, n_context=n_context)
        pmi = select_top_k(pmi, top_k=top_k)
        res = pmi
    else:
        groups = list(data.groupby(group_by))
        res = {}
        for group_name, group_data in tqdm(
            groups, desc="Calculating top PMI context words for each group."
        ):
            texts = group_data["clean_text"].tolist()
            pmi = mutual_information(seed_word, texts, n_context=n_context)
            pmi = select_top_k(pmi, top_k=top_k)
            res[group_name] = pmi
    out_path = Path(out_file)
    # Creating the parent directory in case it doesn't exist.
    out_path.parent.mkdir(exist_ok=True)
    print("Saving results.")
    with out_path.open("w") as out_json:
        out_json.write(json.dumps(res, indent=2))
    print("Done.")


if __name__ == "__main__":
    cli.run()
