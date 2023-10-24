import unittest
import logging
from todolist.todolist import ToDoList
from todolist.Tache import Tache, TacheStatus
from unittest.mock import patch, MagicMock

# Initialize logging for the test module
logging.basicConfig(level=logging.INFO)


class TestToDoList(unittest.TestCase):

    def print_test(func):
        def wrapper(*args, **kwargs):
            print('\nTODOLIST - Launching :', func.__name__)
            return func(*args, **kwargs)
        return wrapper

    @print_test
    def test_init_valid(self):
        try:
            todo = ToDoList()
            self.assertEqual(todo.liste_taches, [])
        except Exception as e:
            self.fail(
                f"Initialization ToDoList with valid arguments failed: {e}")

    @print_test
    def setUp(self) -> None:
        """Setup a new ToDoList for each test."""
        self.todo_list = ToDoList()

    @print_test
    def test_ajouter(self) -> None:
        """Test adding a new task."""
        tache = Tache(nom="Test Task", description="This is a test task.")
        self.todo_list.ajouter(tache)
        self.assertIn(tache, self.todo_list.liste_taches)
        logging.info("Task added successfully.")

    @print_test
    def test_ajouter_exception(self):
        """Test exception handling when adding a new task."""
        self.todo_list.liste_taches = MagicMock()
        self.todo_list.liste_taches.append.side_effect = Exception(
            "Test Exception")

        with self.assertLogs(level="ERROR") as cm:
            self.todo_list.ajouter("Test Task")
        self.assertIn(
            "ERROR:root:Error adding Tache: Test Exception", cm.output)

    @print_test
    def test_modifier(self):
        """Test modifying a task."""
        tache = Tache(nom="Test Task", description="This is a test task.")
        self.todo_list.ajouter(tache)

        self.todo_list.modifier(
            tache, projet="New Project", nom="New Name", description="New Description")
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
        self.todo_list.ajouter(tache)
        self.todo_list.terminer(tache)
        self.assertEqual(tache.status, TacheStatus.TERMINER)
        logging.info("Task marked as terminated successfully.")

    @print_test
    def test_terminer_exception(self):
        """Test exception handling when terminating a task."""

        # Using a string instead of a Tache instance to trigger the ValueError.
        non_tache_object = "This is not a Tache instance."

        with self.assertLogs(level="ERROR") as cm:
            self.todo_list.terminer(non_tache_object)

        # Check if the expected error message appears in the logs.
        self.assertTrue(any(
            "Error completing Tache: Provided object is not a Tache instance." in log for log in cm.output))

    @print_test
    def test_supprimer(self) -> None:
        """Test deleting a task."""
        tache = Tache(nom="Test Task", description="This is a test task.")
        self.todo_list.ajouter(tache)
        self.todo_list.supprimer(tache)
        self.assertNotIn(tache, self.todo_list.liste_taches)
        logging.info("Task deleted successfully.")

    @print_test
    def test_supprimer_exception(self):
        """Test exception handling when removing a task."""

        # Using a string instead of a Tache instance to trigger the ValueError.
        non_tache_object = "This is not a Tache instance."

        with self.assertLogs(level="ERROR") as cm:
            with self.assertRaises(ValueError):
                self.todo_list.supprimer(non_tache_object)

        # Check if the expected error message appears in the logs.
        self.assertTrue(any(
            "Error removing Tache: Provided object is not a Tache instance." in log for log in cm.output))

    @print_test
    def test_afficher(self) -> None:
        """Test showing the ongoing task."""
        tache = Tache(nom="Test Task", description="This is a test task.")

        with patch("builtins.print") as mock_print:
            self.todo_list.afficher(tache)

        mock_print.assert_called_once_with(tache)
        logging.info("Task displayed successfully.")


if __name__ == '__main__':
    unittest.main()
