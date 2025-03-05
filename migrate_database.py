"""
Script to migrate the database from the old 'man' table to the new 'profile' table.
This will:
1. Create a new 'profile' table
2. Copy all data from 'man' to 'profile'
3. Update foreign keys in the 'request' table
4. Drop the old 'man' table
"""
from app import app, db
from models import User, Profile, MartialStatus, Request
import logging
import os
import sqlite3

# Configure logging
if not os.path.exists('Logs'):
    os.makedirs('Logs')
logging.basicConfig(
    filename='Logs/database_migration.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def migrate_database():
    """Migrate the database from 'man' to 'profile'."""
    logging.info("Starting database migration")
    
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('dating.db')
        cursor = conn.cursor()
        
        # Check if 'man' table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='man'")
        man_table_exists = cursor.fetchone() is not None
        
        if not man_table_exists:
            logging.info("'man' table doesn't exist. No migration needed.")
            print("'man' table doesn't exist. No migration needed.")
            return
        
        # Check if 'profile' table already exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='profile'")
        profile_table_exists = cursor.fetchone() is not None
        
        if profile_table_exists:
            logging.info("'profile' table already exists. Skipping migration.")
            print("'profile' table already exists. Skipping migration.")
            return
        
        # Create the new 'profile' table
        with app.app_context():
            # Create all tables (including the new 'profile' table)
            db.create_all()
            
            # Get all columns from the 'man' table
            cursor.execute("PRAGMA table_info(man)")
            columns = cursor.fetchall()
            column_names = [column[1] for column in columns]
            
            # Prepare column list for SQL query
            columns_str = ', '.join(column_names)
            
            # Copy data from 'man' to 'profile'
            cursor.execute(f"""
                INSERT INTO profile ({columns_str.replace('idman', 'idprofile')})
                SELECT {columns_str} FROM man
            """)
            
            # Update foreign keys in the 'request' table
            cursor.execute("""
                UPDATE request
                SET idrequester = (
                    SELECT idprofile FROM profile WHERE profile.idprofile = request.idrequester
                ),
                idtarget = (
                    SELECT idprofile FROM profile WHERE profile.idprofile = request.idtarget
                )
            """)
            
            # Commit the changes
            conn.commit()
            
            # Drop the old 'man' table
            cursor.execute("DROP TABLE man")
            conn.commit()
            
            logging.info("Database migration completed successfully")
            print("Database migration completed successfully!")
    
    except Exception as e:
        logging.error(f"Error migrating database: {str(e)}")
        print(f"Error migrating database: {str(e)}")
    
    finally:
        # Close the connection
        if conn:
            conn.close()

if __name__ == "__main__":
    migrate_database()
