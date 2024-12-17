class FPTreeNode:
    def __init__(self, item, count=1):
        self.item = item
        self.count = count
        self.children = {}
        self.parent = None

    def increment(self, count=1):
        self.count += count
