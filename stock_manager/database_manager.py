import sqlite3
from sqlite3 import Error
import pandas as pd

class DatabaseManager:
    def __init__(self, db_path):
        """ Initialise le gestionnaire de base de données avec un chemin vers la base SQLite.
        PRE :
        - db_path doit être une chaîne valide représentant le chemin de la base de données SQLite.

        POST :
        - Une connexion à la base de données est établie si le chemin est valide.

        RAISE :
        - ValueError si db_path est invalide.
        - Error si la connexion échoue.
        """
        if not isinstance(db_path, str) or not db_path.strip():
            raise ValueError("Le chemin de la base de données doit être une chaîne non vide.")

        try:
            self.connection = sqlite3.connect(db_path)
        except Error as e:
            raise Error(f"Erreur lors de la connexion à la base de données : {e}")

    def create_table(self):
        """ Crée une table pour stocker les données consolidées si elle n'existe pas.

        PRE :
        - La connexion à la base de données doit être active.

        POST :
        - Une table nommée 'stocks' est créée dans la base de données.

        RAISE :
        - Error si la création de la table échoue.
        """
        create_table_query = """
            CREATE TABLE IF NOT EXISTS stocks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL
            );
            """
        try:
            cursor = self.connection.cursor()
            cursor.execute(create_table_query)
            self.connection.commit()
        except Error as e:
            raise Error(f"Erreur lors de la création de la table : {e}")

    def insert_data(self, data):
        """ Insère des données dans la table 'stocks'.

        PRE :
        - data doit être un DataFrame pandas contenant les colonnes 'name', 'category', 'quantity', et 'unit_price'.

        POST :
        - Les données sont insérées dans la table 'stocks'.

        RAISE :
        - ValueError si data n'est pas un DataFrame valide.
        - KeyError si des colonnes nécessaires sont manquantes.
        - Error si l'insertion des données échoue.
        """
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Les données doivent être un DataFrame pandas.")
        required_columns = {'name', 'category', 'quantity', 'unit_price'}
        if not required_columns.issubset(data.columns):
            raise KeyError(f"Les colonnes suivantes sont requises : {required_columns}")

        try:
            data.to_sql('stocks', self.connection, if_exists='append', index=False)
        except Error as e:
            raise Error(f"Erreur lors de l'insertion des données : {e}")

    def query_data(self, criteria):
        """  Exécute une requête sur la table 'stocks' en fonction des critères spécifiés.

        PRE :
        - criteria doit être un dictionnaire contenant des clés valides (e.g., 'name', 'category', 'quantity').

        POST :
        - Retourne un DataFrame contenant les résultats de la requête.

        RAISE :
        - Error si la requête échoue.
        """
        query = "SELECT * FROM stocks WHERE "
        conditions = []
        params = []

        for key, value in criteria.items():
            conditions.append(f"{key} = ?")
            params.append(value)

        query += " AND ".join(conditions)

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            return pd.DataFrame(rows, columns=columns)
        except Error as e:
            raise Error(f"Erreur lors de la requête des données : {e}")

    def update_data(self, product_id, updated_values):
        """ Met à jour les données d'un produit existant.

        PRE :
        - product_id doit être un entier positif.
        - updated_values doit être un dictionnaire avec des clés valides (e.g., 'quantity', 'unit_price').

        POST :
        - Les données du produit sont mises à jour dans la table 'stocks'.

        RAISE :
        - ValueError si product_id est invalide.
        - Error si la mise à jour échoue.
        """
        if not isinstance(product_id, int) or product_id <= 0:
            raise ValueError("L'ID du produit doit être un entier positif.")

        set_clause = ", ".join([f"{key} = ?" for key in updated_values.keys()])
        params = list(updated_values.values()) + [product_id]

        query = f"""
        UPDATE stocks
        SET {set_clause}
        WHERE id = ?
        """

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
        except Error as e:
            raise Error(f"Erreur lors de la mise à jour des données : {e}")

    def close_connection(self):
        """  Ferme la connexion à la base de données.

        PRE :
        - La connexion doit être active.

        POST :
        - La connexion est fermée.

        RAISE :
        - Error si la fermeture de la connexion échoue.
        """
        try:
            self.connection.close()
        except Error as e:
            raise Error(f"Erreur lors de la fermeture de la connexion : {e}")
