import sys
import os

# Add the root directory of the project to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from project_code.src.main import Statistic, Character, Event
import unittest

class TestStatistic(unittest.TestCase):

    def setUp(self):
        self.strength = Statistic("Strength", value=10)

    def test_statistic_initialization(self):
        self.assertEqual(self.strength.name, "Strength")
        self.assertEqual(self.strength.value, 10)

    def test_statistic_modify(self):
        self.strength.modify(5)
        self.assertEqual(self.strength.value, 15)
        self.strength.modify(-10)
        self.assertEqual(self.strength.value, 5)

    def test_statistic_min_max_bounds(self):
        self.strength.modify(1000)
        self.assertEqual(self.strength.value, self.strength.max_value)
        self.strength.modify(-1000)
        self.assertEqual(self.strength.value, self.strength.min_value)

class TestCharacter(unittest.TestCase):

    def setUp(self):
        self.character = Character(name="Hero")

    def test_character_initialization(self):
        self.assertEqual(self.character.name, "Sally")
        self.assertEqual(self.character.strength.name, "Strength")
        self.assertEqual(self.character.intelligence.name, "Intelligence")
        self.assertEqual(self.character.agility.name, "Agility")
        self.assertEqual(self.character.health.name, "Health")

class TestEvent(unittest.TestCase):

    def setUp(self):
        self.event_data = {
            "prompt_text": "You come across a house do you go inside?",
            "pass": {"message": "Go inside. "},
            "fail": {"message": "The door is locked."},
            "choices": ["Run","Fight"]
        }
        self.event = Event(self.event_data)

    def test_event_initialization(self):
        self.assertEqual(self.event.prompt_text, self.event_data["prompt_text"])
        self.assertEqual(self.event.pass_message, self.event_data["pass"]["message"])
        self.assertEqual(self.event.fail_message, self.event_data["fail"]["message"])
        self.assertEqual(self.event.choices, self.event_data["choices"] ["Default Option 1", "Default Option 2"])
    


if __name__ == '__main__':
    unittest.main()
