# !     /\
# !    /  \
# !   / !! \   ATTENTION AVANT LANCEMENT : TAPPER LA COMMANDE pip install psycopg2 DANS LE TERMINAL DE VOTRE MACHINE PAS DE VSCODE
# !  /  !!  \
# !  --------

"""
base_postgres.py : module pour intéragir avec une base de données PostgreSQL
# ? Ajout de commentaires et gestion des erreurs et des exceptions
"""

import psycopg2

class BasePostgres:
    """ 
    Classe pour intéragir avec une base de données PostgreSQL 
    """
    def __init__(self, host, database, user, password):
        """
        Initialise les paramètres de connexion à la base PostgreSQL
        """
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def connection(self):
        """
        Établit une connexion à la base de données PostgreSQL
        """
        try:
            return psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
        except psycopg2.OperationalError as e:
            print(f"[ERREUR] Impossible de se connecter à la base de données : {e}")
            return None
        except Exception as e:
            print(f"[ERREUR] Une erreur inattendue est survenue lors de la connexion : {e}")
            return None

    def creer_table(self, table, colonnes: list, types: list):
        """
        Crée une table dans la base de données PostgreSQL si elle n'existe pas déjà
        Paramètres :
            - table (str) : nom de la table
            - colonnes (list) : liste des noms de colonnes
            - types (list) : liste des types SQL correspondants
        """
        try:
            conn = self.connection()
            cur = conn.cursor()
            colonnes_def = ", ".join(f'"{col.lower()}" {typ}' for col, typ in zip(colonnes, types)) # * Créer une chaîne de charactères avec la colonne et son type
            sql = f'CREATE TABLE IF NOT EXISTS "{table}" ({colonnes_def})'
            cur.execute(sql)
            conn.commit()
        except (psycopg2.DatabaseError, psycopg2.Error) as e:
            print(f"[ERREUR] Impossible de créer la table {table} : {e}")
        except Exception as e:
            print(f"[ERREUR] Une erreur inattendue est survenue lors de la création de la table {table} : {e}")
        finally:
            if cur: cur.close()
            if conn: conn.close()

    def inserer(self, table, valeurs: list, colonnes: list):
        """
        Insère une ligne de valeurs dans une table de la base de données PostgreSQL
        Paramètres :
            - table (str) : nom de la table
            - valeurs (list) : liste des valeurs à insérer
            - colonnes (list) : liste des noms de colonnes correspondantes
        """
        try:
            conn = self.connection()
            cur = conn.cursor()
            colonnes_def = ", ".join(f'"{col.lower()}"' for col in colonnes) # * Créer une chaîne de charactères avec la colonne et son type
            placeholders = ", ".join(["%s"] * len(valeurs))
            sql = f'INSERT INTO "{table}" ({colonnes_def}) VALUES ({placeholders})'
            cur.execute(sql, valeurs)
            conn.commit()
        except (psycopg2.DatabaseError, psycopg2.Error) as e:
            print(f"[ERREUR] Impossible d'insérer les valeurs dans la table {table} : {e}")
        except Exception as e:
            print(f"[ERREUR] Une erreur inattendue est survenue lors de l'insertion dans la table {table} : {e}")
        finally:
            if cur: cur.close()
            if conn: conn.close()

    def afficher(self, table, champs: list):
        """
        Affiche le contenu d'une table de la base de données PostgreSQL
        Permet de vérifier le contenu d'une table
        Paramètres :
            - table (str) : nom de la table
            - champs (list) : liste des noms de colonnes à afficher
        """
        try:
            conn = self.connection()
            cur = conn.cursor()
            champs_def = ", ".join(f'"{c.lower()}"' for c in champs)
            sql = f'SELECT {champs_def} FROM "{table}"'
            cur.execute(sql)
            lignes = cur.fetchall()
            for ligne in lignes:
                print(ligne)
        except (psycopg2.DatabaseError, psycopg2.Error) as e:
            print(f"[ERREUR] Impossible d'afficher le contenu de la table {table} : {e}")
        except Exception as e:
            print(f"[ERREUR] Une erreur inattendue est survenue lors de l'affichage de la table {table} : {e}")
        finally:
            if cur: cur.close()
            if conn: conn.close()

    def supprimer(self, table):
        """
        Supprime une table de la base de données PostgreSQL
        Paramètre :
            - table (str) : nom de la table à supprimer
        """
        try:
            conn = self.connection()
            cur = conn.cursor()
            sql = f"DROP TABLE {table}"
            cur.execute(sql)
            conn.commit()
        except (psycopg2.DatabaseError, psycopg2.Error) as e:
            print(f"[ERREUR] Impossible de supprimer la table {table} : {e}")
        except Exception as e:
            print(f"[ERREUR] Une erreur inattendue est survenue lors de la suppression de la table {table} : {e}")
        finally:
            if cur: cur.close()
            if conn: conn.close()