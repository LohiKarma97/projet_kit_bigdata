import argparse
import logging
from todolist.Tache import Tache, TacheStatus
import json

# Initialize logging
# logging.basicConfig(level=logging.INFO)


class ToDoList:
    """Class to manage a list of Taches."""

    def __init__(self):
        """Initialize a new ToDoList object."""
        self._task_list = []

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
        try:
            if self._task_list == []:
                logging.debug("Empty list")
            else:
                for tache in self._task_list:
                    if(status == None or tache.status == status):
                        print(tache)
                    
        except Exception as e:
            logging.error(f"Error displaying Tache: {e}")
            
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
                raise ValueError("A Tache with same name is already in the list.")

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
            
            tache.status = TacheStatus.COMPLETED
            logging.debug(f"Tache completed: {tache}")

        except Exception as e:
            logging.error(f"Error completing Tache: {e}")

    def modified(self, tache_name : str, projet: str | None = None, horodatage=None, nom: str | None = None, description: str | None = None):
        """Modify a Tache."""
        try:
            tache = self._name_exist(tache_name)

            if tache == None:
                raise ValueError(f"Tache with name {tache_name} is not in the list.")
            
            if not any([projet, horodatage, nom, description]):
                raise ValueError("No arguments provided to modify Tache.")
            
            if projet:
                tache.projet = projet
            if horodatage:
                tache.horodatage = horodatage
            if nom:
                tache.nom = nom
            if description:
                tache.description = description

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

            with open(file, 'r') as f:
                data = json.load(f)

            status_method = {'en cours': TacheStatus.EN_COURS,
                             'terminée': TacheStatus.COMPLETED,
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

#
#def main():
#    parser = argparse.ArgumentParser(description='Manage a simple ToDo List.')
#    parser.add_argument('-a', '--add', help='Add a new task to the list', type=str)
#    parser.add_argument('-m', '--modify', help='Modify an existing task', nargs=2, metavar=('id', 'new_task'))
#    parser.add_argument('-d', '--delete', help='Delete an existing task', type=int)
#    parser.add_argument('-l', '--list', help='Get the list of tasks', action='store_true')
#    parser.add_argument('-t', '--terminate', help='Terminate an existing task', type=int)
#    parser.add_argument('-s', '--status', help='Show current status of the task', type=int)
#
#    args = parser.parse_args()
#
#    # Initialize ToDoList object. In real-world applications, you'd likely load this from a file or database.
#    todo_list = ToDoList()
#
#    if args.add:
#        todo_list.add(args.add)
#        print(f"Added task: {args.add}")
#
#    elif args.modify:
#        task_id, new_task = args.modify
#        todo_list.modified(int(task_id), new_task)
#        print(f"Modified task {task_id} to: {new_task}")
#
#    elif args.delete:
#        todo_list.delete(args.delete)
#        print(f"Deleted task {args.delete}")
#
#    elif args.list:
#        tasks = todo_list.display_liste()
#        print("Current tasks:", tasks)
#
#    elif args.terminate:
#        todo_list.completed(args.terminate)
#        print(f"Task {args.terminate} marked as complete.")
#
#    elif args.status:
#        status = todo_list.get_status(args.status)
#        print(f"Status of task {args.status}: {status}")
#
#if __name__ == "__main__":
#    main()
