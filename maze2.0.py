import random

class Entity:
    def __init__(self, name, description):
        self.name = name
        self.description = description

class Player(Entity):
    def __init__(self, name):
        super().__init__(name, "The player")
        self.level = 1
        self.health = 100
        self.max_health = 100
        self.attack_power = 10
        self.xp = 0
        self.gold = 0
        self.inventory = []
        self.weapon = None

    def is_alive(self):
        return self.health > 0

    def collect_item(self, item):
        self.inventory.append(item)

    def use_health_potion(self):
        if "Health Potion" in self.inventory:
            self.inventory.remove("Health Potion")
            self.health += 20
            print("You used a Health Potion and gained 20 health.")
        else:
            print("You don't have a Health Potion to use.")

    def attack(self, enemy):
        if self.weapon:
            damage = random.randint(self.weapon.min_damage, self.weapon.max_damage)
            enemy.take_damage(damage)
            print("You attacked the", enemy.name + " with your", self.weapon.name + " and dealt", damage, "damage!")
        else:
            damage = random.randint(self.attack_power // 2, self.attack_power)
            enemy.take_damage(damage)
            print("You attacked the", enemy.name + " for", damage, "damage.")
        
        if not enemy.is_alive():
            self.xp += enemy.xp
            self.gold += enemy.drop_gold()
            print("You defeated the", enemy.name + "!")
            print("You gained", enemy.xp, "experience and", enemy.drop_gold(), "gold.")
            
            if self.xp >= self.level * 20:
                self.xp -= self.level * 20
                self.level_up()

    def defend(self, enemy):
        damage = max(0, enemy.attack_power - self.defense)
        self.health -= damage
        print(f"The {enemy.name} attacked you and dealt {damage} damage.")

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def level_up(self):
        self.level += 1
        self.max_health += 10
        self.health = self.max_health
        self.attack_power += 5

    def equip_weapon(self, weapon):
        if weapon in self.inventory:
            if self.weapon:
                self.inventory.append(self.weapon)
                print("You unequipped the", self.weapon.name)
            self.weapon = weapon
            self.inventory.remove(weapon)
            print("You equipped the", weapon.name)
        else:
            print("You don't have the", weapon.name)

    def get_score(self):
        return self.level * 100 + len(self.inventory) * 10 + self.gold

class Enemy(Entity):
    def __init__(self, name, health, attack_power, defense, gold):
        super().__init__(name, "")
        self.health = health
        self.attack_power = attack_power
        self.defense = defense
        self.gold = gold

    def is_alive(self):
        return self.health > 0

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def drop_gold(self):
        return self.gold

class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

class Weapon:
    def __init__(self, name, description, min_damage, max_damage):
        self.name = name
        self.description = description
        self.min_damage = min_damage
        self.max_damage = max_damage

class DungeonBase:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rooms = [[None for _ in range(width)] for _ in range(height)]
        self.player = None
        self.shop = []

    def print_map(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.rooms[y][x] == self.player:
                    print("P", end=" ")
                elif self.rooms[y][x] in self.shop:
                    print("S", end=" ")
                elif self.rooms[y][x] is None:
                    print("-", end=" ")
                else:
                    print("E", end=" ")
            print()
            
    def get_adjacent_rooms(self, x, y):
        adjacent_rooms = []
        if x > 0:
            adjacent_rooms.append((x - 1, y))
        if x < self.width - 1:
            adjacent_rooms.append((x + 1, y))
        if y > 0:
            adjacent_rooms.append((x, y - 1))
        if y < self.height - 1:
            adjacent_rooms.append((x, y + 1))
        return adjacent_rooms

    def is_valid_move(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        if self.rooms[y][x] is None:
            return False
        return True

    def move_player(self, direction):
        x, y = self.get_player_position()

        if direction == "left":
            x -= 1
        elif direction == "right":
            x += 1
        elif direction == "up":
            y -= 1
        elif direction == "down":
            y += 1

        if self.is_valid_move(x, y):
            self.rooms[y][x] = self.player
            self.rooms[self.player.y][self.player.x] = None
            self.player.x = x
            self.player.y = y
        else:
            print("Invalid move!")

    def get_player_position(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.rooms[y][x] == self.player:
                    return x, y

    def battle(self, enemy):
        print("You encountered a", enemy.name + "!")

        while self.player.is_alive() and enemy.is_alive():
            print("Player Health:", self.player.health)
            print("Enemy Health:", enemy.health)
            print("What do you want to do?")
            print("1. Attack")
            print("2. Defend")
            print("3. Use Health Potion")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.player.attack(enemy)
                if enemy.is_alive():
                    enemy.attack(self.player)
            elif choice == "2":
                self.player.defend(enemy)
                enemy.attack(self.player)
            elif choice == "3":
                self.player.use_health_potion()
                enemy.attack(self.player)
            else:
                print("Invalid choice! Try again.")

        if not self.player.is_alive():
            print("Game Over!")
            print("Final Score:", self.player.get_score())

    def play_game(self):
        print("Welcome to the Dungeon Game!")

        self.player = Player(input("Enter your name: "))
        self.player.x = random.randint(0, self.width - 1)
        self.player.y = random.randint(0, self.height - 1)
        self.rooms[self.player.y][self.player.x] = self.player

        num_enemies = random.randint(3, 5)

        for _ in range(num_enemies):
            enemy = Enemy("Enemy", random.randint(50, 100), random.randint(5, 15), random.randint(1, 5), random.randint(10, 20))
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

            while self.rooms[y][x] is not None:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)

            self.rooms[y][x] = enemy

        self.shop = [Item("Health Potion", "Restores 20 health")]

        while self.player.is_alive():
            print("Player Health:", self.player.health)
            print("Player Level:", self.player.level)
            print("Player XP:", self.player.xp)
            print("Player Gold:", self.player.gold)
            self.print_map()
            print("What do you want to do?")
            print("1. Move Left")
            print("2. Move Right")
            print("3. Move Up")
            print("4. Move Down")
            print("5. Battle Enemy")
            print("6. Visit Shop")
            print("7. Quit Game")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.move_player("left")
            elif choice == "2":
                self.move_player("right")
            elif choice == "3":
                self.move_player("up")
            elif choice == "4":
                self.move_player("down")
            elif choice == "5":
                x, y = self.get_player_position()
                for dx, dy in self.get_adjacent_rooms(x, y):
                    if isinstance(self.rooms[dy][dx], Enemy):
                        self.battle(self.rooms[dy][dx])
                        break
                else:
                    print("No enemies nearby!")
            elif choice == "6":
                print("Welcome to the Shop!")
                print("1. Buy Health Potion (10 Gold)")
                print("2. Exit Shop")

                shop_choice = input("Enter your choice: ")

                if shop_choice == "1":
                    if self.player.gold >= 10:
                        self.player.collect_item("Health Potion")
                        self.player.gold -= 10
                        print("You bought a Health Potion for 10 gold.")
                    else:
                        print("Not enough gold!")
                elif shop_choice == "2":
                    print("Goodbye!")
                else:
                    print("Invalid choice!")
            elif choice == "7":
                print("Goodbye!")
                break
            else:
                print("Invalid choice! Try again.")

    def generate(self):
        self.player_location = self.get_random_empty_location()
        self.add_entity(self.player_location, "Player")

        for i in range(3):
            enemy_location = self.get_random_empty_location()
            self.add_entity(enemy_location, Enemy("Enemy", random.randint(10, 20), random.randint(5, 10), random.randint(10, 20), random.randint(3, 4)))

        for i in range(2):
            item_location = self.get_random_empty_location()
            self.add_entity(item_location, "Health Potion")

        for i in range(2):
            weapon_location = self.get_random_empty_location()
            self.add_entity(weapon_location, Weapon("Sword", "A sharp sword", 15, 25))

        shop_location = self.get_random_empty_location()
        self.add_entity(shop_location, "Shop")

        return self.player_location

    def move_player(self, direction):
        row_offset, col_offset = self.get_direction_offset(direction)

        current_room = self.player_location
        current_row, current_col = self.get_row_col(current_room)
        new_row = current_row + row_offset
        new_col = current_col + col_offset

        if 0 <= new_row < self.size and 0 <= new_col < self.size:
            new_room = self.get_room_number(new_row, new_col)
            entity = self.get_entity(new_room)

            if entity is None:
                self.move_entity(current_room, new_room)
                self.player_location = new_room
            elif isinstance(entity, Enemy):
                self.battle_enemy(entity)
                if self.player.is_alive():
                    self.move_entity(current_room, new_room)
                    self.player_location = new_room
                else:
                    print("You have been defeated. Game over!")
                    return False
            elif entity == "exit":
                print("Congratulations! You have reached the exit.")
                return False
            elif entity == "shop":
                self.shop()

        else:
            print("You can't go any further in that direction.")

        return True

    def enter_room(self, location):
        entity = self.get_entity(location)

        if entity is None:
            print("There is nothing here.")
        elif isinstance(entity, Enemy):
            self.battle_enemy(entity)
            if not self.player.is_alive():
                print("You have been defeated. Game over!")
                return False
            self.remove_entity(location)
        elif entity == "exit":
            print("Congratulations! You have reached the exit.")
            return False
        elif entity == "shop":
            self.shop()

        return True

    def shop(self):
        print("Welcome to the shop!")
        print("Gold:", self.player.gold)
        print("1. Buy Health Potion (10 gold)")
        print("2. Sell Health Potion (5 gold)")
        print("3. Buy Sword (50 gold)")
        print("4. Sell Sword (25 gold)")
        print("5. Exit Shop")
        choice = input("Enter your choice: ")
        if choice == "1":
            self.buy_health_potion()
        elif choice == "2":
            self.sell_health_potion()
        elif choice == "3":
            self.buy_sword()
        elif choice == "4":
            self.sell_sword()
        elif choice == "5":
            print("Thank you for visiting the shop.")
        else:
            print("Invalid input. Please enter a number between 1 and 5.")

    def buy_health_potion(self):
        if self.player.gold >= 10:
            self.player.collect_item("Health Potion")
            self.player.gold -= 10
            print("You bought a Health Potion.")
        else:
            print("You don't have enough gold.")

    def sell_health_potion(self):
        if "Health Potion" in self.player.inventory:
            self.player.inventory.remove("Health Potion")
            self.player.gold += 5
            print("You sold a Health Potion.")
        else:
            print("You don't have a Health Potion to sell.")

    def buy_sword(self):
        if self.player.gold >= 50:
            self.player.collect_item("Sword")
            self.player.gold -= 50
            print("You bought a Sword.")
        else:
            print("You don't have enough gold.")

    def sell_sword(self):
        if "Sword" in self.player.inventory:
            self.player.inventory.remove("Sword")
            self.player.gold += 25
            print("You sold a Sword.")
        else:
            print("You don't have a Sword to sell.")

    def update_leaderboard(self):
        score = self.player.get_score()
        with open("leaderboard.txt", "a") as file:
            file.write(self.player.name + "," + str(score) + "\n")

        leaderboard = []
        with open("leaderboard.txt", "r") as file:
            for line in file:
                name, score = line.strip().split(",")
                leaderboard.append((name, int(score)))

        leaderboard.sort(key=lambda x: x[1], reverse=True)

        print()
        print("Leaderboard:")
        print("Rank\tName\t\tScore")
        for i, (name, score) in enumerate(leaderboard):
            print(f"{i+1}\t{name}\t\t{score}")

        print()

    def print_leaderboard(self):
        leaderboard = []
        with open("leaderboard.txt", "r") as file:
            for line in file:
                name, score = line.strip().split(",")
                leaderboard.append((name, int(score)))

        leaderboard.sort(key=lambda x: x[1], reverse=True)

        print("Leaderboard:")
        print("Rank\tName\t\tScore")
        for i, (name, score) in enumerate(leaderboard):
            print(f"{i+1}\t{name}\t\t{score}")

    def reset_leaderboard(self):
        with open("leaderboard.txt", "w") as file:
            pass


# Start the game
size = 10
game = DungeonBase(size)
game.play_game()