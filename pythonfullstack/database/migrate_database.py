# migrate_database.py
import sqlite3

def migrate_database():
    """
    Migrate the books table to support the new category/subcategory structure
    """
  conn = sqlite3.connect("pythonfullstack/database/library.db")
         cursor = conn.cursor()
    
    # Check if the table exists and get its current structure
    cursor.execute("PRAGMA table_info(books)")
    columns = cursor.fetchall()
    column_names = [col[1] for col in columns]
    
    print("Current columns in books table:", column_names)
    
    # Check if we need to add category and subcategory columns
    needs_migration = False
    
    if 'category' not in column_names:
        print("Adding 'category' column...")
        cursor.execute("ALTER TABLE books ADD COLUMN category TEXT")
        needs_migration = True
    
    if 'subcategory' not in column_names:
        print("Adding 'subcategory' column...")
        cursor.execute("ALTER TABLE books ADD COLUMN subcategory TEXT")
        needs_migration = True
    
    if needs_migration:
        # Update existing books with default values if needed
        # You might want to map old categories to new ones
        cursor.execute("""
            UPDATE books 
            SET category = CASE 
                WHEN category IS NULL OR category = '' THEN 'Computer Science'
                ELSE category 
            END,
            subcategory = CASE 
                WHEN subcategory IS NULL OR subcategory = '' THEN 'C++'
                ELSE subcategory 
            END
            WHERE category IS NULL OR subcategory IS NULL
        """)
        
        conn.commit()
        print("✅ Database migration completed successfully!")
    else:
        print("✅ Database already has the correct schema!")
    
    # Show the updated schema
    cursor.execute("PRAGMA table_info(books)")
    columns = cursor.fetchall()
    print("\nUpdated table schema:")
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")
    
    # Show current data
    cursor.execute("SELECT COUNT(*) FROM books")
    count = cursor.fetchone()[0]
    print(f"\nTotal books in database: {count}")
    
    if count > 0:
        cursor.execute("SELECT id, book_name, category, subcategory FROM books LIMIT 5")
        print("\nSample books:")
        for book in cursor.fetchall():
            print(f"  ID: {book[0]}, Name: {book[1]}, Category: {book[2]}, Subcategory: {book[3]}")
    
    conn.close()

if __name__ == "__main__":
    print("🔧 Starting database migration...\n")
    migrate_database()