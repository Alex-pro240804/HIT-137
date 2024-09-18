import spacy
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from collections import Counter
import time

def load_scispacy_model(model_name="en_ner_bc5cdr_md"):
    # Load SciSpacy model for detecting diseases and drugs
    print(f"Loading SciSpacy model: {model_name}...")
    nlp = spacy.load(model_name)
    nlp.max_length = 800000000  # Increase maximum text length limit
    print("SciSpacy model loaded successfully.")
    return nlp

def process_text_in_chunks(text, chunk_size=500000):
    """
    Generator to yield chunks of text.
    """
    for i in range(0, len(text), chunk_size):
        yield text[i:i + chunk_size]

def extract_entities_scispacy(text, model_name="en_ner_bc5cdr_md"):
    nlp = load_scispacy_model(model_name)
    drugs = []
    diseases = []

    start_time = time.time()
    total_length = len(text)
    chunk_size = 500000
    num_chunks = (total_length // chunk_size) + 1
    chunk_count = 0

    # Process text in chunks
    for chunk in process_text_in_chunks(text, chunk_size):
        chunk_count += 1
        print(f"Processing chunk {chunk_count}/{num_chunks} with SciSpacy...")
        chunk_start_time = time.time()
        doc = nlp(chunk)
        # Extract "CHEMICAL" for drugs and "DISEASE" for diseases
        drugs.extend([ent.text for ent in doc.ents if ent.label_ == "CHEMICAL"])
        diseases.extend([ent.text for ent in doc.ents if ent.label_ == "DISEASE"])
        
        # Estimate time remaining
        chunk_end_time = time.time()
        time_per_chunk = chunk_end_time - chunk_start_time
        remaining_chunks = num_chunks - chunk_count
        estimated_remaining_time = time_per_chunk * remaining_chunks
        print(f"Chunk {chunk_count} processed. Estimated time remaining: {estimated_remaining_time:.2f} seconds.")

    end_time = time.time()
    total_time = end_time - start_time
    print(f"Entities extracted with SciSpacy. Time taken: {total_time:.2f} seconds.")
    
    return drugs, diseases

def extract_entities_biobert(text):
    # Load BioBERT model and tokenizer from Hugging Face
    print("Loading BioBERT model...")
    biobert_model_name = "dmis-lab/biobert-base-cased-v1.1"
    tokenizer = AutoTokenizer.from_pretrained(biobert_model_name)
    model = AutoModelForTokenClassification.from_pretrained(biobert_model_name)

    # Use the NER pipeline
    ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, grouped_entities=True)
    print("BioBERT model loaded successfully.")

    start_time = time.time()
    entities = ner_pipeline(text)
    print("Text processed with BioBERT.")

    # Extract entities
    drugs = [entity['word'] for entity in entities if entity['entity_group'] == 'DRUG']
    diseases = [entity['word'] for entity in entities if entity['entity_group'] == 'DISEASE']

    end_time = time.time()
    total_time = end_time - start_time
    print(f"Entities extracted with BioBERT. Time taken: {total_time:.2f} seconds.")
    
    return drugs, diseases

def compare_entities(scispacy_entities, biobert_entities):
    # Convert lists to sets for comparison
    scispacy_set = set(scispacy_entities)
    biobert_set = set(biobert_entities)

    # Entities detected by both models
    common_entities = scispacy_set.intersection(biobert_set)
    unique_to_scispacy = scispacy_set.difference(biobert_set)
    unique_to_biobert = biobert_set.difference(scispacy_set)

    print(f"\n--- Comparison Results ---")
    print(f"Total entities detected by SciSpacy: {len(scispacy_set)}")
    print(f"Total entities detected by BioBERT: {len(biobert_set)}")
    print(f"Common entities: {len(common_entities)}")
    print(f"Unique to SciSpacy: {len(unique_to_scispacy)}")
    print(f"Unique to BioBERT: {len(unique_to_biobert)}")

    print("\nMost common entities detected by SciSpacy:")
    print(Counter(scispacy_entities).most_common(10))

    print("\nMost common entities detected by BioBERT:")
    print(Counter(biobert_entities).most_common(10))

    print("\nEntities detected by SciSpacy but not BioBERT:")
    print(unique_to_scispacy)

    print("\nEntities detected by BioBERT but not SciSpacy:")
    print(unique_to_biobert)

def medical_text_pipeline(text):
    # Step 1: Extract medical entities using SciSpacy
    drugs_scispacy, diseases_scispacy = extract_entities_scispacy(text, "en_ner_bc5cdr_md")
    
    # Step 2: Extract entities using BioBERT
    drugs_biobert, diseases_biobert = extract_entities_biobert(text)
    
    # Combine entities for comparison
    scispacy_entities = drugs_scispacy + diseases_scispacy
    biobert_entities = drugs_biobert + diseases_biobert
    
    # Compare the entities detected by both models
    compare_entities(scispacy_entities, biobert_entities)

# Example usage
if __name__ == "__main__":
    # Load the text from the correct file
    with open('combined_text_output.txt', 'r') as file:
        medical_text = file.read()

    # Run the pipeline
    medical_text_pipeline(medical_text)
