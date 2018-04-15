import sys
import itertools
import os
from copy import deepcopy
from block import Block
from point import Point
from laser import Laser


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

    def __repr__(self):
        '''
        printable representation of object Game. When only initialized, it
        returns the Starting board. Once a solution has been found it returns
        the Solution board.
        '''
        string_to_print = ''
        try:
            string_to_print = "SOLUTION BOARD for %s\n\n" %self.fname
            for list in self.solution_board:
                line = " ".join(map(str, list))
                string_to_print += (line + '\n')
        except:
            string_to_print = "START BOARD for %s\n\n" %self.fname
            for list in self.start_board:
                line = " ".join(map(str, list))
                string_to_print += (line + '\n')
        return string_to_print

    def read(self, fptr):
        '''
        Some function that reads in a file, and generates the internal board.

        **Parameters**

            fptr: *str*
                The file name of the input board to solve.

        **Returns**

            None
        '''
        def check_missing():
            '''
            Function that checks all variables for the game are not empty
            '''
            block_quantity = 0
            for key in self.usable_blocks:
                block_quantity += self.usable_blocks[key]

            if block_quantity == 0:
                raise Exception("There are no blocks on your file!")
            elif not self.start_lazers:
                raise Exception("There are no lasers on your file!")
            elif not self.intersect_points:
                raise Exception("There are no points to intersect on your file!")

        fp = open(fptr, 'rt')
        self.start_board =[] #board that indicataes available spaces and fixed blocks
        self.usable_blocks = {'A': 0, 'B': 0, 'C': 0} #list of the blocks to be put in the board
        self.start_lazers = [] #list of the lazers
        self.intersect_points = [] #list of the points to be intersected
        # gets indexes for self.board layout
        for i, line in enumerate(open(fptr, 'rt')): # goes through file by line to get the info
            # get board indexes to start matrix
            if line == "GRID START\n":
                start_board_line = i + 1
            elif line == "GRID STOP\n":
                end_board_line = i
            #checks for the specific number of blocks to use and make a dictionary
            elif line[0] in ['A', 'B', 'C'] and line[2] not in ['A', 'B', 'C', 'a', 'b', 'c', 'x', 'o', ' ']:
                try:
                    self.usable_blocks[line[0]] = int(line[2])
                except:
                    raise Exception("Whoops! Something is wrong with the way you specified blocks on your file.")
            # have a list of the start points of lasers
            elif line[0] == 'L':
                try:
                    self.start_lazers.append(map(int, line[2:].split(' ')))
                except:
                    raise Exception("Whoops! Something is wrong with the way you specified lasers on your file.")
            # make a list of points that need to be intersected
            elif line[0] == 'P':
                try:
                    self.intersect_points.append(map(int, line[2:].split(' ')))
                except:
                    raise Exception("Whoops! Something is wrong with the way you specified points on your file.")

        # create matrix of the empty start board
        start_board = []
        try:
            for sentence in fp.read().splitlines()[start_board_line:end_board_line]:
                grid_line = []
                for char in sentence:
                    if char in ['x', 'o', 'A', 'B', 'C']:
                        grid_line.append(char)
                start_board.append(grid_line)
            self.start_board = filter(None, start_board)
        except:
            raise Exception("Whoops! Something is wrong the game grid on your file.")

        check_missing()

        fp.close()
        
    def generate_boards(self):
        '''
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

            List of all possible permutations
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

        series = ''
        open_spaces = 0

        #checks how many open spaces are on the board
        for i in self.start_board:
            for j in i:
                if j == 'o':
                    open_spaces += 1

        # makes a list of all usable blocks
        for key in self.usable_blocks:
            series += self.usable_blocks[key]*key

        # Get the different possible block positions.  Note, due to the function we're using, we
        # skip any instance of multiple "stars in bins".
        partitions = [p for p in get_partitions(len(series), open_spaces) if max(p) == 1]

        # gets the permutation of all the blocks to be put in partitions
        blocks_permutations = {"".join(p) for p in itertools.permutations(series)}
        board_permutations = []

        # creates permutations of the board by putting the permutations of the blocks in the corresponding bins
        for partition in partitions:
            for permut in blocks_permutations:
                board_string = ""
                blocks = list(permut)
                for char in partition:
                    if char == 0:
                        board_string +='o'
                    if char == 1:
                        board_string += blocks.pop(0)
                board_permutations.append(board_string)

        return board_permutations

    def set_board(self, board):
        '''
        A function to assign a potential board so that it can be checked.

        **Parameters**

            board: *list, Block*
                A list of block positions.  Note, this list is filled with
                None, unless a block is at said position, then it is a
                Block object.

        **Returns**

            Play_Board
        '''
        #takes a board from the permutations of boards
        board_string = board[:]
        play_board_blocks = deepcopy(self.start_board)

        # assigns the characters of the board string to a play board
        for list in play_board_blocks:
            for indx, char in enumerate(list):
                if char == 'o':
                    list[indx] = board_string[0]
                    board_string = board_string[1:]

        self.solution_board = play_board_blocks

        # creates list of Nones to put the board in and inlcude the points
        play_board =[[None for i in range(((len(play_board_blocks[0]) * 2) + 1))]
                     for j in range(((len(play_board_blocks) * 2) + 1))]

        # puts blocks on the play_board's odd spaces
        blocks_pos = [0, 0]
        for i in range(1,len(play_board) - 1, 2):
            for j in range(1,len(play_board[i]) - 1, 2):
                play_board[i][j] = Block(play_board_blocks[blocks_pos[0]][blocks_pos[1]])
                blocks_pos[1] += 1
            blocks_pos[0] += 1
            blocks_pos[1] = 0

        # puts points on play_board
        for point in self.intersect_points:
            play_board[point[1]][point[0]] = Point(point)

        return play_board
    
    def save_board(self):
        '''
        A function to save potential boards to file.  This is to be used when
        the solution is found, but can also be used for debugging.

        **Returns**

            None
        '''
        #checks if a solution.txt files exists, if so it deletes it
        try:
            os.remove("solution.txt")
        except OSError:
            pass
        # creates a solution.txt file that has the solution board in in
        f = open("solution.txt","w+")
        f.write('~~~ SOLUTION BOARD ~~~\nfor "%s"\n\n' % self.fname)
        f.write("GRID START\n")
        for list in self.solution_board:
            line = " ".join(map(str, list))
            f.write(line + '\n')
        f.write("GRID END\n")
        f.close()
    
    def run(self):
        '''
        The main code is here. We call the generate_boards function, then we
        loop through, using set_board to assign a board, "play" the game,
        check if the board is the solution, if so save_board, if not then
        we loop.

        **Returns**

            None
        '''

        def play_boards(board):
            '''
            A function that plays a board generated by board_permutations.

            **Parameters**

                board: *string*
                    A string with the usable_blocks in the order which they
                    should be on the board.

            **Returns**

                None
            '''
            self.playing_board = self.set_board(board)
            current_lasers = self.start_lazers[:]

            #plays until all of the lasers have been played, including children
            while current_lasers != []:
                all_children = []
                laser = Laser(current_lasers.pop())
                laser.map_trajectory(self.playing_board)
                if laser.children:
                    for child in laser.children:
                        if child not in current_lasers and child not in all_children:
                            current_lasers.append(child)
                            all_children += laser.children

        def check_points():
            '''
            A function checks if all the points have been intersected.

            **Returns**

                Boolean
            '''
            # checks if every point has been intersected
            intersected_points = 0
            for point in self.intersect_points:
                if self.playing_board[point[1]][point[0]].intersected == True:
                    intersected_points += 1

            # if all the points have been intersected then a solution has been found
            if intersected_points == len(self.intersect_points):
                return True
            else:
                return False

        # Get all boards
        print("Generating all the boards..."),
        sys.stdout.flush()
        boards = self.generate_boards()
        print("Done")
        sys.stdout.flush()
        print("Playing boards...")
        sys.stdout.flush()

        # Loop through the boards "play" them
        for board in boards:
            play_boards(board)
            # check if the board played is the solution and if it is save board and break loop
            if check_points():
                self.save_board()
                break

        print "end\n"
        
# # code to run all boards in order (we used this to check if the code was working)
#
# print 'braid_5'
# test = Game("../boards/braid_5.input")
# print test
# test.run()
# print test
#
# print 'diagonal_8'
# test = Game("../boards/diagonal_8.input")
# print test
# test.run()
# print test
#
# print 'diagonal_9'
# test = Game("../boards/diagonal_9.input")
# print test
# test.run()
# print test
#
# print 'mad_1'
# test = Game("../boards/mad_1.input")
# print test
# test.run()
# print test
#
# print 'mad_7'
# test = Game("../boards/mad_7.input")
# print test
# test.run()
# print test
#
# print 'showstopper_2'
# test = Game("../boards/showstopper_2.input")
# print test
# test.run()
# print test
#
# print 'tricky_1'
# test = Game("../boards/tricky_1.input")
# print test
# test.run()
# print test
#
# print 'vertices_1'
# test = Game("../boards/vertices_1.input")
# print test
# test.run()
# print test
#
# print 'vertices_2'
# test = Game("../boards/vertices_2.input")
# print test
# test.run()
# print test
