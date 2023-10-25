import logging
from enum import Enum
from typing import Union
import time

# Configure le logging
# logging.basicConfig(level=logging.INFO)


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
        nom (str): The name of the Tache.
        description (str): The description of the Tache.
    """

    def __init__(self, nom: str, description: str, status: TacheStatus = TacheStatus.A_FAIRE, projet: str = "Default Project", horodatage: Union[int, str, float] = time.time()):
        """Initializes a Tache object.

        Args:
            id:The 
            status (TacheStatus): The status of the Tache.
            projet (str): The project to which the Tache belongs.
            horodatage (Union[int, str]): The timestamp of the Tache.
            nom (str): The name of the Tache.
            description (str): The description of the Tache.

        Raises:
            ValueError: If the timestamp is negative.
        """
        self.status = status
        self.projet = projet
        self.nom = nom
        self.description = description

        if isinstance(horodatage, int):
            if horodatage >= 0:
                self.horodatage = horodatage
                logging.debug(f"Tache '{self.nom}' a été créé avec succès.")
            else:
                logging.error("L'horodatage doit être un entier non négatif.")
                raise ValueError(
                    "L'horodatage doit être un entier non négatif.")
        else:
            self.horodatage = int(time.time())
            logging.debug(
                f"Tache '{self.nom}' a été créé avec succès - horodatage par défault.")

    def afficher(self):
        """Display a Tache."""
        print(self)

    def terminer(self):
        """Complete a Tache."""
        try:
            if not isinstance(self, Tache):
                raise ValueError("Provided object is not a Tache instance.")
            self.status = TacheStatus.TERMINER
            logging.debug(f"Tache completed: {self}")
        except Exception as e:
            logging.error(f"Error completing Tache: {e}")

    def modifier(self, tache, projet=None, horodatage=None, nom=None, description=None):
        """Modify a Tache."""
        try:
            if projet:
                tache.projet = projet
            if horodatage:
                tache.horodatage = horodatage
            if nom:
                tache.nom = nom
            if description:
                tache.description = description
            logging.debug(f"Tache modified: {tache}")
        except Exception as e:
            logging.error(f"Error modifying Tache: {e}")
                      
    def __str__(self):
        """Returns a string representation of the Tache object."""
        return f"Tache(status={self.status}, projet={self.projet}, horodatage={self.horodatage}, nom={self.nom}, description={self.description})"

