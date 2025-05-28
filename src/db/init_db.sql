CREATE DATABASE IF NOT EXISTS magasin;
USE magasin;

-- Table : produits
CREATE TABLE IF NOT EXISTS produits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    categorie VARCHAR(255),
    prix FLOAT NOT NULL,
    quantite_stock INT NOT NULL
);

-- Table : ventes
CREATE TABLE IF NOT EXISTS ventes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    total FLOAT NOT NULL,
    date DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table : vente_produits (association plusieurs produits ↔ une vente)
CREATE TABLE IF NOT EXISTS vente_produits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vente_id INT NOT NULL,
    produit_id INT NOT NULL,
    FOREIGN KEY (vente_id) REFERENCES ventes(id) ON DELETE CASCADE,
    FOREIGN KEY (produit_id) REFERENCES produits(id)
);
