from flask import Flask, request, render_template, redirect, url_for, send_file, jsonify, session
from extractors.pdf_extractor import extract_text_from_pdf, extract_tables_from_pdf, save_tables_to_excel
from extractors.ocr_extractor import extract_text_from_scanned_pdf
from models.ner_model import load_ner_model, extract_entities
from utils.feedback_handler import FeedbackHandler
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-key-please-change')

# Initialize feedback handler
feedback_handler = FeedbackHandler()

# Load NER model once at startup
ner_model = load_ner_model()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    
    try:
        # Create timestamp for unique filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save the uploaded file
        original_filename = file.filename
        base_name = os.path.splitext(original_filename)[0]
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{base_name}_{timestamp}.pdf")
        file.save(file_path)
        
        # Extract text and tables
        text = extract_text_from_pdf(file_path)
        tables = extract_tables_from_pdf(file_path)
        
        # Extract entities using NER with confidence scores
        entities, confidence_scores = extract_entities(text, ner_model)
        
        # Store in session for feedback
        session['original_text'] = text
        session['extracted_entities'] = entities
        session['confidence_scores'] = confidence_scores
        
        # Save tables to Excel with timestamp
        excel_filename = f"{base_name}_{timestamp}_output.xlsx"
        excel_path = os.path.join(app.config['UPLOAD_FOLDER'], excel_filename)
        save_tables_to_excel(tables, excel_path)
        
        # Store excel path in session for later download
        session['excel_path'] = excel_path
        session['excel_filename'] = excel_filename
        
        return render_template('index.html', 
                             extracted_data=entities,
                             confidence_scores=confidence_scores,
                             excel_ready=True)  # Flag to show download button
    
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return f"Error processing file: {str(e)}", 500

@app.route('/download_excel')
def download_excel():
    """Route to download the generated Excel file"""
    try:
        excel_path = session.get('excel_path')
        excel_filename = session.get('excel_filename')
        
        if not excel_path or not os.path.exists(excel_path):
            return "Excel file not found", 404
            
        return send_file(
            excel_path,
            as_attachment=True,
            download_name=excel_filename,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    except Exception as e:
        print(f"Error downloading file: {str(e)}")
        return f"Error downloading file: {str(e)}", 500

if __name__ == '__main__':
    # Create uploads directory if it doesn't exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)