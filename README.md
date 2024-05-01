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

#### Pilot experiment

To find all collocations of the word `"summer"` in the whole corpus, run:

```python
python3 src/clean_texts.py run "sommer" -o "results/sommer.json"
```

#### Baseline experiment

Run baseline experiment to find collocates of the word `"evangeliet"` in the whole corpus:

```python
python3 src/clean_texts.py run "evangeliet" -o "results/baseline.json"
```

The JSON file will contain context words and their PMI scores with the target word:
```json
{
  "till\u00e6g": 11.524592765313995,
  "h\u00e6gte": 10.93963026459284,
  "udsolgt": 9.93963026459284,
  ...
}
```

#### Experiment 1:

Find collocates of `"evangeliet"` over the two publishers:

```python
python3 src/clean_texts.py run "evangeliet" -g "Udgiver" -o "results/experiment_1.json"
```

This will produce an object for each group:
```json
{
  "Indre Mission": {
    "drivelse": 10.66382068114434,
    "krybeniskjul": 10.66382068114434,
    ...
  },
  "Kirkeligt Samfund": {
    "till\u00e6g": 10.67638071343271,
    "h\u00e6gte": 10.091418212711554,
    "undervurdere": 10.091418212711554,
    ...
  }
}
```

#### Experiment 2:

Find collocates of `"evangeliet"` over time periods:

```python
python3 src/clean_texts.py run "evangeliet" -g "Periode" -o "results/experiment_2.json"
```

This will produce an object for each period.
