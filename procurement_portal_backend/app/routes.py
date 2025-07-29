from flask import Blueprint, jsonify
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from .utils.pdf_parser import parse_pdf
from .models import PDFExtraction
from . import db
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return jsonify(message="Backend is running!")

@main.post("/extract")
def extract():
    if "file" not in request.files: # Check if anything has been uploaded at all
        return jsonify(error="No file part"), 400

    f = request.files["file"]
    if f.filename == "": # Check if the filename is empty
        return jsonify(error="No selected file"), 400

    filename  = secure_filename(f.filename) # Sanitize the filename
    logging.info(f"Received file: {filename}")

    if f.content_type != "application/pdf":
        logging.error(f"Invalid file type: {f.content_type}")
        return jsonify(error="Uploaded file is not a PDF"), 400

    logging.info(f"File type confirmed as PDF: {f.content_type}")

    save_path = f"{current_app.config['UPLOAD_FOLDER']}/{filename}"
    f.save(save_path)
    logging.info(f"File saved to: {save_path}")

    try:
        data = parse_pdf(save_path)
        logging.info("PDF parsing completed successfully.")

        # Ensure data is a dictionary, not a JSON string
        if isinstance(data, str):
            logging.warning("Data returned by parse_pdf is a string. Parsing it back to a dictionary.")
            data = json.loads(data)

        # Save extracted data to the database
        pdf_record = PDFExtraction(filename=filename, extracted_data=data)
        db.session.add(pdf_record)
        db.session.commit()
        logging.info("Extracted data saved to the database.")

        return jsonify(data)  # Properly format the JSON response
    except Exception as e:
        logging.error(f"Error while parsing PDF: {e}")
        return jsonify(error=str(e)), 500
    
@main.get("/entries")
def get_entries():
    try:
        records = PDFExtraction.query.all()
        entries = [
            {
                "id": record.id,
                "filename": record.filename,
                "extracted_data": record.extracted_data,
                "status": record.status,
            } for record in records
        ]
        return jsonify(entries), 200
    except Exception as e:
        logging.error(f"Error fetching entries: {e}")
        return jsonify(error=str(e)), 500
    
@main.put("/update/<int:id>/<int:status>")
def update_entry(id, status):
    try:
        record = PDFExtraction.query.get_or_404(id)
        record.status = status
        db.session.commit()
        logging.info(f"Record {id} updated with status {status}.")
        return jsonify(message="Entry updated successfully"), 200
    except Exception as e:
        logging.error(f"Error updating entry {id}: {e}")
        return jsonify(error=str(e)), 500
    
@main.delete("/delete/<int:id>")
def delete_entry(id):
    try:
        record = PDFExtraction.query.get_or_404(id)
        db.session.delete(record)
        db.session.commit()
        logging.info(f"Record {id} deleted successfully.")
        return jsonify(message="Entry deleted successfully"), 200
    except Exception as e:
        logging.error(f"Error deleting entry {id}: {e}")
        return jsonify(error=str(e)), 500