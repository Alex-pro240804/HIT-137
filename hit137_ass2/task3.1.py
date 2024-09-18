from collections import Counter
import csv

# Specify the path to the .txt file
txt_file = 'combined_text_output.txt'

# Read the text from the file
with open(txt_file, 'r') as file:
    text = file.read()

# Split the text into words (simple splitting by whitespace)
words = text.split()

# Count the occurrences of each word
word_counts = Counter(words)

# Get the top 30 most common words
top_30_words = word_counts.most_common(30)

# Save the top 30 words to a CSV file
with open('top_30_common_words.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Word', 'Count'])
    writer.writerows(top_30_words)

print("Top 30 common words have been saved to 'top_30_common_words.csv'.")
