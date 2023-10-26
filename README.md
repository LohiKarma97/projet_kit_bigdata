# KitBigData_Todolist
Projet Kit big data

L'objectif de ce projet est de mettre en pratique les concepts et les compétences appris en cours sur le développement Python pour la production et créer une
bibliothèque Python complète de tâches personnelles (To-Do List).
Le but étant de couvrir un certain nombre d'étapes clef, notamment: la structure du projet, la gestion de l'environnement Python avec Poetry, la programmation orientée objet, le type hinting, la gestion des logs, le respect des normes PEP 8, la gestion des exceptions, la sécurité, les tests unitaires avec pytest, le test coverage, la documentation avec Sphinx, et la mise en place d'un pipeline CI/CD avec GitHub Actions.

# Installation guide
## Poetry
- pip install poetry
- poetry install
- poetry env info (vérifier la config, notamment path)
- projet shell (let's begin !)
- poetry show (statut des dépendances)
- poetry export -f requirements.txt > requirements.txt

# User manual
- View an example of a ToDoList : 
      TODO=ToDoList()
      TODO.open_ToDoList('data.json')
- Initialize a new todolist : XXXXXXXXXXXXXX
- Add a new task to the list : XXXXXXXXXXXXXX
- Modify an existing task : XXXXXXXXXXXXXX
- Delete an existing task : XXXXXXXXXXXXXX
- Show current tasks : 
- Terminate an existing task: XXXXXXXXXXXXXX
- Show current status of the todolist : XXXXXXXXXXXXXX #A quoi cela corespond-il ?

# Developper manual
## Testing
- ```python3 -m unittest tests/test_tache.py```
- ```python3 -m unittest tests/test_todolist.py```
## Coverage
- ```poetry run python -m coverage run -m unittest tests/test_tache.py```
- ```poetry run python -m coverage run -a -m unittest tests/test_todolist.py```
- '''poetry run python -m coverage report'''

## Documentation Sphinx
- Generate the doc (all .rst are update automaticaly through 'conf.py')
   * cd docs
   * make html
- Access the doc : search for 'index.html' in '.docs/html'
