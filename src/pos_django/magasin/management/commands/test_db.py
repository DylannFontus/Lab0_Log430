from django.core.management.base import BaseCommand
import MySQLdb
import os
from django.contrib.auth.models import User

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        self.stdout.write("Connexion à MySQL pour donner les droits sur la base de test...")

        # Création du super utilisateur s'il n'existe pas
        if not User.objects.filter(username="useradmin").exists():
            User.objects.create_superuser(
                username="useradmin",
                email="admin@example.com",
                password="verysecretpassword"
            )
            self.stdout.write(self.style.SUCCESS("Super utilisateur 'magasin' créé."))
        else:
            self.stdout.write("Super utilisateur déjà présent, rien à faire.")

        try:
            conn = MySQLdb.connect(
                host=os.getenv("DB_HOST", "db"),
                user=os.getenv("MYSQL_ROOT_USER", "root"),
                passwd=os.getenv("MYSQL_ROOT_PASSWORD", "root")
            )
            cursor = conn.cursor()

            # Modifier ici selon le nom exact de ta base de test
            cursor.execute("GRANT ALL PRIVILEGES ON `test_%`.* TO 'magasin'@'%';")
            cursor.execute("FLUSH PRIVILEGES;")
            conn.commit()
            cursor.close()
            conn.close()

            self.stdout.write(self.style.SUCCESS("Droits accordés à 'magasin' sur les bases test_%"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Échec de l’attribution des droits : {e}"))