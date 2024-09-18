import pandas as pd
import os

csv_folder = '/Users/asesh/Desktop/hit137_ass2'
output_file = 'combined_text_output.txt'
all_text = []

for filename in ['CSV1.csv', 'CSV2.csv', 'CSV3.csv', 'CSV4.csv']:
    file_path = os.path.join(csv_folder, filename)
    print(f"Processing file: {filename}")
    
    try:
        df = pd.read_csv(file_path)
        print(f"Columns in {filename}: {df.columns.tolist()}")
        
        if filename == 'CSV1.csv':
            column_name = 'SHORT-TEXT'
        else:
            column_name = 'TEXT'
        
        if column_name in df.columns:
            text_data = df[column_name].dropna().tolist()
            print(f"Found {len(text_data)} lines in '{column_name}' column in {filename}.")
            all_text.extend(text_data)
        else:
            print(f"Warning: '{column_name}' column not found in {filename}")
    
    except Exception as e:
        print(f"Error reading {filename}: {e}")

if all_text:
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in all_text:
            f.write(line + '\n')
    print(f"Combined text has been saved to {output_file}.")
else:
    print("No text found to save.")