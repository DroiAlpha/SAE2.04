# README.md

## Ce dossier contient 8 fichiers : 

- **le fichier acces_api.py** : il contient la classe AccesAPI, pour définir la connection à l'API, et les différentes méthodes pour extraires des données de l'API (colonnes et valeurs) (Développement : Amaury - Optimisation : Théo & Massi - Tests : Clémence)

- **le fichier base_postgres.py** : il contient la classe BasePostgres, pour définir la connection avec la base de données PostgreSQL, ainsi que les différentes actions possibles (création de table et insertion) sur la database, ainsi qu'une fonction d'affichage des données d'une table de la database (Développement : Amaury - Optimisation : Théo & Massi - Tests : Willy)

- **le fichier recup_donnees.py** : il contient **la classe RecupDonnees**, pour définir les **méthodes** nécessaires pour récuperer les données depuis l'API (Développement : Amaury - Optimisation : Théo & Massi - Tests : Clémence)

- **le fichier gestion_donnees.py** : il contient l'exécution du code en thread pour que l'importation des données dans la base de données PostgerSQL soit plus rapide (Développement : Amaury - Optimisation : Théo & Massi - Tests : Willy)

- **le ficher tests_interface.py** : il contient **la classe abstraite TestInterface** qui rassemble l'ensemble tests unitaires à développer **dans le fichier tests.py** (Développement : Amaury - Optimisation : Willy & Clémence)

- **le fichier tests.py** : il contient **la classe Test** dans laquelle sont intégrés les tests unitaires demandés **dans le fichier tests_interface.py** (Développement : Willy & Clémence)

> Modifications effectuées par Clémence :
- README.md : en gras
- fichiers .py : en commentaires (# ? [...])

> Modifications dans l'attente d'une validation par les membres de l'équipe projet et en priorité de :
- Willy pour valider sa partie
- Théo pour vérifier les tests
- Amaury (chef d'équipe) pour donner son accord