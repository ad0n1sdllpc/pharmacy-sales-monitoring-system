import sqlite3
import random

# Connect to the SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect('transactions.db')
cursor = conn.cursor()

# Specify the year for which you want to delete 100 IDs
target_year = '2021'

# Fetch 100 random IDs from the specified year
cursor.execute(f'''
    SELECT id
    FROM transactions
    WHERE strftime('%Y', transaction_date) = '{target_year}'
    ORDER BY RANDOM()
    LIMIT 300
''')
ids_to_delete = cursor.fetchall()

# Extract the IDs from the result
ids = [id[0] for id in ids_to_delete]

# Execute the DELETE statement using the extracted IDs
cursor.execute(f'DELETE FROM transactions WHERE id IN ({", ".join(map(str, ids))});')

# Commit the changes
conn.commit()

# Close the connection
conn.close()
