from fp_tree import  FPTree


def build_fp_tree(sorted_transactions) -> FPTree:
    fp_tree = FPTree()
    for transaction in sorted_transactions:
        fp_tree.add_transaction(transaction)
    return fp_tree

def mine_fp_tree(header_table, min_support=2, prefix=None):
    if prefix is None:
        prefix = []

    frequent_itemsets = []
    for item, nodes in header_table.items():
        # Calculate the support for the item
        support = sum(node.count for node in nodes)
        if support >= min_support:
            new_prefix = prefix + [item]
            frequent_itemsets.append((new_prefix, support))

            # Build conditional pattern base
            conditional_pattern_base = []
            for node in nodes:
                path = []
                parent = node.parent
                while parent and parent.item is not None:
                    path.append(parent.item)
                    parent = parent.parent
                for _ in range(node.count):
                    conditional_pattern_base.append(path)

            # Build conditional FP-tree
            conditional_tree = FPTree()
            for transaction in conditional_pattern_base:
                conditional_tree.add_transaction(transaction)

            # Recursively mine the conditional FP-tree
            frequent_itemsets += mine_fp_tree(conditional_tree, conditional_tree.header_table, min_support, new_prefix)

    return frequent_itemsets

def filter_items_with_duplicates(frequent_itemsets: list[tuple[list[str], int]]):
    return [
        (topics, count) 
        for topics, count in frequent_itemsets 
        if len(topics) == len(set(topics))
    ]

    