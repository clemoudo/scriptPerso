import pandas as pd


class ReportGenerator:
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file)

    def save_report(self, output_file):
        # Génération du rapport détaillé par catégorie
        quantity = self.data['Quantité']
        unit_price = self.data['Prix Unitaire']
        self.data['Valeur Totale'] = quantity * unit_price
        summary = self.data.groupby('Catégorie').agg(
            Quantité_Totale=('Quantité', 'sum'),
            Valeur_Totale=('Valeur Totale', 'sum')
        ).reset_index()

        # Calcul des totaux globaux
        total_quantities = self.data['Quantité'].sum()
        total_value = self.data['Valeur Totale'].sum()

        # Ajouter une ligne pour les totaux globaux
        total_row = {
            'Catégorie': 'Toutes',
            'Quantité_Totale': total_quantities,
            'Valeur_Totale': total_value
        }
        summary = pd.concat([summary, pd.DataFrame([total_row])],
                            ignore_index=True)

        # Sauvegarde du fichier
        summary.to_csv(output_file, index=False)
        print(f"Rapport sauvegardé dans le fichier : {output_file}")
