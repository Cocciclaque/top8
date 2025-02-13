def readBracketFile(Filename:str) -> list[str]:
    content = []
    lines = []

    gamesArray:list[list[Match]] = [[[Match( "", "")] for _ in range(5)] for _ in range(5)]
    gamesArray[0] = [Match( "", "") for _ in range(6)]
    gamesArray[1] = [[Match( "", "")] for _ in range(4)]
    gamesArray[2] = [[Match( "", "")] for _ in range(2)]
    gamesArray[3] = [[Match( "", "")] for _ in range(2)]
    gamesArray[4] = [[Match( "", "")] for _ in range(2)]

    with open(Filename, "r") as f:
        content = f.readlines()
        content = [elt.rstrip().split(",") for elt in content]
        
        coordinates = []

        for elt in content:
            split = elt[0].split('-')
            elt[0] = [int(split[0]), int(split[1]), int(split[2])]

        for elt in content:
            gamesArray[elt[0][0]][elt[0][1]].addPlayer(Player(elt[1], elt[2]))
            gamesArray[elt[0][0]][elt[0][1]].state = elt[3]
    return gamesArray

class Player:

    def __init__(self, name:str, surname:str):
        
        self.name = name
        self.surname = surname

    def __repr__(self):
        return f" \nPlayer : ({self.name},{self.surname})"

class Match():

    def __init__(self, result:str, state:str):

        self.p1 = None
        self.p2 = None
        self.result = result
        self.state = state

    def addPlayer(self, player):
        if self.p1 == None:
            self.p1 = player
        else:
            self.p2 = player

    def __repr__(self):
        return f"[{self.p1}, {self.p2},\n, {self.result}, {self.state}]"


readBracketFile("bracket.bracket")