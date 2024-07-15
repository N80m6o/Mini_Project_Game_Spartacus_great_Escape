import random
import time
import sys
import re
from moviepy.editor import VideoFileClip
import pygame
from PIL import Image

def print_slow(str, first_time=True):
    """Prints text slowly for dramatic effect."""
    if first_time:
        for letter in str:
            sys.stdout.write(letter)
            sys.stdout.flush()
            time.sleep(0.03)
    else:
        print(str)

class Game:
    def __init__(self):
        self.state = {
            'current_room': 'Prison Cell',
            'inventory': [],
            'puzzle_solved': False,
            'gave_up': False
        }
        self.rooms = {
            "Prison Cell": {
                "description": "You wake up on the cold stone floor of your cell, bound and bruised. The only light comes from a small, barred window high above. As your eyes adjust to the darkness, you notice a loose stone in the wall.",
                "actions": {
                    "investigate": "You find a hidden compartment containing a small, rusted key.",
                    "examine bed": "You find nothing of interest under the bed.",
                    "look around": "You see a locked door and a small barred window."
                },
                "next_room": "Library",
                "key": "rusted key",
                "puzzle": "investigate"
            },
            "Library": {
                "description": "You step into a large library filled with ancient scrolls and dusty tomes. The room is dimly lit, and the scent of old parchment fills the air.",
                "actions": {
                    "examine desk": "You find a key for the next door among the scrolls.",
                    "read scrolls": "The scrolls are written in a language you don't understand.",
                    "search shelves": "You find an old map detailing the layout of the fortress."
                },
                "next_room": "Workshop",
                "key": "library key",
                "puzzle": "examine desk"
            },
            "Workshop": {
                "description": "You find yourself in a workshop filled with tools and gadgets. The walls are lined with shelves holding various mechanical parts.",
                "actions": {
                    "search thoroughly": "You find a hidden key among the tools.",
                    "inspect tools": "You find a variety of tools that might be useful.",
                    "examine machinery": "The machinery looks complex but you might be able to figure it out."
                },
                "next_room": "Study",
                "key": "workshop key",
                "puzzle": "search thoroughly"
            },
            "Study": {
                "description": "You step into a grand study with high walls filled with books and scrolls. At the far end, you see a table with various models of screens and an open book describing their specifications.",
                "actions": {
                    "identify model": "You identify the correct screen model and find the key to the final door.",
                    "examine books": "You find a book that might help you understand the screen models.",
                    "look at table": "The table has various models of screens and a book detailing their specs."
                },
                "next_room": "Garden",
                "key": "study key",
                "puzzle": "identify model"
            },
            "Garden": {
                "description": "You enter a serene garden filled with the sounds of trickling water and birdsong. The floor is a mosaic of colored tiles.",
                "actions": {
                    "navigate garden": "You carefully navigate the garden and find a box containing the final key.",
                    "examine fountain": "The fountain is beautiful and calming.",
                    "look around": "You see a path leading to a door and a vine-covered archway."
                },
                "next_room": "Outside",
                "key": "garden key",
                "puzzle": "navigate garden"
            },
            "Outside": {
                "description": "Spartacus, the legend, lives on, you think to yourself as you walk towards the horizon, ready to continue your quest for knowledge and freedom.",
                "actions": {}
            }
        }

    def play_intro_video(self, video_path):
        """Plays the introductory video with sound."""
        clip = VideoFileClip(video_path)
        clip.preview()
        clip.close()

    def play_sound(self, sound_path):
        """Plays a sound."""
        pygame.mixer.init()
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    def display_image(self, image_path):
        """Displays an image."""
        img = Image.open(image_path)
        img.show()

    def display_room(self, room, first_time=False):
        """Displays the current room's description and available actions."""
        if room == "Prison Cell" and first_time:
            self.play_intro_video("C:/Users/Admin/OneDrive/Documentos/IronHack/Mini_Project_Game_Spartacus_great_Escape/Video/Awakening.mp4")
        print_slow(f"\nYou are in the {room}.", first_time)
        print_slow(self.rooms[room]['description'], first_time)
        print_slow(" What would you like to do?", first_time)
        actions = list(self.rooms[room]['actions'].keys())
        random.shuffle(actions)  # Shuffle the actions to make it less predictable
        for action in actions:
            print_slow(f" \n - {action}", first_time)
        print_slow(" \n - give up", first_time)

    def process_action(self, action):
        """Processes the player's action."""
        if action == "give up":
            self.state['gave_up'] = True
            return
        current_room = self.state['current_room']
        if action in self.rooms[current_room]['actions']:
            print_slow(self.rooms[current_room]['actions'][action], False)
            if action == self.rooms[current_room]['puzzle']:
                self.state['puzzle_solved'] = True
                if current_room == "Prison Cell":
                    self.play_sound("C:/Users/Admin/OneDrive/Documentos/IronHack/Mini_Project_Game_Spartacus_great_Escape/Sounds/prison_cell.mp3")
                if 'key' in self.rooms[current_room]:
                    self.state['inventory'].append(self.rooms[current_room]['key'])
                    self.state['puzzle_solved'] = False
                    del self.rooms[current_room]['key']
                if 'next_room' in self.rooms[current_room]:
                    self.state['current_room'] = self.rooms[current_room]['next_room']
                    print_slow("You have unlocked the next room!", False)
            if current_room == "Library" and action == "search shelves":
                self.display_image("C:/Users/Admin/OneDrive/Documentos/IronHack/Mini_Project_Game_Spartacus_great_Escape/Images/Shelves_Search.gif")
            else:
                print("That action didn't help much. Try again.")
        else:
            print("Invalid action. Please try again.")

    def validate_input(self, user_input, pattern):
        """Validates the user input against a regex pattern."""
        return re.match(pattern, user_input)

    def print_title(self):
        """Prints the title of the game in big letters."""
        import pyfiglet
        title = pyfiglet.figlet_format("The Unshackled")
        print(title)

    def main(self):
        """Main game loop."""
        try:
            self.print_title()
            print_slow("Hi Gamer! Please enter your name: ", True)
            player_name = input("Name: ")
            
            while not self.validate_input(player_name, r"^\w{3,}$"):
                print("Please enter your name with at least three characters.")
                player_name = input("Hi Gamer! Please enter your name: ")
            
            print_slow(f"Greetings {player_name}! Welcome to the adventure of your life! ", True)

            first_time = True
            while self.state['current_room'] != 'Outside' and not self.state['gave_up']:
                self.display_room(self.state['current_room'], first_time)
                first_time = False
                action = input("\n Choose an action: ").strip().lower()
                if self.validate_input(action, r"^[a-z\s]+$"):
                    self.process_action(action)
                    if self.state['gave_up']:
                        break
                else:
                    print("Invalid input. Actions can only contain letters and spaces.")
            
            if self.state['gave_up']:
                print(f"\n{player_name}, you have chosen to give up. The path to freedom is fraught with challenges, and not everyone can endure. Perhaps another time, you'll find the strength to overcome.")
            else:
                print(f"\nCongratulations {player_name}! \n You have ESCAPED. \n Spartacus, the legend, lives on!")
        
        except Exception as e:
            print(f"An error occurred: {e}")
        
        finally:
            print("Thank you for playing the game!")

# Run the game
if __name__ == "__main__":
    game = Game()
    game.main()
