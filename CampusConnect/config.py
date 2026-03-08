import os

class Config:
    SECRET_KEY = 'your-secret-key-change-this-in-production'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///campus_complaints.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
