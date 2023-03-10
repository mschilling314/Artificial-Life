from pyrosim.commonFunctions import Save_Whitespace

class MATERIAL: 

    def __init__(self, cS='<color rgba="0 0 1 1"/>', col="Blue"):

        self.depth  = 3

        self.string1 = '<material name="' + col + '">'

        self.string2 = cS

        self.string3 = '</material>'

    def Save(self,f):

        Save_Whitespace(self.depth,f)

        f.write( self.string1 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string2 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string3 + '\n' )
