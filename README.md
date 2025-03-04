# word-associations
Word associations in Indre Mission and Kirkeligt Samfund.

## Usage

Folder structure:
```
- dataset/
    - data/
        - pr983_204.txt
        ...
    - Stopord.txt
    - metadata_nordveck.csv
```

Install requirements:
```bash
pip install -r requirements.txt
```

### Preprocessing

Preprocess the corpus (lemmatization, stop word removal, normalization):
```python
python3 src/clean_texts.py
```

This will output the cleaned corpus as a csv file with `id`, `text` and `clean_text` columns.
```
- dataset/
    - clean_data.csv
```

### Collect collocations

You can use the `src/cooccurrences.py run` CLI, to extract the highest scoring collocations of a target word based on PMI.

#### Arguments

| Argument                | Description                                                                                  | Type   | Default           |
|-------------------------|----------------------------------------------------------------------------------------------|--------|-------------------|
| `seed_word`             | Seed word to start off from.                                                                 | str    | -                 |
| `-h`, `--help`          | Show help message and exit.                                                             |        |                   |
| `--group_by GROUP_BY`,<br>`-g GROUP_BY` | Metadata column to group results by.                                                        | str    | None              |
| `--out_file OUT_FILE`,<br>`-o OUT_FILE` | JSON file to output results to.                                                              | str    | results/coocurrences.json |
| `--top_k TOP_K`,<br>`-k TOP_K` | Top K ranking cooccurring words to output.                                                   | int    | 50                |
| `--n_context N_CONTEXT`,<br>`-n N_CONTEXT` | Number of context words to consider in each direction.                                     | int    | 5                 |
