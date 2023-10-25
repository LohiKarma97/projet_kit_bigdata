import unittest
import logging
# Remplacez 'your_module' par le nom du module où se trouve votre classe Tache
from todolist.Tache import Tache, TacheStatus
from unittest.mock import patch, MagicMock

class TestTache(unittest.TestCase):

    def print_test(func):
        def wrapper(*args, **kwargs):
            print('\nTACHE - Launching :', func.__name__)
            return func(*args, **kwargs)
        return wrapper

    @print_test
    def test_init_valid(self):
        try:
            t = Tache("Tâche 1", "Description 1", TacheStatus.EN_COURS,
                      "Projet A", 1633897200)
            self.assertEqual(t.status, TacheStatus.EN_COURS)
            self.assertEqual(t.projet, "Projet A")
            self.assertEqual(t.horodatage, 1633897200)
            self.assertEqual(t.nom, "Tâche 1")
            self.assertEqual(t.description, "Description 1")
        except Exception as e:
            self.fail(f"Initialization with valid arguments failed: {e}")

    @print_test
    def test_init_invalid_horodatage(self):
        with self.assertRaises(ValueError):
            Tache("Tâche 2", "Description 2",
                  TacheStatus.A_FAIRE, "Projet B", -10)

    @print_test
    def test_afficher(self) -> None:
        """Test showing a task."""
        tache = Tache(nom="Test Task", description="This is a test task.")

        with patch("builtins.print") as mock_print:
            tache.afficher()

        mock_print.assert_called_once_with(tache)
        logging.debug("Task displayed successfully.")


    @print_test
    def test_modifier(self):
        """Test modifying a task."""
        tache = Tache(nom="Test Task", description="This is a test task.")
        tache.modifier(tache, projet="New Project", nom="New Name", description="New Description")
        self.assertEqual(tache.projet, "New Project")
        self.assertEqual(tache.nom, "New Name")
        self.assertEqual(tache.description, "New Description")

    '''@print_test
    def test_modifier_exception(self):
        """Test exception handling when modifying a task."""
        tache = Tache(nom="Test Task", description="This is a test task.")
        with patch.object(tache, "nom", side_effect=Exception("Test Exception")):
            with self.assertLogs(level="ERROR") as cm:
                self.todo_list.modifier(tache, nom="New Name")
            self.assertIn("Error modifying Tache: Test Exception", cm.output)'''

    @print_test
    def test_terminer(self) -> None:
        """Test marking a task as terminated."""
        tache = Tache(nom="Test Task", description="This is a test task.")
        tache.terminer()
        self.assertEqual(tache.status, TacheStatus.TERMINER)
        logging.debug("Task marked as terminated successfully.")

    @print_test
    def test_terminer_exception(self):
        """Test exception handling when terminating a task."""

        # Using a string instead of a Tache instance to trigger the ValueError.
        non_tache_object = "This is not a Tache instance."
        
        #with self.assertLogs(level="ERROR") as cm:
        #    self.assertLogs(non_tache_object.terminer(),"Provided object is not a Tache instance.")
        #    self.non_tache_object.terminer()

        # Check if the expected error message appears in the logs.
        #self.assertTrue(any(
        #    "Error completing Tache: Provided object is not a Tache instance." in log for log in cm.output))
      
    @print_test
    def test_str_representation(self):
        t = Tache("Tâche 3", "Description 3", TacheStatus.EN_COURS,
                  "Projet C", 1633897300)
        expected_str = "Tache(status=TacheStatus.EN_COURS, projet=Projet C, horodatage=1633897300, nom=Tâche 3, description=Description 3)"
        self.assertEqual(str(t), expected_str)


if __name__ == '__main__':
    unittest.main()
