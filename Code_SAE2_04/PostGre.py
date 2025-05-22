#    /\
#   /  \   D'ABORD : LANCER pip install psycopg2 DANS LE TERMINAL DE LA MACHINE PAS DE VSCODE
#  / !! \
# /  !!  \
# --------

import psycopg2

# classe pour intéragir avec la database de PostGre
class PostGre:
    def __init__(self, host, database, user, password):
        """
        Définie les parametres pour la connection à la 
        database de postgre
        """
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def connection(self):
        """
        Création de la connection à la database postgre
        """
        return psycopg2.connect(
            host = self.host,
            database = self.database,
            user = self.user,
            password = self.password)

    def creer_table(self, table, colonnes: list, types: list):
        """
        Méthode pour créer une table : 
            - Il faut mettre la liste des colonnes en parametre
            - Il faut mettre la liste des types des colonnes en parametre
        """
        conn = self.connection()
        cur = conn.cursor()
        colonnes_def = ", ".join(f'"{col.lower()}" {typ}' for col, typ in zip(colonnes, types)) # * Créer une chaîne de charactères avec la colonne et son type
        sql = f'CREATE TABLE IF NOT EXISTS "{table}" ({colonnes_def})'
        cur.execute(sql)
        cur.close()
        conn.commit()
        conn.close()

    def inserer(self, table, valeurs: list, colonnes: list):
        """
        Méthode pour insérer des valeurs dans une BD :
            - Il faut mettre la liste des valeurs à mettre en parametre
        """
        conn = self.connection()
        cur = conn.cursor()
        colonnes_def = ", ".join(f'"{col.lower()}"' for col in colonnes) # * Créer une chaîne de charactères avec la colonne et son type
        placeholders = ", ".join(["%s"] * len(valeurs))
        sql = f'INSERT INTO "{table}" ({colonnes_def}) VALUES ({placeholders})'
        cur.execute(sql, valeurs)
        cur.close()
        conn.commit()
        conn.close()

    def afficher(self, table, champs: list):
        """
        Méthode pour afficher le contenu d'une table de la database
        permet de tester si le contenu d'une table est présent dans la database
        (et le contenu est bon)
        """
        conn = self.connection()
        cur = conn.cursor()
        champs_def = ", ".join(f'"{c.lower()}"' for c in champs)
        sql = f'SELECT {champs_def} FROM "{table}"'
        cur.execute(sql)
        lignes = cur.fetchall()
        for ligne in lignes:
            print(ligne)
        cur.close()
        conn.close()

    def supprimer(self, table):
        """
        Méthode pour supprimer une table
        """
        conn = self.connection()
        cur = conn.cursor()
        sql = f"DROP TABLE {table}"
        cur.execute(sql)
        conn.commit()
        conn.close()