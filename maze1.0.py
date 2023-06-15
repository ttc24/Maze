import random

# Define the player class
class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.max_health = 100
        self.level = 1
        self.xp = 0
        self.attack_power = 10
        self.defense_power = 5
        self.gold = 0
        self.inventory = []

    def take_damage(self, damage):
        self.health -= damage

    def heal(self, amount):
        self.health = min(self.health + amount, self.max_health)

    def level_up(self):
        self.level += 1
        self.max_health += 10
        self.health = self.max_health
        self.attack_power += 5
        self.defense_power += 2
        print("Level up! You are now level", self.level)

    def collect_item(self, item):
        self.inventory.append(item)
        print("You picked up a", item)

    def use_health_potion(self):
        if "Health Potion" in self.inventory:
            self.heal(20)
            self.inventory.remove("Health Potion")
            print("You used a Health Potion and healed 20 HP.")
        else:
            print("You don't have any Health Potions.")

    def get_score(self):
        score = self.level * 10
        score += self.inventory.count("Health Potion") * 5
        score += self.inventory.count("Gold") * 2
        return score

    def is_alive(self):
        return self.health > 0

# Define the enemy class
class Enemy:
    def __init__(self, name, health, attack_power, experience, gold_drop):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.experience = experience
        self.gold_drop = gold_drop

    def take_damage(self, damage):
        self.health -= damage

    def is_alive(self):
        return self.health > 0

    def attack(self, player):
        player.take_damage(self.attack_power)

    def drop_gold(self):
        return self.gold_drop

# Define the shop class
class Shop:
    def __init__(self):
        self.items = {
            "Health Potion": 2,
            "Attack Boost": 5,
            "Defense Boost": 4
        }

    def display_items(self):
        print("Welcome to the Shop!")
        print("Available Items:")
        for item, price in self.items.items():
            print(f"{item}: {price} gold")

    def purchase_item(self, player, item):
        if item in self.items:
            price = self.items[item]
            if player.gold >= price:
                player.gold -= price
                player.collect_item(item)
                print(f"You purchased a {item} for {price} gold.")
            else:
                print("Not enough gold to purchase the item.")
        else:
            print("Item not available in the shop.")

# Define the dungeon class
class Dungeon:
    def __init__(self, size):
        self.size = size
        self.player = None
        self.player_location = None 
        self.exit_location = None
        self.enemies = []
        self.items = []
        self.shop = Shop()
        self.leaderboard = []
        self.moves = 0  # Track the number of moves

    def generate(self):
        # Place the player at a random location
        self.player = Player("Player")
        player_location = (random.randint(0, self.size-1), random.randint(0, self.size-1))

        # Place the exit at a random location
        self.exit_location = (random.randint(0, self.size-1), random.randint(0, self.size-1))

        # Generate enemies
        num_enemies = random.randint(self.size, self.size*2)
        for _ in range(num_enemies):
            enemy_level = self.player.level
            enemy = Enemy("Enemy", random.randint(10, 20) * enemy_level, random.randint(5, 10) * enemy_level, enemy_level * 10, random.randint(3, 4))
            enemy_location = (random.randint(0, self.size-1), random.randint(0, self.size-1))
            self.enemies.append((enemy, enemy_location))

        # Generate items
        num_items = random.randint(self.size, self.size*2)
        for _ in range(num_items):
            item = "Health Potion"
            item_location = (random.randint(0, self.size-1), random.randint(0, self.size-1))
            self.items.append((item, item_location))

        return player_location

    def move_player(self, direction):
        player_x, player_y = self.player_location

        if direction == "north" and player_y > 0:
            self.player_location = (player_x, player_y - 1)
        elif direction == "south" and player_y < self.size - 1:
            self.player_location = (player_x, player_y + 1)
        elif direction == "west" and player_x > 0:
            self.player_location = (player_x - 1, player_y)
        elif direction == "east" and player_x < self.size - 1:
            self.player_location = (player_x + 1, player_y)
        else:
            print("You cannot move in that direction.")

    def battle(self, enemy):
        print("You encountered an enemy!")
        while enemy.is_alive() and self.player.is_alive():
            print("Player HP:", self.player.health)
            print("Enemy HP:", enemy.health)
            print("1. Attack")
            print("2. Run")
            choice = input("Enter your choice: ")

            if choice == "1":
                # Player attacks the enemy
                enemy.take_damage(self.player.attack_power)
                print("You attacked the enemy for", self.player.attack_power, "damage.")
                if not enemy.is_alive():
                    print("You defeated the enemy.")
                    self.player.xp += enemy.experience
                    self.player.gold += enemy.drop_gold()
                    self.player.collect_score(10)  # Increase score for defeating enemy
                    break

                # Enemy attacks the player
                enemy.attack(self.player)
                print("The enemy attacked you for", enemy.attack_power, "damage.")
                if not self.player.is_alive():
                    print("You have been defeated.")
                    break

            elif choice == "2":
                print("You ran away from the enemy.")
                break

            else:
                print("Invalid choice. Try again.")

    def run(self):
        print("Welcome to the maze! \nGood luck with your escape!")
        player_location = self.generate()
        self.player_location = player_location

        while True:
            print("\n" + "=" * 20)
            print("Location:", self.player_location)
            print("Health:", self.player.health, "/", self.player.max_health)
            print("Level:", self.player.level)
            print("XP:", self.player.xp)
            print("Gold:", self.player.gold)
            print("Inventory:", self.player.inventory)

            if self.player_location == self.exit_location:
                score = self.player.get_score()
                print("Congratulations! You reached the exit.")
                print("Your score:", score)
                self.leaderboard.append((self.player.name, score))
                print("Amount of moves to escape:", self.moves)  # Add the moves count
                print("\nLeaderboard:")
                for player, score in self.leaderboard:
                    print(player, "-", score)
                break

            # Print messages after encountering an enemy
            defeated_enemies = []  # Track defeated enemies

            for enemy, enemy_location in self.enemies:
                if enemy_location == self.player_location:
                    print("An enemy has appeared!")
                while enemy.is_alive() and self.player.is_alive():
                        print("Player HP:", self.player.health)
                        print("Enemy HP:", enemy.health)
                        print("1. Attack")
                        print("2. Run")
                        choice = input("Enter your choice: ")

                        if choice == "1":
                            enemy.take_damage(self.player.attack_power)
                            self.player.take_damage(enemy.attack_power)
                            if enemy.is_alive():
                                print("You attacked the enemy.")
                            else:
                                print("You defeated the enemy.")
                                self.player.collect_item("Gold")
                                self.player.xp += 10
                                if self.player.xp >= self.player.level * 20:
                                    self.player.level_up()
                                    # Increase enemy power
                                    for enemy, _ in self.enemies:
                                        enemy.attack_power += 2
                                        enemy.health += 10
                                # Drop gold
                                gold_drop = random.randint(3, 4)
                                self.player.gold += gold_drop
                                print(f"The enemy dropped {gold_drop} gold.")
                                defeated_enemies.append((enemy, enemy_location))
                                break
                        elif choice == "2":
                            print("You ran away from the enemy.")
                            self.move_player(random.choice(["north", "south", "west", "east"]))
                            break
                        else:
                            print("Invalid choice. Try again.")

                        if not enemy.is_alive():
                            print("You defeated the enemy.")
                            self.player.collect_item("Gold")
                            self.player.xp += 10
                            if self.player.xp >= self.player.level * 20:
                                self.player.level_up()
                                # Increase enemy power
                                for enemy, _ in self.enemies:
                                    enemy.attack_power += 2
                                    enemy.health += 10
                            # Drop gold
                            gold_drop = random.randint(3, 4)
                            self.player.gold += gold_drop
                            print(f"The enemy dropped {gold_drop} gold.")
                            defeated_enemies.append((enemy, enemy_location))

            # Remove defeated enemies from the enemies list
            for enemy, enemy_location in defeated_enemies:
                self.enemies = [(e, loc) for e, loc in self.enemies if loc != enemy_location]

            for item, item_location in self.items:
                if item_location == self.player_location:
                    print("You found a", item)
                    self.player.collect_item(item)
                    self.items.remove((item, item_location))
                    break

            if self.player_location == (self.size-1, self.size-1):
                self.shop.display_items()
                while True:
                    choice = input("Enter the item you want to purchase (or 'exit' to leave): ")
                    if choice == "exit":
                        break
                    else:
                        self.shop.purchase_item(self.player, choice)

            print("Choose your action:")
            print("1. Move north")
            print("2. Move south")
            print("3. Move west")
            print("4. Move east")
            print("5. Use Health Potion")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.move_player("north")
            elif choice == "2":
                self.move_player("south")
            elif choice == "3":
                self.move_player("west")
            elif choice == "4":
                self.move_player("east")
            elif choice == "5":
                self.player.use_health_potion()
            else:
                print("Invalid choice. Try again.")

            self.moves += 1  # Increment moves count

# Run the game
dungeon = Dungeon(6)
dungeon.run()

def play_game():
    # Run the game
    dungeon = Dungeon(6)
    dungeon.run()

    # Ask the player if they want to play again
    play_again = input("Do you want to play again? (yes/no): ")
    if play_again.lower() == "yes":
        play_game()
    else:
        print("Thank you for playing!")

# Play the game
play_game()