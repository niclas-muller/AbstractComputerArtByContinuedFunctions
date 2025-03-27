import pandas as pd

class Node():

    def __init__(self, name=None):
        self.name = name
        self.value = 0
        self.children = []
        self.parent = None

    def __str__(self):
        name = self.name
        parent = self.parent
        while parent:
            if parent.name is not None:
                name = f'{parent.name}:{name}'
            parent = parent.parent
        return f'{name}:{self.value}'

    def hasChild(self, childName):
        for child in self.children:
            if child.name == childName:
                return True
        return False

    def createChild(self, childName):
        new = Node(name=childName)
        new.parent = self
        self.children.append(new)

    def child(self, childName):
        for child in self.children:
            if child.name == childName:
                return child
        return None

    def addValue(self, value):
        self.value += value

class FunctionTree():
    
    def __init__(self,df):
        self.df = df
        self.root = Node()
        self.buildTree()
        self.displayTree()

    def buildTree(self):
        for index, row in df.iterrows():
            rank = row.tot_rank
            function = row.Comment
            focus = self.root
            for funcAtom in function.split('_'):
                funcAtom = funcAtom.split(':')[0]
                if not focus.hasChild(funcAtom):
                    focus.createChild(funcAtom)
                focus.child(funcAtom).addValue(rank)
                focus = focus.child(funcAtom)

    def displayTree(self):
        for child1 in self.root.children:
            for child2 in child1.children:
                for child3 in child2.children:
                    for child4 in child3.children:
                        print(child4)

df = pd.read_excel('frameOverviews/FrameOverview_0.xlsx')[['Comment', 'tot_rank']]
Tree = FunctionTree(df)
