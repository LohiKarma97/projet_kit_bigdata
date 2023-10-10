import logging
from enum import Enum
from typing import Union

# Configure le logging
logging.basicConfig(level=logging.INFO)

class TaskStatus(Enum):
    """Enumeration for Task Status.
    
    Attributes:
        EN_COURS: Task is ongoing.
        TERMINER: Task is completed.
        A_FAIRE: Task is yet to be started.
    """
    EN_COURS = "en cours"
    TERMINER = "terminer"
    A_FAIRE = "à faire"

class Task:
    """Task class to manage tasks.
    
    Attributes:
        status (TaskStatus): The status of the task.
        projet (str): The project to which the task belongs.
        horodatage (Union[int, str]): The timestamp of the task.
        Nom (str): The name of the task.
        Description (str): The description of the task.
    """
    
    def __init__(self, status: TaskStatus, projet: str, horodatage: Union[int, str], Nom: str, Description: str):
        """Initializes a Task object.
        
        Args:
            status (TaskStatus): The status of the task.
            projet (str): The project to which the task belongs.
            horodatage (Union[int, str]): The timestamp of the task.
            Nom (str): The name of the task.
            Description (str): The description of the task.
            
        Raises:
            ValueError: If the timestamp is negative.
        """
        self.status = status
        self.projet = projet
        self.Nom = Nom
        self.Description = Description

        if isinstance(horodatage, int) and horodatage >= 0:
            self.horodatage = horodatage
            logging.info(f"Task '{self.Nom}' a été créé avec succès.")
        else:
            logging.error("L'horodatage doit être un entier non négatif.")
            raise ValueError("L'horodatage doit être un entier non négatif.")

    def __str__(self):
        """Returns a string representation of the Task object."""
        return f"Task(status={self.status}, projet={self.projet}, horodatage={self.horodatage}, Nom={self.Nom}, Description={self.Description})"

# Exemple d'utilisation
try:
    t1 = Task(TaskStatus.EN_COURS, "Projet A", 1633897200, "Tâche 1", "Cette tâche est la première.")
    print(t1)
    
    t2 = Task(TaskStatus.A_FAIRE, "Projet B", -1633998200, "Tâche 2", "Cette tâche est la deuxième.")
    print(t2)
except ValueError as e:
    logging.error(f"Une erreur s'est produite: {e}")
