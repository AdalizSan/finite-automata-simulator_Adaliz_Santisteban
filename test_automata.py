import unittest
from app import automata

class TestAutomata(unittest.TestCase):
    def setUp(self):
        self.validAutomata = {
            "id": "automata1",
            "name": "Even checker",
            "initial_state": "q0",
            "acceptance_states": ["q0"],
            "alphabet": ["0", "1"],
            "states": ["q0", "q1"],
            "transitions": [
                {"from_state": "q0", "symbol": "0", "to_state": "q0"},
                {"from_state": "q0", "symbol": "1", "to_state": "q1"},
                {"from_state": "q1", "symbol": "0", "to_state": "q0"},
                {"from_state": "q1", "symbol": "1", "to_state": "q1"}
            ],
            "test_strings": ["0", "10", ""]
        }
        self.invalidAutomata = {
            "id": "automata2",
            "name": "Broken checker",
            "initial_state": "q0",
            "acceptance_states": ["q5"],
            "alphabet": ["0", "1"],
            "states": ["q0", "q1"],
            "transitions": [
                {"from_state": "q0", "symbol": "0", "to_state": "q0"}
            ],
            "test_strings": ["0"]
        }

    def test_validAutomata(self):
        auto = automata(self.validAutomata)
        auto.checkAll()

    def test_invalid_accept_state(self):
        auto = automata(self.invalidAutomata)
        with self.assertRaises(ValueError):
            auto.checkAll()

    def test_word_check(self):
        auto = automata(self.validAutomata)
        self.assertTrue(auto.checkWord("00"))
        self.assertFalse(auto.checkWord("01"))
        self.assertTrue(auto.checkWord(""))

if __name__ == '__main__':
    unittest.main()