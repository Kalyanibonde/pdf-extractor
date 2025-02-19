# feedback_handler.py
import json
import os
from datetime import datetime

class FeedbackHandler:
    """Handles feedback collection and storage for model improvements"""
    
    def __init__(self, feedback_dir='feedback'):
        # Use absolute path relative to project root
        self.feedback_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), feedback_dir)
        if not os.path.exists(self.feedback_dir):
            os.makedirs(self.feedback_dir)
            
    def save_feedback(self, original_text, extracted_entities, corrected_entities, confidence_scores):
        """
        Saves feedback data to a JSON file
        Args:
            original_text: Original text from PDF
            extracted_entities: Entities extracted by model
            corrected_entities: User-corrected entities
            confidence_scores: Model confidence scores for extracted entities
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        feedback_data = {
            "timestamp": timestamp,
            "original_text": original_text,
            "extracted_entities": extracted_entities,
            "corrected_entities": corrected_entities,
            "confidence_scores": confidence_scores
        }
        
        filename = f"feedback_{timestamp}.json"
        filepath = os.path.join(self.feedback_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(feedback_data, f, indent=4, ensure_ascii=False)
        
        return filepath
    
    def get_feedback_files(self):
        """Returns list of all feedback files"""
        return [f for f in os.listdir(self.feedback_dir) if f.endswith('.json')]
    
    def load_feedback(self, filename):
        """Loads specific feedback file"""
        filepath = os.path.join(self.feedback_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)