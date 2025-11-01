from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the database connection
db = SQLAlchemy()

# Define the Request model
class Request(db.Model):
    __tablename__ = 'requests'

    id = db.Column(db.Integer, primary_key=True)
    requester_name = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime, nullable=True)

    def mark_resolved(self):
        """Mark a request as resolved and set the resolved time."""
        self.status = 'Resolved'
        self.resolved_at = datetime.utcnow()
