#!/usr/bin/env python3
"""
Test AlwaysData Database Connection
"""

import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

def test_connection():
    """Test database connection"""
    print("🔍 Testing AlwaysData MySQL Connection...")
    print(f"Host: mysql-aymenchaghoub.alwaysdata.net")
    print(f"Database: aymenchaghoub_pfc\n")
    
    if not DATABASE_URL:
        print("❌ DATABASE_URL not found in .env file")
        return False
    
    try:
        # Create engine
        engine = create_engine(DATABASE_URL, pool_pre_ping=True)
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.fetchone()
            
        print("✅ Database connection: SUCCESS")
        
        # Test tables
        with engine.connect() as conn:
            result = conn.execute(text("SHOW TABLES"))
            tables = result.fetchall()
            
            if tables:
                print(f"✅ Found {len(tables)} tables:")
                for table in tables:
                    print(f"   - {table[0]}")
            else:
                print("⚠️  No tables found (database is empty)")
                print("   This is normal for first deployment - tables will be created automatically")
        
        return True
        
    except Exception as e:
        print(f"❌ Database connection FAILED")
        print(f"Error: {str(e)}")
        
        # Provide troubleshooting
        print("\n📋 Troubleshooting:")
        print("  1. Verify database credentials in .env")
        print("  2. Check AlwaysData database is active")
        print("  3. Verify firewall/network access")
        
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
