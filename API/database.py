"""
Database connection handlers for SQLite and MongoDB
"""
import sqlite3
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Base directory (project root)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Load .env from the project root
ENV_PATH = os.path.join(BASE_DIR, '.env')
load_dotenv(ENV_PATH)
DB_PATH = os.path.join(BASE_DIR, "databases", "erd", "hr_attrition.db")

class SQLiteDB:
    """SQLite database connection handler"""
    
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
    
    def get_connection(self):
        """Get a new SQLite connection"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Return rows as dictionaries
            return conn
        except sqlite3.Error as e:
            raise Exception(f"SQLite connection error: {e}")
    
    def test_connection(self):
        """Test SQLite connection"""
        try:
            conn = self.get_connection()
            conn.close()
            return True
        except:
            return False

class MongoDB:
    """MongoDB connection handler"""
    
    def __init__(self):
        self.client = None
        self.db = None
        self.connect()
    
    def connect(self):
        """Establish MongoDB connection"""
        connection_string = os.getenv('MONGODB_URI')
        
        try:
            if connection_string:
                self.client = MongoClient(connection_string, serverSelectionTimeoutMS=10000)
                self.client.admin.command('ping')
            else:
                self.client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=3000)
                self.client.admin.command('ping')
            
            self.db = self.client["hr_rdbms_project"]
            return True
        except Exception as e:
            print(f"MongoDB connection warning: {e}")
            return False
    
    def get_db(self):
        """Get MongoDB database instance"""
        if self.db is None:
            self.connect()
        return self.db
    
    def test_connection(self):
        """Test MongoDB connection"""
        try:
            if self.client:
                self.client.admin.command('ping')
                return True
            return False
        except:
            return False
    
    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()

# Singleton instances
sqlite_db = SQLiteDB()
mongodb_db = MongoDB()
