import logging
from enum import Enum
from typing import Union

# Configure le logging
logging.basicConfig(level=logging.INFO)


class TacheStatus(Enum):
    """Enumeration for Tache Status.

    Attributes:
        EN_COURS: Tache is ongoing.
        TERMINER: Tache is completed.
        A_FAIRE: Tache is yet to be started.
    """
    EN_COURS = "en cours"
    TERMINER = "terminer"
    A_FAIRE = "à faire"


class Tache:
    """Tache class to manage Taches.

    Attributes:
        status (TacheStatus): The status of the Tache.
        projet (str): The project to which the Tache belongs.
        horodatage (Union[int, str]): The timestamp of the Tache.
        Nom (str): The name of the Tache.
        Description (str): The description of the Tache.
    """

    def __init__(self, status: TacheStatus, projet: str, horodatage: Union[int, str], nom: str, description: str):
        """Initializes a Tache object.

        Args:
            status (TacheStatus): The status of the Tache.
            projet (str): The project to which the Tache belongs.
            horodatage (Union[int, str]): The timestamp of the Tache.
            Nom (str): The name of the Tache.
            Description (str): The description of the Tache.

        Raises:
            ValueError: If the timestamp is negative.
        """
        self.status = status
        self.projet = projet
        self.nom = nom
        self.description = description

        if isinstance(horodatage, int) and horodatage >= 0:
            self.horodatage = horodatage
            logging.info(f"Tache '{self.Nom}' a été créé avec succès.")
        else:
            logging.error("L'horodatage doit être un entier non négatif.")
            raise ValueError("L'horodatage doit être un entier non négatif.")

    def __str__(self):
        """Returns a string representation of the Tache object."""
        return f"Tache(status={self.status}, projet={self.projet}, horodatage={self.horodatage}, Nom={self.nom}, Description={self.description})"


# Exemple d'utilisation
try:
    t1 = Tache(TacheStatus.EN_COURS, "Projet A", 1633897200,
               "Tâche 1", "Cette tâche est la première.")
    print(t1)

    t2 = Tache(TacheStatus.A_FAIRE, "Projet B", -1633998200,
               "Tâche 2", "Cette tâche est la deuxième.")
    print(t2)
except ValueError as e:
    logging.error(f"Une erreur s'est produite: {e}")
