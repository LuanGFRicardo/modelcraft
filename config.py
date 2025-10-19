import os

class Config:
   SECRET_KEY = os.environ.get('SECRET_KEY', 'unisenai')  
   SQLALCHEMY_DATABASE_URI = 'sqlite:///modelcraft.db'