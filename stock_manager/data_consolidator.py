import pandas as pd
import os


class DataConsolidator:
    def __init__(self):
        """ Initialise un consolidateur de données avec un DataFrame vide.

        PRE : Aucun
        POST : Une instance de DataConsolidator est initialisée avec un DataFrame vide.
        """
        self.data = pd.DataFrame()


    def load_csv_files(self, input_dir):
        """ Charge tous les fichiers CSV d'un répertoire donné et les consolide dans un seul DataFrame.

        PRE :
        - input_dir doit être un chemin valide contenant des fichiers CSV.
        - Les fichiers CSV doivent être formatés correctement.

        POST :
        - Les fichiers CSV sont chargés et concaténés dans self.data.
        - self.data contient les données consolidées.

        RAISE :
        - FileNotFoundError si le répertoire n'existe pas.
        - pd.errors.ParserError si un fichier CSV est mal formaté.
        """
        if not os.path.isdir(input_dir):
            raise FileNotFoundError(f"Le répertoire spécifié n'existe pas : {input_dir}")

        all_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]
        dataframes = []

        for file in all_files:
            filepath = os.path.join(input_dir, file)
            try:
                df = pd.read_csv(filepath)
                dataframes.append(df)
            except Exception as e:
                print(f"Erreur lors du chargement du fichier {file}: {e}")

        self.data = pd.concat(dataframes, ignore_index=True)


    def clean_data(self):
        """ Nettoie les données consolidées en supprimant les valeurs manquantes et en standardisant les types.

        PRE :
        - self.data doit contenir un DataFrame valide chargé via load_csv_files.

        POST :
        - Les valeurs manquantes sont supprimées de self.data.
        - Les colonnes 'quantity' et 'unit_price' sont converties dans leurs types respectifs.
        """
        self.data.dropna(inplace=True)

        if 'quantity' in self.data.columns:
            self.data['quantity'] = self.data['quantity'].astype(int)
        if 'unit_price' in self.data.columns:
            self.data['unit_price'] = self.data['unit_price'].astype(float)


    def remove_duplicates(self):
        """ Supprime les doublons dans le DataFrame consolidé.

        PRE :
        - self.data doit contenir un DataFrame valide.

        POST :
        - Tous les doublons dans self.data sont supprimés.
        """
        self.data.drop_duplicates(inplace=True)


    def get_data(self):
        """ Retourne les données consolidées sous forme de DataFrame.

        PRE :
        - Les données doivent avoir été chargées via load_csv_files.

        POST :
        - Retourne un DataFrame pandas contenant les données consolidées.

        RAISE :
        - ValueError si self.data est vide.
        """
        if self.data.empty:
            raise ValueError("Les données consolidées sont vides.")
        return self.data
