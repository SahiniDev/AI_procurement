from . import db
class PDFExtraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    extracted_data = db.Column(db.JSON, nullable=False)
    status = db.Column(db.Integer, default=0)  # Store numeric status (0, 1, 2)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


    # Map numeric status to string representation
    @property
    def status_label(self):
        status_map = {0: "Open", 1: "In Progress", 2: "Closed"}
        return status_map.get(self.status, "Unknown")