import logging
from todolist.Tache import Tache

# Initialize logging
logging.basicConfig(level=logging.INFO)

class ToDoList:
    """Class to manage a list of Taches."""

    def __init__(self):
        """Initialize a new ToDoList object."""
        self.liste_taches = []

    def afficher(self, tache):
        """Display a Tache."""
        try:
            print(tache)
        except Exception as e:
            logging.error(f"Error displaying Tache: {e}")

    def ajouter(self, tache):
        """Add a Tache to the list."""
        try:
            self.liste_taches.append(tache)
            logging.info(f"Tache added: {tache}")
        except Exception as e:
            logging.error(f"Error adding Tache: {e}")

    def supprimer(self, tache):
        """Remove a Tache from the list."""
        try:
            self.liste_taches.remove(tache)
            logging.info(f"Tache removed: {tache}")
        except Exception as e:
            logging.error(f"Error removing Tache: {e}")

    def terminer(self, tache):
        """Complete a Tache."""
        try:
            tache.status = Tache.Status.TERMINER
            logging.info(f"Tache completed: {tache}")
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
            logging.info(f"Tache modified: {tache}")
        except Exception as e:
            logging.error(f"Error modifying Tache: {e}")
