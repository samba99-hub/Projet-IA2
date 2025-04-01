import sqlite3

# Connexion (créera le fichier users.db s'il n'existe pas)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Création de la table des utilisateurs
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    face_descriptor BLOB)''')

conn.commit()
conn.close()

print("Base de données SQLite créée avec succès !")