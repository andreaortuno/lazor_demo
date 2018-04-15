class Block:
    '''
    A generic block for lazor.  We make this extendable so that it can be
    defined as either:

        (a) Reflecting block - Only reflects the laser
        (b) Opaque block - Absorbs the laser
        (c) See-Through block - Both reflects and lets light pass
    '''
    def __init__(self, block_type):
        '''
        Initialize a block object and assigns the block properties

        **Parameters**

            block_type: *string*
                string with the block type [A, B, C, X, etc]

        **Returns**

            block: *Block*
                This block object
        '''
        #dictionary of possible properties
        block_pro = {'A': {'updown': (1, -1), 'leftright': (-1, 1), 'refract': False},
                     'B': {'updown': (0, 0), 'leftright': (0, 0), 'refract': False},
                     'C': {'updown': (1, -1), 'leftright': (-1, 1), 'refract': True},
                     'o': {'updown': (1, 1), 'leftright': (1, 1), 'refract': False}}

        #checks block_type and assigns properties to the Block
        if block_type in ['a', 'A']:
            self.blk_type = 'A'
            self.prop = block_pro[self.blk_type]
        elif block_type in ['b', 'B']:
            self.blk_type = 'B'
            self.prop = block_pro[self.blk_type]
        elif block_type in ['c', 'C']:
            self.blk_type = 'C'
            self.prop = block_pro[self.blk_type]
        #in a "solution board" if a postion has 'x or o' they are treated as empty blocks
        elif block_type in ['x', 'o']:
            self.blk_type = 'o'
            self.prop = block_pro[self.blk_type]
        else:
            raise TypeError('Invalid block type')
