from database.db_connection import connect_to_db

def apply_schema():
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        try:
            # Check if tbl_budget exists
            cursor.execute("SHOW TABLES LIKE 'tbl_budget'")
            if cursor.fetchone():
                print("tbl_budget already exists.")
            else:
                print("Creating tbl_budget...")
                cursor.execute("""
                CREATE TABLE tbl_budget (
                    budget_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    category_id INT NOT NULL,
                    amount DECIMAL(10, 2) NOT NULL,
                    month INT NOT NULL,
                    year INT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES tbl_users(user_id) ON DELETE CASCADE,
                    FOREIGN KEY (category_id) REFERENCES tbl_categories(category_id) ON DELETE CASCADE,
                    UNIQUE(user_id, category_id, month, year)
                );
                """)
                print("tbl_budget created successfully.")
            conn.commit()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    apply_schema()
