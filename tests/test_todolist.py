import unittest
import os
from todolist.todolist import ToDoList
from todolist.Tache import Tache, TacheStatus
from unittest.mock import patch, MagicMock, Mock, ANY
from todolist.todolist import main

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
        # Add a task to the list
        self.todo_list._task_list.append(self.tache1)
        
        # Call the display_list method
        tasks = self.todo_list.display_list()
        
        # Verify that the returned list contains the added task's string representation
        self.assertIn(str(self.tache1), tasks)

    @patch('logging.debug')
    def test_display_list_empty(self, mock_debug):
        # Clear the task list for this test
        self.todo_list._task_list = []

        self.todo_list.display_list()
        mock_debug.assert_called_with("Empty list")

    @patch('logging.error')
    @patch('logging.debug')
    def test_display_list_success(self, mock_debug, mock_error):

        # Add two tasks to the list
        self.todo_list._task_list.append(self.tache1)
        self.todo_list._task_list.append(self.tache2)

        # Call the display_list method
        tasks = self.todo_list.display_list()

        # Verify that the returned list contains the added tasks' string representations
        self.assertIn(str(self.tache1), tasks)
        self.assertIn(str(self.tache2), tasks)

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

    @patch('logging.debug')
    def test_open_ToDoList_non_existent_file(self, mock_debug):
        """Test opening a non-existent file."""
        if os.path.exists('nonexistent.json'):
            os.remove('nonexistent.json')
        self.todo_list.open_ToDoList(file='nonexistent.json')
        
        # Check if logging.debug was called with the expected message
        mock_debug.assert_called_with("'nonexistent.json' does not exist. A new file will be created upon saving.")


    @patch('logging.error')
    def test_open_ToDoList_empty_file(self, mock_error):
        """Test opening an empty file."""
        with open('empty.json', 'w') as f:
            f.write('')
        self.todo_list.open_ToDoList(file='empty.json')
        mock_error.assert_called_with("Error opening file: Expecting value: line 1 column 1 (char 0)")
        os.remove('empty.json')

    @patch('logging.error')
    def test_open_ToDoList_invalid_data(self, mock_error):
        """Test opening a file with invalid JSON data."""
        with open('invalid.json', 'w') as f:
            f.write("{invalid_json")
        self.todo_list.open_ToDoList(file='invalid.json')
        mock_error.assert_called_with("Error opening file: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)")
        os.remove('invalid.json')

class TestCLI(unittest.TestCase):

    def setUp(self):
        """Setup for each test."""
        # If there's any shared setup, put it here.
        pass


    @patch('todolist.todolist.ToDoList.add')
    @patch('todolist.todolist.argparse.ArgumentParser.parse_args')
    def test_cli_add_task_with_status(self, mock_args, mock_add):
        """Test the CLI add task with name and status."""
        
        mock_args.return_value = MagicMock(nom="Test Task", description=None, status="en cours", add=True, projet=None, modify=False, delete=False, list=False, terminate=False)

        main()

        # Get the Tache instance from the mock_add call arguments
        tache_instance = mock_add.call_args[0][0]  # This fetches the first positional argument passed to mock_add

        # Now, assert against the attributes of the Tache instance
        self.assertEqual(tache_instance.nom, "Test Task")
        self.assertEqual(tache_instance.status, TacheStatus.EN_COURS)


    @patch('todolist.todolist.ToDoList.add')
    @patch('todolist.todolist.argparse.ArgumentParser.parse_args')
    def test_cli_add_task_with_description(self, mock_args, mock_add):
        """Test the CLI add task with name and description."""
        
        mock_args.return_value = MagicMock(nom="Test Task", description="Test Description", status="en cours", add=True, projet=None, modify=False, delete=False, list=False, terminate=False)

        main()

        # Get the Tache instance from the mock_add call arguments
        tache_instance = mock_add.call_args[0][0]

        # Now, assert against the attributes of the Tache instance
        self.assertEqual(tache_instance.nom, "Test Task")
        self.assertEqual(tache_instance.description, "Test Description")


    @patch('todolist.todolist.ToDoList.add')
    @patch('todolist.todolist.argparse.ArgumentParser.parse_args')
    def test_cli_add_task_with_status(self, mock_args, mock_add):
        """Test the CLI add task with name and status."""
        
        mock_args.return_value = MagicMock(nom="Test Task", description=None, status="en cours", add=True, projet=None, modify=False, delete=False, list=False, terminate=False)

        main()

        # Get the Tache instance from the mock_add call arguments
        tache_instance = mock_add.call_args[0][0]

        # Now, assert against the attributes of the Tache instance
        self.assertEqual(tache_instance.nom, "Test Task")
        self.assertEqual(tache_instance.status, TacheStatus.EN_COURS)



    @patch('todolist.todolist.ToDoList.add')
    @patch('todolist.todolist.argparse.ArgumentParser.parse_args')
    def test_cli_add_task_all_args(self, mock_args, mock_add):
        """Test the CLI add task with all arguments."""
        
        mock_args.return_value = MagicMock(nom="Test Task", description="Test Description", status="en cours", add=True, projet="Work Project", modify=False, delete=False, list=False, terminate=False)

        main()

        # Get the Tache instance from the mock_add call arguments
        tache_instance = mock_add.call_args[0][0]  # This fetches the first positional argument passed to mock_add

        # Now, assert against the attributes of the Tache instance
        self.assertEqual(tache_instance.nom, "Test Task")
        self.assertEqual(tache_instance.description, "Test Description")
        self.assertEqual(tache_instance.status, TacheStatus.EN_COURS)
        self.assertEqual(tache_instance.projet, "Work Project")

    @patch('todolist.todolist.ToDoList.modified')
    @patch('todolist.todolist.argparse.ArgumentParser.parse_args')
    def test_cli_modify_task_name(self, mock_args, mock_modify):
        """Test the CLI modify task name."""
        mock_args.return_value = MagicMock(nom="Original Task", new_nom="Modified Task", description=None, status=None, add=False, modified=True, delete=False, list=False, completed=False)
        
        main()

        mock_modify.assert_called_with("Original Task", description=None, status=None, projet=ANY)


    @patch('todolist.todolist.ToDoList.modified')
    @patch('todolist.todolist.ToDoList.save_ToDoList')
    @patch('todolist.todolist.logging.error')
    @patch('todolist.todolist.argparse.ArgumentParser.parse_args')
    def test_cli_modify_task_description(self, mock_args, mock_error, mock_save, mock_modified):
        """Test the CLI modify task description."""
        
        mock_args.return_value = MagicMock(nom="Test Task", modify=True, description="Updated Description", status=None, add=False, delete=False, list=False, completed=False)
        
        main()

        mock_modified.assert_called_with('Test Task', description='Updated Description', status=None, projet=ANY)


    @patch('todolist.todolist.ToDoList.modified')
    @patch('todolist.todolist.ToDoList.save_ToDoList')
    @patch('todolist.todolist.logging.error')
    @patch('todolist.todolist.argparse.ArgumentParser.parse_args')
    def test_cli_modify_task_status(self, mock_parse_args, mock_error, mock_save, mock_modified):
        """Test the CLI modify task status."""
        
        # Mock the return value of parse_args
        mock_parse_args.return_value = Mock(nom='Test Task', modify=True, description=None, status='completed', projet=None, add=False, delete=False, list=False, terminate=False)
        
        try:
            main()
        except SystemExit as e:
            self.fail(f"SystemExit was raised: {e}")
        
        mock_modified.assert_called_with('Test Task', description=None, status='completed', projet=None)



    @patch('todolist.todolist.ToDoList.modified')
    @patch('todolist.todolist.argparse.ArgumentParser.parse_args')
    def test_cli_modify_task_multiple_attrs(self, mock_args, mock_modify):
        """Test the CLI modify task with multiple attributes."""
        mock_args.return_value = MagicMock(nom="Test Task", description="New Description", status="completed", add=False, modify=True, delete=False, list=False, completed=False, projet="Mocked Project")
        
        main()

        mock_modify.assert_called_with("Test Task", description="New Description", status="completed", projet="Mocked Project")




if __name__ == '__main__':
    unittest.main()
