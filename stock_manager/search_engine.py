import pandas as pd

class SearchEngine:
    def __init__(self, data):
        """ Initialise le moteur de recherche avec un DataFrame contenant les données consolidées.
        PRE :
        - data doit être un DataFrame pandas non vide.

        POST :
        - Une instance de SearchEngine est initialisée avec les données fournies.

        RAISE :
        - ValueError si data est vide ou n'est pas un DataFrame.
        """
        if not isinstance(data, pd.DataFrame) or data.empty:
            raise ValueError("Les données doivent être un DataFrame pandas non vide.")
        self.data = data

    def filter_by_name(self, name):
        """ Filtre les produits par nom exact.

        PRE :
        - name doit être une chaîne de caractères valide.

        POST :
        - Retourne un DataFrame contenant les produits correspondant exactement au nom donné.

        RAISE :
        - ValueError si le nom est vide.
        """
        if not name:
            raise ValueError("Le nom du produit ne peut pas être vide.")

        result = self.data[self.data['name'] == name]
        return result

    def filter_by_category(self, category):
        """ Filtre les produits par catégorie.

        PRE :
        - category doit être une chaîne de caractères valide.

        POST :
        - Retourne un DataFrame contenant les produits de la catégorie donnée.

        RAISE :
        - ValueError si la catégorie est vide.
        """
        if not category:
            raise ValueError("La catégorie ne peut pas être vide.")

        result = self.data[self.data['category'] == category]
        return result

    def filter_by_price_range(self, min_price, max_price):
        """ Filtre les produits dont le prix unitaire est compris dans une plage donnée.

        PRE :
        - min_price et max_price doivent être des nombres valides (min_price <= max_price).

        POST :
        - Retourne un DataFrame contenant les produits dans la plage de prix donnée.

        RAISE :
        - ValueError si min_price > max_price ou si l'un des arguments est invalide.
        """
        if min_price > max_price:
            raise ValueError("min_price doit être inférieur ou égal à max_price.")

        result = self.data[(self.data['unit_price'] >= min_price) & (self.data['unit_price'] <= max_price)]
        return result

    def filter_by_quantity(self, min_quantity):
        """ Filtre les produits dont la quantité en stock est supérieure ou égale à min_quantity.

        PRE :
        - min_quantity doit être un entier positif.

        POST :
        - Retourne un DataFrame contenant les produits avec une quantité >= min_quantity.

        RAISE :
        - ValueError si min_quantity est négatif ou non entier.
        """
        if min_quantity < 0:
            raise ValueError("min_quantity doit être un entier positif.")

        result = self.data[self.data['quantity'] >= min_quantity]
        return result

    def sort_results(self, by, ascending=True):
        """ Trie les résultats par une colonne donnée.

        PRE :
        - by doit être une colonne valide du DataFrame.
        - ascending est un booléen indiquant l'ordre du tri.

        POST :
        - Retourne un DataFrame trié par la colonne spécifiée.

        RAISE :
        - ValueError si la colonne n'existe pas dans le DataFrame.
        """
        if by not in self.data.columns:
            raise ValueError(f"La colonne spécifiée '{by}' n'existe pas.")

        result = self.data.sort_values(by=by, ascending=ascending)
        return result