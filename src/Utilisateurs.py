class Utilisateurs:
    def __init__(self, name, password):
        self.name = name
        self.password = password

    def se_connecter(self, nom_utilisateur, mot_de_passe):
        return self.name == nom_utilisateur and self.password == mot_de_passe