import spacy
from typing import Tuple, Dict

def load_ner_model():
    """Load the spaCy NER model"""
    try:
        # Load English language model
        nlp = spacy.load("en_core_web_sm")
        return nlp
    except OSError:
        # If model not found, download it
        print("Downloading spaCy model...")
        spacy.cli.download("en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")
        return nlp

def extract_entities(text: str, model) -> Tuple[Dict[str, str], Dict[str, float]]:

    if not isinstance(text, str):
        text = str(text)
    
    # Process the text with spaCy
    try:
        doc = model(text)
        
        entities = {}
        confidence_scores = {}
        
        # Extract entities
        for ent in doc.ents:
            # Store unique entities (keep the first occurrence if duplicate labels)
            key = f"{ent.label_}_{len(entities)}"  # Make unique keys for each entity
            entities[key] = {
                'text': ent.text,
                'label': ent.label_
            }
            # Mock confidence score between 0.7 and 1.0
            confidence_scores[key] = 0.7 + (hash(ent.text) % 3000) / 10000.0
        
        return entities, confidence_scores
        
    except Exception as e:
        print(f"Error in entity extraction: {str(e)}")
        # Return empty results if there's an error
        return {}, {}