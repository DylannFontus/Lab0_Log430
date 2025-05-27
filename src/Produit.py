class Produit:
    def __init__(self, identifiant, nom, categorie, prix):
        self._identifiant = identifiant
        self._nom = nom
        self._categorie = categorie
        self._prix = prix

    # Getter et Setter pour identifiant
    def get_identifiant(self):
        return self._identifiant

    def set_identifiant(self, identifiant):
        self._identifiant = identifiant

    # Getter et Setter pour nom
    def get_nom(self):
        return self._nom

    def set_nom(self, nom):
        self._nom = nom

    # Getter et Setter pour categorie
    def get_categorie(self):
        return self._categorie

    def set_categorie(self, categorie):
        self._categorie = categorie

    # Getter et Setter pour prix
    def get_prix(self):
        return self._prix
    
    def set_prix(self, prix):
        if prix < 0:
            raise ValueError("Le prix ne peut pas être négatif.")
        self._prix = prix

    def __str__(self):
        return f"Produit(id={self._identifiant}, nom='{self._nom}', categorie='{self._categorie}', prix='{self._prix}')"
