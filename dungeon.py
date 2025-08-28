#pylint:disable=W1114
#pylint:disable=W0613
#pylint:disable=W0122
#pylint:disable=W0102


# room, whats is it etc
class  Room:
    def __init__(
    self,
    name: str,
    src: str,
    contents: list,
    doors: list
    ):
        self.src = src
        self.name = name
        self.contents = contents
        self.doors = doors
        self.actions = {}
        self.update_action_list()
        
    # create or update action list
    def update_action_list(self):
        i = 0
        for item in self.contents:
            self.actions[str(i)] = item
            i += 1
        for door in self.doors:
            self.actions[str(i)] = door
            i += 1
     
     # add door
    def add_door(self, door):
        self.doors.append(door)
        self.update_action_list()
     
     # describes the room and its contents   
    def describe(self):
        print(f"You walk into {self.src}. It contains a ", end="")
        for item in self.contents:
            print(f"{item.name}")
    
    # lists the avliable actions 
    def list_actions(self):
        i = 0
        print("Actions: ")
        for item in self.contents:
            print(f"{item.name} [{i}]")
        print("Doors: ")
        for door in self.doors:
            print(f"{door.name} [{i}]")
      
     # take action      
    def action(self, action, character):
        action = action
        room_code = self.actions[action].actioned(character, "fp")
        if room_code == "rm":
            self.contents.remove(self.actions[action])
            self.update_action_list()
        
        
        
# the player
class Character:
    def __init__(
    self,
    room: Room,
    health: int = 100,
    atk: float = 1,
    defe: float = 1,
    items: list = []
    ):
        self.room = room
        self.health = health
        self.atk = atk
        self.defe = defe
        self.items = items
        
    # modify a stat
    def mod(self, mod: int, stat: str):
        if stat.startswith("a"):
            self.atk += mod
        elif stat.startswith("d"):
            self.defe += mod
        elif stat.startswith("h"):
            self.health += mod
            
    # character actions
    def action(self, action):
        # i = list all items, and a menu to interact
        if action == "i":
            actions = {}
            i = 0
            for item in self.items:
                actions[str(i)] = item
                i += 1
            # list items
            i = 0
            print("Backpack: ")
            for item in self.items:
                print(f"{item.name} [{i}]")
            choice = input("Select: ")
            actions[choice].actioned(self, "bp")
                
        
# Item class
class Item:
    def __init__(
    self,
    name: str,
    description: str,
    investigated_description: str,
    mod: float,
    stat: str
    ):
        self.name = name
        self.description = description
        self.investigated_description = investigated_description
        self.mod = mod
        self.stat = stat
    
    def actioned(self, character, tag):
        # when an item is actioned certain tags define how it was actioned. The list of tags is here for now.
        # bp: item was actioned from backpack
        # fp: item was picked up from floor
        # fi: item was investigated from floor
        if tag == "bp" or tag == "fi":
            print(self.investigated_description)
            return ""
        elif tag == "fp":
            character.mod(self.mod, self.stat)
            character.items.append(self)
            return "rm"

        
# Door class
class Door():
    def __init__(
    self,
    name: str,
    start: Room,
    end: Room):
        self.name = name
        self.start = start
        self.end = end
    
    def actioned(self, charater: Character):
        if charater.room not in [
        self.start, self.end]:
            raise ValueError("chracter not in door start or end")
        elif charater.room == self.start:
            charater.room = self.end
        elif charater.room == self.end:
            charater.room = self.end
        return ""
      
                        
# Rooms are hard coded below. Future versions will allow files to contain rooms and be imported


# default room
default_room = Room(
"default",
"this is a default room for testing",
[],
[])

# start room
start_room = Room(
"A Cobled Start",
"A small cobled room with no windows, and a staircase made of the same coble stone dimmly lit by torches leading downwards",
[Item(
"Sward",
"This Stone Sward looks like it has seen better days, with chips in the blade and scratches on the handle it has slayed many beasts",
"Stone Sward, +5 atk",
0.05,
"atk")
],
[])


# Doors are hard coded bellow. Future versions will allow files to contain rooms and be imported. The first function will take care of making a door

def make_door(
name: str,
start: Room,
end: Room
):
    start.add_door(Door(name, start, end))
    end.add_door(Door(name, end, start))
    
make_door("stairs", start_room, default_room)
# Other variables 

# false for game over
running = True

# Main
def main():
    # describe rules
    print("The folowing actions are always avliable from the default menu:\ni: lists items in backpack, and provides a menu to interact with them\n\n")
    player = Character(start_room)
    # game loop
    while running:
        player.room.describe()
        player.room.list_actions()
        action = input("Select: ")
        if action.isnumeric():
            player.room.action(action, player)
        else:
            player.action(action)


if "__main__" == __name__:
    main()