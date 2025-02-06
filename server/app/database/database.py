# Imports
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# Load Environment Variables
load_dotenv()

# Database URL
DATABASE_URL = os.environ['DATABASE_URL']

# Set Up Engine
engine = create_engine(DATABASE_URL)

# Set Up Local Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Set Up Base
Base = declarative_base()

