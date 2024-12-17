from fp_tree_node import FPTreeNode


class FPTree:
    def __init__(self):
        self.root = FPTreeNode(None)  # Root node
        self.header_table = {}

    def add_transaction(self, transaction):
        current_node = self.root

        for item in transaction:
            if item in current_node.children:
                current_node.children[item].increment()
            else:
                new_node = FPTreeNode(item)
                new_node.parent = current_node
                current_node.children[item] = new_node

                # Update header table
                if item not in self.header_table:
                    self.header_table[item] = []
                self.header_table[item].append(new_node)

            current_node = current_node.children[item]
