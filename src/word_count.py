import pandas as pd
from collections import Counter

def read_csv_file(filepath, text_column):
    df = pd.read_csv(filepath)
    return " ".join(df[text_column].astype(str))

def count_words(text):
    words = text.split()
    return Counter(words)

def save_word_counts_to_csv(counter, output_filepath):
    word_counts = counter.most_common()
    data = [{"Rank": rank, "Word": word, "Frequency": frequency}
            for rank, (word, frequency) in enumerate(word_counts, start=1)]
    df = pd.DataFrame(data)
    df.to_csv(output_filepath, index=False)

def main(filepath, text_column, output_filepath):
    content = read_csv_file(filepath, text_column)
    word_counter = count_words(content)
    save_word_counts_to_csv(word_counter, output_filepath)

if __name__ == "__main__":
    filepath = r"C:\Users\au546005\OneDrive - Aarhus universitet\Documents\PhD\Nordveck_project\Tools_nordveck\dataset\corrected_clean_data.csv"  # Replace with the path to your CSV file
    text_column = "clean_text"  # Replace with the name of the column containing text
    output_filepath = r"C:\Users\au546005\OneDrive - Aarhus universitet\Documents\PhD\Nordveck_project\Tools_nordveck\word-count\results\wordcount8.csv"  # Replace with the desired output file path

    main(filepath, text_column, output_filepath)
