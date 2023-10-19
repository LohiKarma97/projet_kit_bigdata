import unittest
import logging
# Remplacez 'your_module' par le nom du module où se trouve votre classe Tache
from todolist.Tache import Tache, TacheStatus


class TestTache(unittest.TestCase):

    def test_init_valid(self):
        try:
            t = Tache(TacheStatus.EN_COURS, "Projet A",
                      1633897200, "Tâche 1", "Description 1")
            self.assertEqual(t.status, TacheStatus.EN_COURS)
            self.assertEqual(t.projet, "Projet A")
            self.assertEqual(t.horodatage, 1633897200)
            self.assertEqual(t.nom, "Tâche 1")
            self.assertEqual(t.description, "Description 1")
        except Exception as e:
            self.fail(f"Initialization with valid arguments failed: {e}")

    def test_init_invalid_horodatage(self):
        with self.assertRaises(ValueError):
            Tache(TacheStatus.A_FAIRE, "Projet B", -
                  10, "Tâche 2", "Description 2")

    def test_str_representation(self):
        t = Tache(TacheStatus.EN_COURS, "Projet C",
                  1633897300, "Tâche 3", "Description 3")
        expected_str = "Tache(status=TacheStatus.EN_COURS, projet=Projet C, horodatage=1633897300, Nom=Tâche 3, Description=Description 3)"
        self.assertEqual(str(t), expected_str)


if __name__ == '__main__':
    # Désactiver les logs pendant les tests
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
