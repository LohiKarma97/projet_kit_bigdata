from task import Task, TaskStatus
from typing import Union

class TacheComercial(Task):
    def __init__(self, status: TaskStatus, projet: str, horodatage: Union[int, str], Nom: str, Description: str, client: str):
        super().__init__(status, projet, horodatage, Nom, Description)
        self.client = client

    def __str__(self):
        return f"TacheComercial({super().__str__()}, client={self.client})"
