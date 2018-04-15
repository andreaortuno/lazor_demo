import sys
import copy
import itertools
# import the Point, Block, and Laser objects


class Game:
    '''
    The game grid.  Here we read in some user input, assign all our blocks,
    lasers, and points, determine all the possible different combinations
    of boards we could make, and then run through them all to try and find
    the winning one.
    '''

    def __init__(self, fptr):
        '''
        Difficulty 1 Andrea

        Initialize our game.

        **Parameters**

            fptr: *str*
                The file name of the input board to solve.

        **Returns**

            game: *Game*
                This game object.
        '''
        self.fname = fptr
        self.read(fptr)

    # DO SOMETHING HERE SO WE CAN PRINT A REPRESENTATION OF GAME!

    def read(self, fptr):
        '''
        Difficulty 3 Andrea

        Some function that reads in a file, and generates the internal board.

        **Parameters**

            fptr: *str*
                The file name of the input board to solve.

        **Returns**

            None
        '''
        fp = open(fptr, 'rt')
        board =[]
        usable_blocks = {'a': 0, 'b': 0, 'c': 0}
        start_lazers = []
        intersect_points = []
        # gets indexes for board layout
        for i, line in enumerate(open(fptr, 'rt')):
            # get board indexes to start matrix
            if line == "GRID START\n":
                start_board_line = i + 1
            elif line == "GRID STOP\n":
                end_board_line = i
            #checks for the specific number of blocks to use and make a dictionary
            elif line[0] == 'A':
                usable_blocks['a'] = int(line[2])
            elif line[0] == 'B':
                usable_blocks['b'] = int(line[2])
            elif line[0] == 'C':
                usable_blocks['c'] = int(line[2])
            # have a list of the start points of lasers
            elif line[0] == 'L':
                start_lazers.append(map(int, line[2:-1].split(' ')))
            # make a list of points that need to be intersected
            elif line[0] == 'P':
                intersect_points.append(map(int, line[2:-1].split(' ')))

        # create matrix of the empty board
        for sentence in fp.read().splitlines()[start_board_line:end_board_line]:
            grid_line = []
            for char in sentence:
                if char == 'x':
                    grid_line.append('x')
                elif char == 'o':
                    grid_line.append('o')
                elif char == 'A':
                    grid_line.append('A')
                elif char == 'B':
                    grid_line.append('B')
                elif char == 'C':
                    grid_line.append('C')
            board.append(grid_line)

        #TO DO MAYBE assign all below vaiables to self.whatever
        print board
        print usable_blocks
        print start_lazers
        print intersect_points
        # Length of board for half steps: x, y = 2 * len(board), 2 * len(board[0])
        # file errors to display
        # No GRID START or END
        # No Usable blocks defined
        # No start of lazer defined
        # No intersect points defined


    def generate_boards(self):
        '''
        Difficulty 3 Apeksha

        A function to generate all possible board combinations with the
        available blocks.

        First get all possible combinations of blocks on the board (we'll call these boards)
          We know we have self.blocks, and N_blocks = len(self.blocks)
          We also know we have self.available_space
          So, essentially we have to find all the possible ways to put N_blocks into
          self.available_space
        This becomes the "stars and bars" problem; however, we have distinguishable "stars",
        and further we restrict our system so that only one thing can be put in each bin.

        **Returns**

            None
        '''

        def get_partitions(n, k):
            '''
            A robust way of getting all permutations.  Note, this is clearly not the fastest
            way about doing this though. Andrea

            **Reference**

             - http://stackoverflow.com/a/34690583
            '''
            for c in itertools.combinations(range(n + k - 1), k - 1):
                yield [b - a - 1 for a, b in zip((-1,) + c, c + (n + k - 1,))]

        # Get the different possible block positions.  Note, due to the function we're using, we
        # skip any instance of multiple "stars in bins".
        partitions = [
            p for p in get_partitions(len(self.blocks), self.available_space) if max(p) == 1
        ]


        # Now we have the partitions, we just need to make our boards
        boards = []

        # YOUR CODE HERE
        pass

    def set_board(self, board):
        '''
        Difficulty 2 Andrea

        A function to assign a potential board so that it can be checked.

        **Parameters**

            board: *list, Block*
                A list of block positions.  Note, this list is filled with
                None, unless a block is at said position, then it is a
                Block object.

        **Returns**

            None
        '''
        # YOUR CODE HERE
        pass

    def save_board(self):
        '''
        Difficulty 2 Apeksha, KK

        A function to save potential boards to file.  This is to be used when
        the solution is found, but can also be used for debugging.

        **Returns**

            None
        '''
        # YOUR CODE HERE
        pass

    def run(self):
        '''
        Difficulty 3 KK

        The main code is here.  We call the generate_boards function, then we
        loop through, using set_board to assign a board, "play" the game,
        check if the board is the solution, if so save_board, if not then
        we loop.

        **Returns**

            None
        '''

        # Get all boards
        print("Generating all the boards..."),
        sys.stdout.flush()
        boards = self.generate_boards()
        print("Done")
        sys.stdout.flush()

        print("Playing boards...")
        sys.stdout.flush()
        # Loop through the boards, and "play" them
        for b_index, board in enumerate(boards):
            # Set board
            self.set_board(board)

            # MAYBE MORE CODE HERE?

            # LOOP THROUGH LASERS
            for j, laser in enumerate(current_lasers):
              child_laser = None
              child_laser = laser.update(self.board, self.points)

            # MAYBE MORE CODE HERE?

            # CHECKS HERE
test = Game("test.input")
