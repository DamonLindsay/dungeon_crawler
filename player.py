# player.py


class Player:
    """
    Represents the hero of the dungeon crawler.

    Attributes:
        name (str): The name of the player.
        health (int): The current health of the player.
        max_health (int): The maximum health of the player.
        attack (int): The attack power of the player.
        defense (int): The defense power of the player.
        level (int): The current level of the player.
        experience (int): The current experience points of the player.
        experience_to_next_level (int): The experience points required to reach the next level.
        gold (int): The amount of gold the player has.
        inventory (list): A list of items in the player's inventory.
        position (tuple): The current position of the player in the dungeon (x, y).
    """

    def __init__(self, name: str):
        # --- Identity ---
        self.name = name

        # --- Combat Stats ---
        self.health = 30
        self.max_health = 30
        self.attack = 5
        self.defense = 2

        # --- Progression ---
        self.level = 1
        self.experience = 0
        self.experience_to_next_level = 20  # Experience required to reach level 2

        # --- Resources ---
        self.gold = 0
        self.inventory = []

        # --- Position on the Map ---
        self.position = (0, 0)  # (row, col)

    # --- Combat ---

    def is_alive(self) -> bool:
        """
        Returns True if the player still has health remaining.
        """
        return self.health > 0

    def take_damage(self, amount: int):
        """
        Reduces current health by (amount - defense), with a minimum of 1 damage.
        The max() call ensures defense can never fully negate an attack.
        """
        actual = max(1, amount - self.defense)
        self.health -= actual
        self.health = max(0, self.health)  # Prevent health from going negative
        return actual

    def heal(self, amount: int):
        """
        Increases current health by the specified amount, without exceeding max health.
        """
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health

    # --- Progression ---

    def gain_experience(self, amount: int):
        """
        Adds experience and triggers level_up() if the threshold is reached.
        Uses a while loop so multiple level-ups can occur if a large amount of experience is gained at once.
        """
        self.experience += amount
        while self.experience >= self.experience_to_next_level:
            self.experience -= self.experience_to_next_level
            self.level_up()

    def level_up(self):
        """
        Increases stats and raises the XP bar for the next level.
        The experience required grows by 50% each level, so it increases exponentially.
        """
        self.experience_to_next_level = int(self.experience_to_next_level * 1.5)

        self.level += 1
        self.max_health += 10
        self.health = self.max_health  # Heal to full on level up
        self.attack += 2
        self.defense += 1

        print(f"{self.name} leveled up to level {self.level}! Stats increased.")

    def status(self):
        """
        Prints a neat status block showing the player's current stats and inventory.
        """

        bar_filled = int((self.health / self.max_health) * 10)
        health_bar = "[" + "█" * bar_filled + "░" * (10 - bar_filled) + "]"

        print(f"\n{'=' * 35}")
        print(f"{self.name} - Level {self.level}")
        print(f"Health {health_bar} {self.health}/{self.max_health}")
        print(f"Attack: {self.attack} | Defense: {self.defense}")
        print(
            f"Experience: {self.experience}/{self.experience_to_next_level} | Gold: {self.gold}"
        )
        print(f"{'=' * 35}")

    def __str__(self):
        """
        Returns a string representation of the player.
        """
        return f"{self.name} (Level {self.level}) - HP: {self.health}/{self.max_health}, ATK: {self.attack}, DEF: {self.defense}, EXP: {self.experience}/{self.experience_to_next_level}, Gold: {self.gold}"
