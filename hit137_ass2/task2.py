from transformers import AutoTokenizer, AutoModel

# Specify the BioBERT model name
model_name = 'dmis-lab/biobert-base-cased-v1.1'

# Step 1: Initialize and download the tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Step 2: Initialize and download the model
model = AutoModel.from_pretrained(model_name)

print("BioBERT model and tokenizer have been successfully downloaded.")
