# dungeon.py

import random

# We'll use these symbols to render the map in the terminal
TILE_WALL = "#"
TILE_FLOOR = "."
TILE_PLAYER = "@"
TILE_ENEMY = "E"
TILE_ITEM = "!"
TILE_EXIT = "X"
TILE_UNKNOWN = " "  # For unexplored areas


class Room:
    """
    Represents a single cell in the dungeon grid.

    Attributes:
        row, col : The position of the room in the grid.
        room_type (str): The type of the room (e.g., 'empty', 'enemy', 'item', 'exit').
        explored (bool): Whether the player has explored this room.
        enemy (Enemy): The enemy present in the room, if any.
        item (Item): The item present in the room, if any.
    """

    def __init__(self, row: int, col: int, room_type: str = "floor"):
        self.row = row
        self.col = col
        self.room_type = room_type
        self.explored = False
        self.enemy = None
        self.item = None

    def is_walkable(self) -> bool:
        """
        Returns True if the player can move into floors and the exit.
        """
        return self.room_type in ["floor", "exit"]

    def __str__(self):
        return f"Room({self.row}, {self.col}, type={self.room_type}, explored={self.explored})"


class Dungeon:
    """
    Holds the full grid of Rooms and handles generation and rendering.

    Attributes:
        rows, cols (int): The dimensions of the dungeon.
        grid (list): A 2D list of Room objects representing the dungeon layout.
        exit_position (tuple): The (row, col) coordinates of the exit room.
    """

    def __init__(self, rows: int = 8, cols: int = 12):
        self.rows = rows
        self.cols = cols
        self.grid = []
        self.exit_position = None
        self._generate()

    # --- Generation ---

    def _generate(self):
        """
        Builds the dungeon grid with rooms.
        """
        self.grid = []

        for row in range(self.rows):
            current_row = []
            for col in range(self.cols):

                # Border cells are always walls
                if row == 0 or row == self.rows - 1:
                    room_type = "wall"
                elif col == 0 or col == self.cols - 1:
                    room_type = "wall"
                else:
                    # Interior cells: 20% chance of being a wall, otherwise floor
                    room_type = "wall" if random.random() < 0.2 else "floor"

                current_row.append(Room(row, col, room_type))
            self.grid.append(current_row)

        # Place the exit in the bottom-right area
        exit_row = self.rows - 2
        exit_col = self.cols - 2
        self.grid[exit_row][exit_col].room_type = "exit"
        self.exit_position = (exit_row, exit_col)

        # Guarantee the starting room (top-left interior) is walkable
        self.grid[1][1].room_type = "floor"

    # --- Access Helpers ---

    def get_room(self, row: int, col: int) -> Room:
        """
        Safe room accessor.
        """
        return self.grid[row][col]

    def is_valid_position(self, row: int, col: int) -> bool:
        """
        Checks the position is inside the grid AND walkable.
        """
        if row < 0 or row >= self.rows:
            return False
        if col < 0 or col >= self.cols:
            return False
        return self.get_room(row, col).is_walkable()

    def explore_around(self, row: int, col: int):
        """
        Marks the room the player is in, plus all 8 neighbours as explored.
        """
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                r = row + dr
                c = col + dc
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    self.get_room(r, c).explored = True

    # --- Rendering ---

    def render(self, player_pos: tuple):
        """
        Prints the dungeon to the terminal.
        player_pos is a (row, col) tuple passed in from the Player object.
        """
        print()
        for row in range(self.rows):
            row_str = ""
            for col in range(self.cols):
                room = self.grid[row][col]

                # Player takes visual priority over overthing
                if (row, col) == player_pos:
                    row_str += TILE_PLAYER

                # Unexplored rooms are hidden (fog of war)
                elif not room.explored:
                    row_str += TILE_UNKNOWN

                elif room.room_type == "wall":
                    row_str += TILE_WALL

                elif room.room_type == "exit":
                    row_str += TILE_EXIT

                elif room.enemy is not None:
                    row_str += TILE_ENEMY

                elif room.item is not None:
                    row_str += TILE_ITEM

                else:
                    row_str += TILE_FLOOR
            print(row_str)
        print()


if __name__ == "__main__":
    d = Dungeon()
    player_start = (1, 1)
    d.explore_around(*player_start)  # reveal starting area
    d.render(player_start)
    print(d.get_room(1, 1))
    print("Exit at:", d.exit_position)
