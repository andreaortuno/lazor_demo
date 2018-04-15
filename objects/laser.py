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
