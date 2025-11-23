import os

class Config:
    """Set Flask configuration from .env file."""

    # General Config
    SECRET_KEY = os.environ.get('SECRET_KEY')
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG')

    # Database
    SQLALCHEMY_DATABASE_URI = "sqlite:///../instance/jenny_memory.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # OpenRouter API (avec Grok gratuit)
    OPENROUTER_API_KEY = "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"
    OPENROUTER_MODEL = "x-ai/grok-4.1-fast:free"  # Modèle Grok gratuit sur OpenRouter
    
    # Image Directory
    IMAGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'images'))