from . import db
import json

class User(db.Model):
    """Model for user accounts."""
    __tablename__ = 'users'

    user_id = db.Column(db.String(80), primary_key=True)
    history = db.Column(db.Text, nullable=False, default='[]')
    consent_intime = db.Column(db.Boolean, nullable=False, default=False)
    proposal_pending = db.Column(db.Boolean, nullable=False, default=False)
    mood = db.Column(db.String(50), nullable=False, default='neutre')

    def get_history(self):
        return json.loads(self.history or '[]')

    def set_history(self, history_list):
        self.history = json.dumps(history_list)

    def __repr__(self):
        return f'<User {self.user_id}>'