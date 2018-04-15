from point import Point
class Laser:
    '''
    The Laser.  We need to store both the starting position and direction of
    the laser.
    '''
    def __init__(self, laser):
        '''
        Initialize a laser object.

        **Parameters**

            laser: *list*
                list of starting position and direction

        **Returns**

            laser: *Laser*
                This laser object
        '''

        self.starting_pos = laser[:2]
        self.direction = laser[2:]
        self.children = []

    def map_trajectory(self, play_board):
        '''
        Creates a list with the laser trajectory and changes the intersected
        property of points if they are intersected by the laser

        **Parameters**

            play_board: *list*
                list of the board to be played with the blocks and points
                to be intersected

        **Returns**

            None
        '''
        def check_if_out(play_board, pos):
            '''
            Checks if a postion is valid in play_board

            **Parameters**

                play_board: *list*
                    list of the board to be played with the blocks and points
                    to be intersected

                pos: *list*
                    position to check

            **Returns**

                Boolean
            '''
            if pos[1] in range(0,len(play_board)) and pos[0] in range(0, len(play_board[0])):
                return True
            else:
                return False

        current_pos = self.starting_pos[:]
        current_direction = self.direction[:]
        trajectory = [self.starting_pos[:] + self.direction[:]]

        #checks if the current_pos is valid
        while check_if_out(play_board, current_pos):

            #checks if postion is at a Point and if it is changes the property intersected of the Point
            if isinstance(play_board[current_pos[1]][current_pos[0]], Point):
                play_board[current_pos[1]][current_pos[0]].intersected = True

            #if position in odd index_x checks side blocks and updates the current direction
            if current_pos[0]%2 != 0:
                try:
                    block_to_check = play_board[current_pos[1] + current_direction[1]][current_pos[0]]
                    #checks if the block is a refract block to create children
                    if block_to_check.prop['refract'] == True:
                        self.children.append([sum(x) for x in zip(current_pos, current_direction)] + current_direction)
                    #update direction according to the block properties
                    current_direction = [a*b for a, b in zip(current_direction, block_to_check.prop['updown'])]
                except:
                    break
            #if position in even index_x checks the blocks up or down and updates the current direction
            elif current_pos[0]%2 == 0:
                try:
                    block_to_check = play_board[current_pos[1]][current_pos[0] + current_direction[0]]
                    #checks if the block is a refract block to create children
                    if block_to_check.prop['refract'] == True:
                        self.children.append([sum(x) for x in zip(current_pos, current_direction)] + current_direction)
                    #update direction according to the block properties
                    current_direction = [a*b for a, b in zip(current_direction, block_to_check.prop['leftright'])]
                except:
                    break

            #updating current_pos with the new direction
            current_pos = [sum(x) for x in zip(current_pos, current_direction)]

            # when [current_pos, current_direction] is in trajectory there is an infinite Loop
            # when current_direction == [0, 0] we hit a B block and the trajectory ends
            # in both cases we should stop runnign laser.trajectory, else we should add new pos to the trajectory
            if current_pos + current_direction in trajectory or current_direction == [0, 0]:
                break
            else:
                trajectory.append(current_pos + current_direction)


            None
        '''
        def check_if_out(play_board, pos):
            '''
            Checks if a postion is valid in play_board

            **Parameters**

                play_board: *list*
                    list of the board to be played with the blocks and points
                    to be intersected

                pos: *list*
                    position to check

            **Returns**

                Boolean
            '''
            if pos[1] in range(0,len(play_board)) and pos[0] in range(0, len(play_board[0])):
                return True
            else:
                return False
