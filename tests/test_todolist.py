import unittest
import os
from todolist.todolist import ToDoList
from todolist.Tache import Tache, TacheStatus
from unittest.mock import patch

# Initialize logging for the test module
# logging.basicConfig(level=logging.INFO)


class TestTacheConsistency(unittest.TestCase):

    def setUp(self):
        self.todo_list = ToDoList()  # Replace with the actual class

    def test_status_none(self):
        tache = Tache(status=None, nom="Test", description="Test Description")
        with self.assertRaises(ValueError):
            self.todo_list._check_tache_consistency(tache)

    def test_name_none(self):
        tache = Tache(status=TacheStatus.A_FAIRE, nom=None,
                      description="Test Description")
        with self.assertRaises(ValueError):
            self.todo_list._check_tache_consistency(tache)

    def test_name_empty(self):
        tache = Tache(status=TacheStatus.A_FAIRE, nom="",
                      description="Test Description")
        with self.assertRaises(ValueError):
            self.todo_list._check_tache_consistency(tache)

    def test_description_none(self):
        tache = Tache(status=TacheStatus.A_FAIRE, nom="Test", description=None)
        with self.assertRaises(ValueError):
            self.todo_list._check_tache_consistency(tache)

    def test_description_empty(self):
        tache = Tache(status=TacheStatus.A_FAIRE, nom="Test", description="")
        with self.assertRaises(ValueError):
            self.todo_list._check_tache_consistency(tache)

    def test_negative_timestamp(self):
        with self.assertRaises(ValueError):
            tache = Tache(status=TacheStatus.A_FAIRE, nom="Test",
                          description="Test Description", horodatage=-1)

    def test_projet_none(self):
        tache = Tache(status=TacheStatus.A_FAIRE, nom="Test",
                      description="Test Description", projet=None)
        with self.assertRaises(ValueError):
            self.todo_list._check_tache_consistency(tache)

    def test_projet_empty(self):
        tache = Tache(status=TacheStatus.A_FAIRE, nom="Test",
                      description="Test Description", projet="")
        with self.assertRaises(ValueError):
            self.todo_list._check_tache_consistency(tache)

    def test_name_exist(self):
        tache = Tache(nom="Test Task", description="This is a test task.")
        self.todo_list._task_list.append(tache)

        result = self.todo_list._name_exist(tache.nom)
        self.assertEqual(result, tache)

        result = self.todo_list._name_exist("this is just a name")
        self.assertEqual(result, None)

    def test_is_in_list(self):
        tache = Tache(nom="Test Task", description="This is a test task.")
        self.todo_list._task_list.append(tache)

        result = self.todo_list._is_in_list(tache)
        self.assertEqual(result, True)

        tache_not_in_list = Tache(
            nom="Test Task2", description="This is a second test task.")
        result = self.todo_list._is_in_list(tache_not_in_list)
        self.assertEqual(result, False)


class TestToDoList(unittest.TestCase):

    def setUp(self) -> None:
        """Setup a new ToDoList for each test."""
        self.todo_list = ToDoList()

    def print_test(func):
        def wrapper(*args, **kwargs):
            print('\nTODOLIST - Launching :', func.__name__)
            return func(*args, **kwargs)
        return wrapper

    def setUp(self):
        self.todo_list = ToDoList()
        self.tache1 = Tache(
            nom="Test Task", description="This is a test task.")
        self.tache2 = Tache(
            nom="Test Task2", description="This is a second test task.")

    @print_test
    def test_add(self):
        self.todo_list.add(self.tache1)
        self.assertIn(self.tache1, self.todo_list._task_list)

    @patch('logging.error')
    @print_test
    def test_add_existing_tache(self, mock_error):
        self.todo_list.add(self.tache1)
        self.todo_list.add(self.tache1)
        mock_error.assert_called_once()

    @patch('logging.error')
    @print_test
    def test_add_tache_with_existing_name(self, mock_error):
        self.todo_list.add(self.tache1)
        tache_duplicate_name = Tache(
            nom="Test Task", description="This is a test task.")
        self.todo_list.add(tache_duplicate_name)
        mock_error.assert_called_once()

    @print_test
    def test_modified(self):
        self.todo_list.add(self.tache1)

        self.todo_list.modified(
            self.tache1.nom, projet="New Project", nom="New Name", description="New Description")
        self.assertEqual(self.tache1.projet, "New Project")
        self.assertEqual(self.tache1.nom, "New Name")
        self.assertEqual(self.tache1.description, "New Description")

    @patch('logging.error')
    def test_modified_tache_not_in_list(self, mock_error):

        self.todo_list.modified('nonexistent_tache_name')
        mock_error.assert_called_with(
            "Error modifying Tache: Tache with name nonexistent_tache_name is not in the list.")

    @patch('logging.error')
    def test_modified_no_args_provided(self, mock_error):
        self.todo_list.add(self.tache1)
        self.todo_list.modified(self.tache1.nom)
        mock_error.assert_called_with(
            "Error modifying Tache: No arguments provided to modify Tache.")

    @print_test
    @patch('logging.debug')
    def test_completed(self, mock_debug):
        self.todo_list.add(self.tache1)
        self.todo_list.completed(self.tache1.nom)
        self.assertEqual(self.tache1.status, TacheStatus.COMPLETED)
        mock_debug.assert_called_with(f"Tache completed: {self.tache1}")

    @patch('logging.error')
    def test_completed_tache_not_in_list(self, mock_error):
        self.todo_list.completed('nonexistent_tache_name')
        mock_error.assert_called_with(
            "Error completing Tache: Provided Tache is not in the list.")

    @patch('logging.error')
    def test_completed_already_completed(self, mock_error):
        self.tache1.status = TacheStatus.COMPLETED
        self.todo_list._task_list.append(self.tache1)  # Add to task list

        self.todo_list.completed(self.tache1.nom)
        mock_error.assert_called_with(
            f"Error completing Tache: Provided Tache is already completed.")

    @patch('logging.error')
    def test_delete_tache_not_in_list(self, mock_error):
        self.todo_list.delete('nonexistent_tache_name')
        mock_error.assert_called_with(
            "Error removing Tache: Provided Tache is not in the list.")

    @patch('logging.debug')
    def test_delete_success(self, mock_debug):
        tache_name = 'existing_tache_name'
        tache = Tache(nom=tache_name, description="Some description")
        # Assuming _task_list is public or use a method to add
        self.todo_list._task_list.append(tache)

        self.todo_list.delete(tache_name)
        mock_debug.assert_called_with(f"Tache removed: {tache}")

    @patch('logging.debug')
    def test_display_tache_not_in_list(self, mock_debug):
        self.todo_list.display('nonexistent_tache_name')
        mock_debug.assert_called_with("Tache not found")

    @patch('builtins.print')
    def test_display_success(self, mock_print):
        # Assuming _task_list is public or use a method to add
        self.todo_list._task_list.append(self.tache1)

        self.todo_list.display(self.tache1.nom)
        mock_print.assert_called_with(self.tache1)

    @patch('logging.debug')
    def test_display_list_empty(self, mock_debug):
        # Clear the task list for this test
        self.todo_list._task_list = []

        self.todo_list.display_list()
        mock_debug.assert_called_with("Empty list")

    @patch('logging.error')
    @patch('logging.debug')
    @patch('builtins.print')
    def test_display_list_success(self, mock_print, mock_debug, mock_error):

        self.todo_list._task_list.append(self.tache1)
        self.todo_list._task_list.append(self.tache2)

        self.todo_list.display_list()

        # Verify that 'print' is called twice: once for each task
        self.assertEqual(mock_print.call_count, 2)

        # Verify the calls contain the correct tache objects
        mock_print.assert_any_call(self.tache1)
        mock_print.assert_any_call(self.tache2)

        # Verify that debug and error logging are not called
        mock_debug.assert_not_called()
        mock_error.assert_not_called()

    def test_save_ToDoList(self):
        self.todo_list.add(self.tache1)
        self.todo_list.add(self.tache2)
        self.todo_list.save_ToDoList()

        # check json file
        with open('data.json', 'r') as f:
            json_file = f.read()
            self.assertIn(self.tache1.nom, json_file)
            self.assertIn(self.tache2.nom, json_file)

        # remove json file
        os.remove('data.json')

    def test_open_ToDoList(self):
        self.todo_list.add(self.tache1)
        self.todo_list.add(self.tache2)
        self.todo_list.save_ToDoList(file='test.json')

        todo_list_recup = ToDoList()
        todo_list_recup.open_ToDoList(file='test.json')

        self.assertEqual(len(todo_list_recup._task_list), 2)
        self.assertEqual(todo_list_recup._task_list[0].nom, self.tache1.nom)
        self.assertEqual(todo_list_recup._task_list[1].nom, self.tache2.nom)

        self.assertEqual(
            todo_list_recup._task_list[0].description, self.tache1.description)
        self.assertEqual(
            todo_list_recup._task_list[1].description, self.tache2.description)

        self.assertEqual(
            todo_list_recup._task_list[0].status, self.tache1.status)
        self.assertEqual(
            todo_list_recup._task_list[1].status, self.tache2.status)

        self.assertEqual(
            todo_list_recup._task_list[0].projet, self.tache1.projet)
        self.assertEqual(
            todo_list_recup._task_list[1].projet, self.tache2.projet)

        self.assertEqual(
            todo_list_recup._task_list[0].horodatage, self.tache1.horodatage)
        self.assertEqual(
            todo_list_recup._task_list[1].horodatage, self.tache2.horodatage)

        # remove json file
        os.remove('test.json')


if __name__ == '__main__':
    unittest.main()
