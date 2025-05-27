import mysql.connector
def get_connection():
    return mysql.connector.connect(
        host="db",
        user="magasin",
        password="wagjids",
        database="magasin"
    )


def main():
    conn = get_connection()
    repo = MySqlUserRepository(conn)

    # Exemple : ajouter un utilisateur
    user = User(id=1, name="Alice")
    repo.save(user)

    # Exemple : récupérer l'utilisateur
    retrieved = repo.find_by_id(1)
    print("Trouvé:", retrieved)

    # Liste tous les utilisateurs
    users = repo.find_all()
    for u in users:
        print(u)

    # Supprimer
    repo.delete(1)

    conn.close()

if __name__ == "__main__":
    main()
