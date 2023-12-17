import itertools
import random


class Minesweeper:
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):
        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for _ in range(self.height):
            row = [False for _ in range(self.width)]
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i, j in itertools.product(
            range(cell[0] - 1, cell[0] + 2), range(cell[1] - 1, cell[1] + 2)
        ):
            # Ignore the cell itself
            if (i, j) == cell:
                continue

            # Update count if cell in bounds and is mine
            if 0 <= i < self.height and 0 <= j < self.width:
                if self.board[i][j]:
                    count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence:
    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        return self.cells if len(self.cells) == self.count else set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        return self.cells if self.count == 0 else set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI:
    def __init__(self, height=8, width=8):
        self.height = height
        self.width = width
        self.moves_made = set()
        self.mines = set()
        self.safes = set()
        self.knowledge = []

    def mark_mine(self, cell):
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        self.moves_made.add(cell)
        self.mark_safe(cell)

        new_sentence_cells = self.get_neighbors(cell)
        new_sentence_cells -= self.safes.union(self.moves_made)
        new_sentence = Sentence(new_sentence_cells, count)
        self.knowledge.append(new_sentence)

        for sentence in self.knowledge:
            known_mines = sentence.known_mines()
            known_safes = sentence.known_safes()

            if known_mines:
                self.mines.update(known_mines)
            if known_safes:
                self.safes.update(known_safes)

        self.update_inferred_sentences()

    def make_safe_move(self):
        return next((cell for cell in self.safes if cell not in self.moves_made), None)

    def make_random_move(self):
        possible_moves = list(itertools.product(range(self.height), range(self.width)))
        if possible_moves := set(possible_moves) - self.moves_made - self.mines:
            return random.choice(list(possible_moves))
        return None

    def update_inferred_sentences(self):
        for set1, count1 in itertools.product(self.knowledge, repeat=2):
            if set1.cells.issubset(count1.cells) and set1 != count1:
                new_cells = count1.cells - set1.cells
                new_count = count1.count - set1.count
                new_sentence = Sentence(new_cells, new_count)
                if new_sentence not in self.knowledge:
                    self.knowledge.append(new_sentence)

    def get_neighbors(self, cell):
        i, j = cell
        return {
            (x, y)
            for x, y in itertools.product(
                range(max(0, i - 1), min(self.height, i + 2)),
                range(max(0, j - 1), min(self.width, j + 2)),
            )
            if (x, y) != cell
        }
