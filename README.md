# KitBigData_Todolist
Projet Kit big data

L'objectif de ce projet est de mettre en pratique les concepts et les compétences que vous
avez appris en cours sur le développement Python pour la production et créer une
bibliothèque Python complète de tâches personnelles (To-Do List).
Vous allez vous concentrer sur la structure du projet, la gestion de l'environnement Python
avec Poetry, la programmation orientée objet, le type hinting, la gestion des logs, le respect
des normes PEP 8, la gestion des exceptions, la sécurité, les tests unitaires avec pytest, le
test coverage, la documentation avec Sphinx, et la mise en place d'un pipeline CI/CD avec
GitHub Actions.

# Comment executer les tests
```python3 -m unittest tests/test_tache.py```

# Poetry
pip install poetry (linux command -slide 18)
poetry install (dl l'environement)
poetry env info (vérifier la config, notamment path)
projet shell (let's begin !)
poetry show (statut des dépendances)
poetry export -f requirements.txt > requirements.txt

NB : .venv dans le repo avec 'poetry config virtualenvs.in-project true'
.gitignore déplacé au root du repo

# PEP8
utilisation de flake8
poetry add --dev flake8
poetry run flake8 (vérifie le code)

A faire :
setup.py Poetry pour gestion des versions
Instaurer règles PEP8
Type Hinting
Insérer des loggings & gestion des exceptions
Vérifier sécurité
Etoffer tests unitaire
Test coverage
CI/CD
Documentation !