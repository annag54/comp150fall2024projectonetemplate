import sys
import os
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from project_code.src.main import Statistic, Character, Event, Weapon, EventStatus

class TestStatistic(unittest.TestCase):
    def setUp(self):
        self.strength = Statistic("Strength", value=10)

    def test_statistic_initialization(self):
        self.assertEqual(self.strength.name, "Strength")
        self.assertEqual(self.strength.value, 10)

    def test_statistic_modify(self):
        # Test increasing and decreasing the value within bounds
        self.strength.modify(5)
        self.assertEqual(self.strength.value, 15)
        self.strength.modify(-10)
        self.assertEqual(self.strength.value, 5)

    def test_statistic_min_max_bounds(self):
        # Test if the value is capped by max_value
        self.strength.modify(1000)
        self.assertEqual(self.strength.value, self.strength.max_value)

        # Test if the value is capped by min_value
        self.strength.modify(-1000)
        self.assertEqual(self.strength.value, self.strength.min_value)


class TestCharacter(unittest.TestCase):
    def setUp(self):
        self.character = Character(name="Sally")

    def test_character_initialization(self):
        self.assertEqual(self.character.name, "Sally")
        self.assertEqual(self.character.strength.name, "Strength")
        self.assertEqual(self.character.intelligence.name, "Intelligence")
        self.assertEqual(self.character.agility.name, "Agility")
        self.assertEqual(self.character.health.name, "Health")

    def test_weapon_modify_stat(self):
        knife = Weapon("Knife", 10)
        self.character.strength.modify(knife.damage)  # Damage from weapon is added to strength
        self.assertEqual(self.character.strength.value, 10 + knife.damage)  # 10 is the initial value

    def test_choose_weapon(self):
        sword = Weapon("Sword", 12)
        self.character.weapon = sword
        self.character.strength.modify(sword.damage)
        self.assertEqual(self.character.strength.value, 22)


class TestEvent(unittest.TestCase):
    def setUp(self):
        self.event_data = {
            "prompt_text": "You come across a house. Do you go inside?",
            "pass": {"message": "You go inside and find supplies."},
            "fail": {"message": "The door is locked."},
            "choices": ["Run", "Fight"]
        }
        self.event = Event(self.event_data)

    def test_event_initialization(self):
        self.assertEqual(self.event.prompt_text, self.event_data["prompt_text"])
        self.assertEqual(self.event.pass_message, self.event_data["pass"]["message"])
        self.assertEqual(self.event.fail_message, self.event_data["fail"]["message"])
        self.assertEqual(self.event.choices, self.event_data["choices"])
    
    @patch('random.choice', return_value=True)  
    def test_event_execute_pass_condition(self):
        character = Character("Test Character")
        character.strength.value = 50  # High value to ensure pass
        self.event.execute(character, parser= None) 
        self.assertEqual(self.event.status, EventStatus.PASS)
    
    @patch('random.choice', return_value=False)  # Assume False means failure
    def test_event_execute_fail_condition(self):
        character = Character("Test Character")
        character.strength.value = 0  # Low value to ensure fail
        self.event.execute(character, parser=None)
        self.assertEqual(self.event.status, EventStatus.FAIL)

    def test_player_dead(self):
        character = Character("Test")
        character.health.value = 0
        self.event.execute(character, parser=None)
        all_dead = all(character.health.value == 0 )
        self.assertTrue(all_dead, "Player is not dead") # Confirms player has 0 health if they do not then the message will prompt







if __name__ == '__main__':
    unittest.main()
