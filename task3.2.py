from transformers import AutoTokenizer
from collections import Counter
import csv

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

def tokenize_and_count(text):
    tokens = tokenizer.tokenize(text)
    return Counter(tokens)

# Initialize an empty Counter
total_token_counts = Counter()

# Read the text file in chunks
with open('combined_text_output.txt', 'r') as file:
    while True:
        text_chunk = file.read(512)  # Read in smaller chunks (max sequence length is 512)
        if not text_chunk:
            break
        chunk_token_counts = tokenize_and_count(text_chunk)
        total_token_counts.update(chunk_token_counts)

# Get the top 30 unique tokens
top_tokens = total_token_counts.most_common(30)

# Save the top 30 tokens and their counts to a CSV file
output_file = 'top_30_tokens.csv'
with open(output_file, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Token', 'Count'])
    csvwriter.writerows(top_tokens)

print(f"Top 30 tokens have been saved to {output_file}.")
