import json
import sys
import random
from typing import List, Optional
from enum import Enum


class EventStatus(Enum):
    UNKNOWN = "unknown"
    PASS = "pass"
    FAIL = "fail"
    PARTIAL_PASS = "partial_pass"


class Statistic:
    def __init__(self, name: str, value: int = 0, description: str = "", min_value: int = 0, max_value: int = 100):
        self.name = name
        self.value = value
        self.description = description
        self.min_value = min_value
        self.max_value = max_value
   
    def __str__(self):
        return f"{self.name}: {self.value} (Health: {self.health}, Strength: {self.strength}, Agility: {self.agility},Intelligence: {self.intelligence})"

    def modify(self, amount: int):
        self.value = max(self.min_value, min(self.max_value, self.value + amount))

class Weapons: 
    def __init__(self, name: str, damage: int):
        self.name = name
        self.damage = damage
        self.description = f"A {name} that deals {damage} damage." 
        
        weapons = [
            Weapons("Sword", 50),
            Weapons("Gun", 70),
            Weapons("Axe", 40),
            Weapons("Knife", 30),
            Weapons("Chainsaw", 90)
        ]
        
        if name not in [weapon.name for weapon in weapons]:                                                 # If player does not choose an existing weapon in weapons
            raise ValueError(f"{name} is not a valid weapon name.Choose a valid weapon from {weapons}")
    
    def __str__(self):
        return f"{self.name} (Damage: {self.damage})" # Weapons are name and damage 

class Character:
    def __init__(self, name: str = "Sally"):
        self.name = name
        self.strength = Statistic("Strength", description= "Strength is a measure of physical power.")
        self.health = Statistic("Health", description= "Health is a measure of lifespan")
        self.agility = Statistic("Agility", description= "Agility is used to measure a characters reflexes to attacks")
        self.intelligence = Statistic("Intelligence", description= "Intelligence measures a characters chances of persuasion")

   
    
    def choose_weapon(self, available_weapons: list):
        print(f"\n{self.name}, choose your weapon:")
        for i, weapon in enumerate(available_weapons, start=1):
            print(f"{i}. {weapon.name} (Damage: {weapon.damage})")

        choice = int(input("\nEnter the number of the weapon you want: ")) - 1
        if 0 <= choice < len(available_weapons):
            self.weapon = available_weapons[choice]
            print(f"\n{self.name} has chosen the {self.weapon.name}!")
        else:
            print("Invalid choice. No weapon selected.")

    """
    Generate random damage value based 
    on character's strength & Modify target's health by the 
    damage dealt
    """
    def attack(self, target: "Character"):    
        damage = random.randint(1, self.strength.value) 
        target.health.modify(-damage) 

    def __str__(self):
        return f"Character: {self.name}, Strength: {self.strength}, Health: {self.health}, Agility: {self.agility}"

    def get_stats(self):
        return [self.strength, self.health, self.agility]  # Extend this list if there are more stats

class Sally(Character):
    def __init__(self):
        super().__init__("Sally")
        self.strength = Statistic("Strength", 20, "Sally is pretty strong.") 
        self.health = Statistic("Health", 90, "Sally has low health.") 
        self.agility = Statistic("Agility", 15, "Sally is very fast.")   
        self.intelligence = Statistic("Intelligence", 20 , "Sally is very smart")



    def choose_weapon(self, available_weapons: list):
        return super().choose_weapon(available_weapons)
        
    def attack(self, target: "Character"):
        super().attack(target)
        if target.health.value <= 0:
            print(f"{self.name} has defeated {target.name}!")

    def get_stats(self):
        return [self.strength, self.health, self.agility]  

    def __str__(self):
        return f"""Character: {self.name}, Strength: {self.strength}, 
        Health: {self.health}, Agility: {self.agility}"""
    
class Kirk(Character):
        def __init__(self):
            super().__init__("Kirk")
            self.strength = Statistic("Strength", 20, "Kirk is strong")
            self.health = Statistic("Health", 135, "Kirk has high health")
            self.agility = Statistic("Agility", 10, "Kirk is slow.")                
            self.intelligence = Statistic("Intelligence", 10 , "Kirk is not very smart")


        def choose_weapon(self, available_weapons: list):
            return super().choose_weapon(available_weapons)

        def attack(self, target: "Character"):
            super().attack(target)
            if target.health.value <= 0:
                print(f"{self.name} has defeated {target.name}!")

        def get_stats(self):
            return [self.strength, self.health, self.agility]  

        def __str__(self):
            return f"""Character: {self.name}, Strength: {self.strength}, 
            Health: {self.health}, Agility: {self.agility}"""
        
class Event:
    def __init__(self, data: dict):
        self.primary_attribute = data['primary_attribute']
        self.secondary_attribute = data['secondary_attribute']
        self.prompt_text = data['prompt_text']
        self.pass_message = data['pass']['message']
        self.fail_message = data['fail']['message']
        self.partial_pass_message = data['partial_pass']['message']
        self.status = EventStatus.UNKNOWN

    def execute(self, party: List[Character], parser):
        print(self.prompt_text)
        character = parser.select_party_member(party)
        chosen_stat = parser.select_stat(character)
        self.resolve_choice(character, chosen_stat)

    def resolve_choice(self, character: Character, chosen_stat: Statistic):
        if chosen_stat.name == self.primary_attribute:
            self.status = EventStatus.PASS
            print(self.pass_message)
            character.strength.modify(15)                       # Update strength with successful event  (gains 15 strength)
            character.health.modify(10)                         # Update health with successful event (gains 10 health)
        elif chosen_stat.name == self.secondary_attribute:
            self.status = EventStatus.PARTIAL_PASS
            print(self.partial_pass_message)
            character.strength.modify(10)                       # Update strength with partially successful event (gains 10 strength)
        else:
            self.status = EventStatus.FAIL
            print(self.fail_message)
            character.health.modify(-5)                         # Player loses 5 health from failed event                  

class Location:
    def __init__(self, events: List[Event]):
        self.events = events

    def get_event(self) -> Event:
        return random.choice(self.events)


class Game:
    def __init__(self, parser, characters: List[Character], locations: List[Location]):
        self.parser = parser
        self.party = characters
        self.locations = locations
        self.continue_playing = True
        self.player_character = None 

    def choose_player(self):
        print("\nChoose your character to play as:")
        for idx, character in enumerate(self.party):
            print(f"{idx + 1}. {character.name} (Strength: {character.strength.value}, Health: {character.health.value}, Agility: {character.agility.value}, 
                  Intelligence: {self.intelligence})")
        
        choice = int(input("Enter the number of the character you want to play: ")) - 1
        if 0 <= choice < len(self.party):
            self.player_character = self.party[choice]
            print(f"\nYou have chosen to play as {self.player_character.name}!")
        else:
            print("Invalid choice, selecting default character.")
            self.player_character = self.party[0]  # Default to the first character if invalid input

    
    def start(self):
        self.choose_player()
        while self.continue_playing:
            location = random.choice(self.locations)
            event = location.get_event()
            event.execute([self.player_character], self.parser)
            if self.check_game_over():
                self.continue_playing = False
        print("Game Over.")

    def check_game_over(self):
        all_dead = all(character.health.value <= 0 for character in self.party)
        if all_dead:
            print("character has died. Game Over!")
        return all_dead

class UserInputParser:
    def parse(self, prompt: str) -> str:
        return input(prompt)

    def select_party_member(self, party: List[Character]) -> Character:
        print("Choose a party member:")
        for idx, member in enumerate(party):
            print(f"{idx + 1}. {member.name}")
        choice = int(self.parse("Enter the number of the chosen party member: ")) - 1
        return party[choice]

    def select_stat(self, character: Character) -> Statistic:
        print(f"Choose a stat for {character.name}:")
        stats = character.get_stats()
        for idx, stat in enumerate(stats):
            print(f"{idx + 1}. {stat.name} ({stat.value})")
        choice = int(self.parse("Enter the number of the stat to use: ")) - 1
        return stats[choice]


def load_events_from_json(file_path: str) -> List[Event]:
    with open(file_path, 'r') as file:
        data = json.load(file)
    return [Event(event_data) for event_data in data]


def start_game():
    parser = UserInputParser()

    sally = Sally()
    kirk = Kirk()
    characters = [sally, kirk]

    # Load events from the JSON file
    events = load_events_from_json('project_code/location_events/location_1.json')

    locations = [Location(events)]
    game = Game(parser, characters, locations)
    game.start()


if __name__ == '__main__':
    start_game()
