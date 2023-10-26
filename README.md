# KitBigData_Todolist
Projet Kit big data

L'objectif de ce projet est de mettre en pratique les concepts et les compétences appris en cours sur le développement Python pour la production et créer une
bibliothèque Python complète de tâches personnelles (To-Do List).
Le but étant de couvrir un certain nombre d'étapes clef, notamment: la structure du projet, la gestion de l'environnement Python avec Poetry, la programmation orientée objet, le type hinting, la gestion des logs, le respect des normes PEP 8, la gestion des exceptions, la sécurité, les tests unitaires avec pytest, le test coverage, la documentation avec Sphinx, et la mise en place d'un pipeline CI/CD avec GitHub Actions.

# Installation guide
## install dependencies
- pip install poetry
- apt-install pandoc

# Installation
- poetry install


# User manual
- The TODOLIST consist of a class where the interface is callbable over the api todolist.
- There are 5 methods to manipulate a todolist
- Each task has several attributes : --nom, --description, --status, --projet, --horodatage

## Usage example : (from todolist directory)
- Add a new task to the list : ```todolist -a --nom "<nom>" --description "<description>"```
- Modify an existing task : ```todolist -m --nom "<nom>" --<attribute to change> ...```
- Delete an existing task : ```todolist -d --nom "<nom>"```
- Get the list of tasks : ```todolist -l```
- Terminate an existing task: ```todolist -t --nom "<nom>"```

# Developper manual
## Testing
- ```python3 -m unittest tests/test_tache.py```
- ```python3 -m unittest tests/test_todolist.py```
## Coverage
- ```poetry run python -m coverage run -m unittest tests/test_tache.py```
- ```poetry run python -m coverage run -a -m unittest tests/test_todolist.py```
- ```poetry run python -m coverage report```

## Documentation Sphinx
- Generate the doc (all .rst are update automaticaly through 'conf.py')
   poetry run make -C docs html
- Access the doc : search for 'index.html' in '.docs/html'
