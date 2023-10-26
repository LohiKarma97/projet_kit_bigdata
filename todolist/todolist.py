import argparse
import logging
from todolist.Tache import Tache, TacheStatus
import json
import os

class ToDoList:
    """Class to manage a list of Taches."""

    def __init__(self):
        """Initialize a new ToDoList object."""
        self._task_list = []
        self.open_ToDoList()

    def _check_tache_consistency(self, tache: Tache):
        """Check if a Tache is consistent."""

        if tache.status == None:
            raise ValueError("Provided Tache has wrong status.")

        if tache.nom == None or tache.nom == "":
            raise ValueError("Provided Tache has no name.")

        if tache.description == None or tache.description == "":
            raise ValueError("Provided Tache has no description.")

        if tache.horodatage == None or tache.horodatage == "":
            raise ValueError("Provided Tache has no horodatage.")

        if tache.projet == None or tache.projet == "":
            raise ValueError("Provided Tache has no projet.")

    def _is_in_list(self, tache: Tache):
        """Check if a Tache is in the list."""
        if tache in self._task_list:
            return True
        else:
            return False

    def _name_exist(self, tache: str):
        """Check if a Tache is in the list.
        Return the Tache if it exist, else return None"""
        for t in self._task_list:
            if t.nom == tache:
                return t
        return None

    def display_list(self, status: TacheStatus = None):
        """ Display all Task from list
        If status is provided, display only Task with this status"""
        tasks_to_display = []
        try:
            if self._task_list == []:
                logging.debug("Empty list")
            else:
                for tache in self._task_list:
                    if (status == None or tache.status == status):
                        tasks_to_display.append(str(tache))

        except Exception as e:
            logging.error(f"Error displaying Tache: {e}")

        return  tasks_to_display

    def display(self, tache_name: str):
        """Display a Tache."""
        try:

            t = self._name_exist(tache_name)

            if t == None:
                logging.debug("Tache not found")
            else:
                print(t)

        except Exception as e:
            logging.error(f"Error displaying Tache en cours: {e}")

    def add(self, tache: Tache):
        """Add a Tache to the list."""
        try:
            self._check_tache_consistency(tache)

            if self._is_in_list(tache):
                raise ValueError("Provided Tache is already in the list.")

            if self._name_exist(tache.nom) != None:
                raise ValueError(
                    "A Tache with same name is already in the list.")

            self._task_list.append(tache)
            logging.debug(f"Tache added: {tache}")

        except Exception as e:
            logging.error(f"Error adding Tache: {e}")

    def delete(self, tache_name: str):
        """Remove a Tache from the list."""
        try:
            tache = self._name_exist(tache_name)

            if tache == None:
                raise ValueError("Provided Tache is not in the list.")

            self._task_list.remove(tache)
            logging.debug(f"Tache removed: {tache}")

        except Exception as e:
            logging.error(f"Error removing Tache: {e}")

    def completed(self, tache_name: str):
        """Complete a Tache."""
        try:
            tache = self._name_exist(tache_name)

            if tache == None:
                raise ValueError("Provided Tache is not in the list.")

            if tache.status == TacheStatus.COMPLETED:
                raise ValueError("Provided Tache is already completed.")

            print('Complete method is called')
            tache.status = TacheStatus.COMPLETED
            logging.debug(f"Tache completed: {tache}")

        except Exception as e:
            logging.error(f"Error completing Tache: {e}")

    def modified(self, tache_name: str, projet: str | None = None, horodatage=None, nom: str | None = None, description: str | None = None, status: TacheStatus = None):
        """Modify a Tache."""
        try:
            tache = self._name_exist(tache_name)

            if tache == None:
                raise ValueError(
                    f"Tache with name {tache_name} is not in the list.")

            if not any([projet, horodatage, nom, description, status]):
                raise ValueError("No arguments provided to modify Tache.")

            if projet:
                tache.projet = projet
            if horodatage:
                tache.horodatage = horodatage
            if nom:
                tache.nom = nom
            if description:
                tache.description = description
            if status:
                tache.status = TacheStatus(status)

            logging.debug(f"Tache modified: {tache}")
        except Exception as e:
            logging.error(f"Error modifying Tache: {e}")

    def save_ToDoList(self, file: str = 'data.json'):
        """Save the ToDoList in a file.

        Args:
            file (str, optional): file path. Defaults to 'data.json'.
        """
        try:
            data = []
            for t in self._task_list:
                data.append(t.to_dict())
            with open(file, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            logging.error(f"Error saving file: {e}")

    def open_ToDoList(self, file: str = 'data.json'):
        """Open a file and load the ToDoList.

        Args:
            file (str, optional): file path. Defaults to 'data.json'.

        Returns:
            _type_: _description_
        """
        try:
            if not os.path.exists(file):
                logging.debug(f"'{file}' does not exist. A new file will be created upon saving.")
                return
            
            with open(file, 'r') as f:
                data = json.load(f)

            status_method = {'en cours': TacheStatus.EN_COURS,
                             'completed': TacheStatus.COMPLETED,
                             'à faire': TacheStatus.A_FAIRE}
            for t in data:
                t_recup = Tache(nom=t['nom'],
                                description=t['description'],
                                status=status_method[t['status']],
                                projet=t['projet'],
                                horodatage=t['horodatage'])
                logging.debug(f"Parsed tache: {t_recup}")

                self.add(t_recup)
        except Exception as e:
            logging.error(f"Error opening file: {e}")


def main():
    parser = argparse.ArgumentParser(description='Manage a simple ToDo List.')

    # Primary Actions
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument('-a', '--add', action='store_true', help='Add a new task')
    action_group.add_argument('-m', '--modify', action='store_true', help='Modify an existing task')
    action_group.add_argument('-d', '--delete', action='store_true', help='Delete a task')
    action_group.add_argument('-l', '--list', action='store_true', help='List all tasks')
    action_group.add_argument('-t', '--terminate', action='store_true', help='Mark a task as completed')

    # Task Attributes
    parser.add_argument('--nom', type=str, help='Name of the task')
    parser.add_argument('--description', type=str, default="No description provided", help='Description of the task')
    parser.add_argument('--status', type=str, choices=['en cours', 'completed', 'à faire'], default='à faire', help='Status of the task')
    parser.add_argument('--projet', type=str, default="Default Project", help='Project associated with the task')

    args = parser.parse_args()

    todo_list = ToDoList()

    if args.add:
        if not args.nom:
            logging.error("Error: The name of the task (--nom) is required to add a task.")
            return
        tache = Tache(nom=args.nom, description=args.description, status=TacheStatus(args.status), projet=args.projet)
        todo_list.add(tache)
        print(f"Added task: {args.nom}")
        todo_list.save_ToDoList()

    elif args.modify:
        if not args.nom:
            logging.error("Error: The name of the task (--nom) is required to modify a task.")
            return
        todo_list.modified(args.nom, description=args.description, status=args.status, projet=args.projet)
        print(f"Modified task: {args.nom}")
        todo_list.save_ToDoList()

    elif args.delete:
        # Ensure '--nom' is provided
        if not args.nom:
            logging.error("Error: The name of the task (--nom) is required to delete a task.")
            return
        todo_list.delete(args.nom)
        print(f"Deleted task: {args.nom}")
        todo_list.save_ToDoList()

    elif args.list:
        tasks = todo_list.display_list()
        if tasks:
            print("Current tasks:")
            for task in tasks:
                print(task)
        else:
            print("No current tasks.")

    elif args.terminate:
        if not args.nom:
            print("Error: The name of the task (--nom) is required to mark a task as complete.")
            return
        todo_list.completed(args.nom)
        todo_list.save_ToDoList()
        print(f"Task {args.nom} marked as complete.")


if __name__ == "__main__":
    main()
