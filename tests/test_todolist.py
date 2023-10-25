import unittest
import logging
from todolist.todolist import ToDoList
from todolist.Tache import Tache, TacheStatus
from unittest.mock import patch, MagicMock, call

# Initialize logging for the test module
# logging.basicConfig(level=logging.INFO)


class TestToDoList(unittest.TestCase):

    def setUp(self) -> None:
        """Setup a new ToDoList for each test."""
        self.todo_list = ToDoList()
        
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
    def test_ajouter(self) -> None:
        """Test adding a new task."""
        tache = Tache(nom="Test Task", description="This is a test task.")
        self.todo_list.ajouter(tache)
        self.assertIn(tache, self.todo_list.liste_taches)
        logging.debug("Task added successfully.")

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
    def test_supprimer(self) -> None:
        """Test deleting a task."""
        tache = Tache(nom="Test Task", description="This is a test task.")
        self.todo_list.ajouter(tache)
        self.todo_list.supprimer(tache)
        self.assertNotIn(tache, self.todo_list.liste_taches)
        logging.debug("Task deleted successfully.")

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
    def test_afficher_taches_en_cours(self) -> None:
        """Test showing the ongoing task."""
        tache1 = Tache(nom="Test Task", description="This is a test task.",status=TacheStatus.EN_COURS)
        tache2 = Tache(nom="Test Task", description="This is a test task.",status=TacheStatus.A_FAIRE)
        self.todo_list = ToDoList()
        self.todo_list.ajouter(tache1)
        self.todo_list.ajouter(tache2)
        self.todo_list.afficher_taches_en_cours()
        
        with patch("builtins.print") as mock_print:
            self.todo_list.afficher_taches_en_cours()
        
        assert mock_print.call_args_list[0] == call(str(tache1))
        logging.debug("Task displayed successfully.")


if __name__ == '__main__':
    unittest.main()
