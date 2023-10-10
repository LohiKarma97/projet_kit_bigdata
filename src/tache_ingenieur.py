from task import Task, TaskStatus
from typing import Union, List

class TacheIngenieur(Task):
    def __init__(self, status: TaskStatus, projet: str, horodatage: Union[int, str], Nom: str, Description: str, technologies: List[str]):
        super().__init__(status, projet, horodatage, Nom, Description)
        self.technologies = technologies

    def __str__(self):
        return f"TacheIngenieur({super().__str__()}, technologies={self.technologies})"
