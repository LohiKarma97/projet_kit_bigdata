import logging
from todolist.Tache import Tache, TacheStatus
import json

# Initialize logging
# logging.basicConfig(level=logging.INFO)


class ToDoList:
    """Class to manage a list of Taches."""

    def __init__(self):
        """Initialize a new ToDoList object."""
        self.liste_taches = []

    def afficher_taches_en_cours(self):
        """Display Tache in ToDoList which status is "en cours" ."""
        try:
            for t in self.liste_taches:
                # print(t.__str__())
                if t.status == TacheStatus.EN_COURS:
                    # A filtrer pour avoir uniquepment taches actives
                    print(t.afficher())
        except Exception as e:
            logging.error(f"Error displaying Tache en cours: {e}")

    def ajouter(self, tache):
        """Add a Tache to the list."""
        try:
            self.liste_taches.append(tache)
            logging.debug(f"Tache added: {tache}")
        except Exception as e:
            logging.error(f"Error adding Tache: {e}")

    def supprimer(self, tache):
        """Remove a Tache from the list."""
        if not isinstance(tache, Tache):
            logging.error(
                "Error removing Tache: Provided object is not a Tache instance.")
            raise ValueError("Provided object is not a Tache instance.")

        try:
            self.liste_taches.remove(tache)
            logging.debug(f"Tache removed: {tache}")
        except Exception as e:
            logging.error(f"Error removing Tache: {e}")

    def save_ToDoList(self, file: str = 'data.json'):  # quel est l'output type ?
        data = []
        for t in self.liste_taches:
            data.append(t.to_dict())
        with open(file, 'w') as f:
            json.dump(data, f)

    def open_ToDoList(self, file: str = 'data.json'):  # l'output = list ?
        with open(file, 'r') as f:
            data = json.load(f)
        temp = ToDoList()
        for t in data:
            t_recup = Tache(nom=t['nom'],
                            description=t['description'],
                            status=t['status'],
                            projet=t['projet'],
                            horodatage=t['horodatage'])
            temp.ajouter(t_recup)
        return temp
