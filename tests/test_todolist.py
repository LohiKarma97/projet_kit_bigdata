import unittest
import logging
# Remplacez 'your_module' par le nom du module où se trouve votre classe Tache
from todolist.todolist import ToDoList

class TestToDoList(unittest.TestCase):

    def print_test(func):
        def wrapper(*args, **kwargs):
            print('\nLaunching',func.__name__)
            return func(*args, **kwargs)
        return wrapper
    
    @print_test    
    def test_init_valid(self):
        try:
            todo=ToDoList()
            self.assertEqual(todo.liste_taches, [])
        except Exception as e:
            self.fail(f"Initialization ToDoList with valid arguments failed: {e}")