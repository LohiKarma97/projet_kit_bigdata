import unittest
import logging
from todolist.Tache import Tache, TacheStatus
from todolist.todolist import ToDoList
from unittest.mock import patch

# Initialize logging for the test module
logging.basicConfig(level=logging.INFO)


class TestToDoList(unittest.TestCase):

    def setUp(self) -> None:
        """Setup a new ToDoList for each test."""
        self.todo_list = ToDoList()

    def test_ajouter(self) -> None:
        """Test adding a new task."""
        tache = Tache(nom="Test Task", description="This is a test task.")
        self.todo_list.ajouter(tache)
        self.assertIn(tache, self.todo_list.liste_taches)
        logging.info("Task added successfully.")

    def test_terminer(self) -> None:
        """Test marking a task as terminated."""
        tache = Tache(nom="Test Task", description="This is a test task.")
        self.todo_list.ajouter(tache)
        self.todo_list.terminer(tache)
        self.assertEqual(tache.status, TacheStatus.TERMINER)
        logging.info("Task marked as terminated successfully.")

    def test_supprimer(self) -> None:
        """Test deleting a task."""
        tache = Tache(nom="Test Task", description="This is a test task.")
        self.todo_list.ajouter(tache)
        self.todo_list.supprimer(tache)
        self.assertNotIn(tache, self.todo_list.liste_taches)
        logging.info("Task deleted successfully.")

    def test_afficher(self) -> None:
        """Test showing the ongoing task."""
        tache = Tache(nom="Test Task", description="This is a test task.")

        with patch("builtins.print") as mock_print:
            self.todo_list.afficher(tache)

        mock_print.assert_called_once_with(tache)
        logging.info("Task displayed successfully.")


if __name__ == '__main__':
    unittest.main()
