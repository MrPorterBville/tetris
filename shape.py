import json as j


class pieces:
    def __init__(self, type):
        self.type = type
        self.pieceShape = []
        self.pieceColor = []
        self.location = 0
        self.loadJson()

    def loadJson(self):
        try:
            with open('pieces.json', 'r') as f:
                data = j.load(f)
            
            # Search the list for the piece that matches self.type
            for p in data['pieces']:
                if p['name'] == self.type:
                    self.pieceShape = p['shape']
                    self.pieceColor = p['color']
                    return # Exit once we find it
            
            print(f"Error: Piece type '{self.type}' not found in JSON.")
            
        except FileNotFoundError:
            print("Error: pieces.json file not found.")

    def dropRow(self):
        self.location +=1

    def color(self):
        return self.pieceColor
    
    def shape(self):
        return self.pieceShape
