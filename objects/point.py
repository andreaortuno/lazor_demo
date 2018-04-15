class Point:
    '''
    The Point.  This object desribes the points for which we want the laser
    light to intersect.
    '''
    def __init__(self, pos):
        '''
        Initialize a point object.

        **Parameters**

            pos: *list*
                The postion of the point on the board

        **Returns**

            point: *Point*
                This point object
        '''
        self.postiion = pos
        self.intersected = False
