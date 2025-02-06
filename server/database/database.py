# Imports
from dotenv import load_dotenv
import os
# Load Environment Variables
load_dotenv()

# Database URL
DATABASE_URL = os.environ['DATABASE_URL']

# Set Up Engine
engine = create_engine(DATABASE_URL)

# Set Up Base
Base = declarative_base()

