"""
Script to fix the gender values in the instance/app.db database.
"""
import sqlite3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_gender_values():
    """Fix gender values in the database."""
    # Use the instance/app.db file
    db_path = "instance/app.db"
    
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        logger.info(f"Tables in the database: {[table[0] for table in tables]}")
        
        # Find the profile table (it might have a different name)
        profile_table = None
        for table in tables:
            table_name = table[0]
            # Check if this table has a gender column
            try:
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns = cursor.fetchall()
                column_names = [col[1] for col in columns]
                if 'gender' in column_names:
                    profile_table = table_name
                    logger.info(f"Found profile table: {profile_table}")
                    logger.info(f"Columns: {column_names}")
                    break
            except Exception as e:
                logger.error(f"Error checking table {table_name}: {str(e)}")
                continue
        
        if not profile_table:
            logger.error("Could not find a table with a gender column")
            return
        
        # Update gender values
        try:
            # Check if there are any profiles with lowercase gender values
            cursor.execute(f"SELECT COUNT(*) FROM {profile_table} WHERE gender='male' OR gender='female'")
            count = cursor.fetchone()[0]
            
            if count > 0:
                # Update male to MALE
                cursor.execute(f"UPDATE {profile_table} SET gender='MALE' WHERE gender='male'")
                male_count = cursor.rowcount
                
                # Update female to FEMALE
                cursor.execute(f"UPDATE {profile_table} SET gender='FEMALE' WHERE gender='female'")
                female_count = cursor.rowcount
                
                # Commit the changes
                conn.commit()
                
                logger.info(f"Updated {male_count} male profiles and {female_count} female profiles")
            else:
                logger.info("No profiles with lowercase gender values found")
        except Exception as e:
            logger.error(f"Error updating gender values: {str(e)}")
        
        # Close the connection
        conn.close()
        
    except Exception as e:
        logger.error(f"Error accessing database: {str(e)}")

if __name__ == "__main__":
    fix_gender_values()
