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

    # MORE
    # Difficulty 4 Everyone
