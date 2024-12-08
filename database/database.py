import sqlite3

def create_connection():
    conn = sqlite3.connect('documents_final.db')
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Document_Name TEXT NOT NULL UNIQUE,
            Document_Type TEXT,
            Summary TEXT,
            Ocr_Enhanced TEXT
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def insert_document(document_name, document_type, summary, ocr_enhanced):
    conn=create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Documents WHERE Document_Name=?", (document_name,))
    count = cursor.fetchone()[0]
    
    if count > 0:
        print(f"Document '{document_name}' already exists. Updating instead.")
        cursor.execute("""
            UPDATE Documents
            SET Document_Type=?, Summary=?, OCR_Enhanced=?
            WHERE Document_Name=?
        """, (document_type, summary, ocr_enhanced, document_name))
    else:
        cursor.execute("""
            INSERT INTO Documents (Document_Name, Document_Type, Summary, OCR_Enhanced)
            VALUES (?, ?, ?, ?)
        """, (document_name, document_type, summary, ocr_enhanced))
    
    conn.commit()
    cursor.close()



def get_document_summary(document_name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Summary FROM Documents WHERE Document_Name = ?", (document_name,))
    summary = cursor.fetchone()
    cursor.close()
    conn.close()
    return summary[0] if summary else None

def get_all_documents():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Documents")
    documents = cursor.fetchall()
    cursor.close()
    conn.close()
    return documents

def get_document_type(document_name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Document_Type FROM Documents WHERE Document_Name = ?", (document_name,))
    doc_type = cursor.fetchone()
    cursor.close()
    conn.close()
    return doc_type[0] if doc_type else None

def get_ocr_enhanced(document_name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Ocr_Enhanced FROM Documents WHERE Document_Name = ?", (document_name,))
    ocr_text = cursor.fetchone()
    cursor.close()
    conn.close()
    return ocr_text[0] if ocr_text else None

def delete_document(document_name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Documents WHERE Document_Name = ?", (document_name,))
    
    if cursor.rowcount > 0:
        print(f"Document '{document_name}' is now deleted.")
    else:
        print(f"No document found with the name '{document_name}' to delete.")
    
    conn.commit()
    cursor.close()
    conn.close()