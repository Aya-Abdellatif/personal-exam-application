import unittest
from frequent_pattern import FPTree, FPTreeNode, FrequentPatternManager

class TestFPTree(unittest.TestCase):
    def test_fp_tree_node_increment(self):
        node = FPTreeNode("A")
        self.assertEqual(node.count, 1)
        node.increment()
        self.assertEqual(node.count, 2)

    def test_fp_tree_add_transaction(self):
        tree = FPTree()
        transaction = ["A", "B", "C"]
        tree.add_transaction(transaction)

        self.assertIn("A", tree.root.children)
        self.assertIn("B", tree.root.children["A"].children)
        self.assertIn("C", tree.root.children["A"].children["B"].children)

        self.assertEqual(tree.root.children["A"].count, 1)
        self.assertEqual(tree.root.children["A"].children["B"].count, 1)
        self.assertEqual(tree.root.children["A"].children["B"].children["C"].count, 1)

    def test_fp_tree_header_table(self):
        tree = FPTree()
        transactions = [["A", "B"], ["A", "C"], ["A", "B"]]
        for transaction in transactions:
            tree.add_transaction(transaction)

        self.assertIn("A", tree.header_table)
        self.assertIn("B", tree.header_table)
        self.assertIn("C", tree.header_table)

        self.assertEqual(len(tree.header_table["A"]), 1)
        self.assertEqual(len(tree.header_table["B"]), 1)
        self.assertEqual(len(tree.header_table["C"]), 1)

        self.assertEqual(tree.header_table["A"][0].count, 3)

class TestFrequentPatternManager(unittest.TestCase):
    def test_build_fp_tree(self):
        transactions = [["A", "B"], ["A", "C"], ["A", "B", "D"]]
        fp_tree = FrequentPatternManager.build_fp_tree(transactions)

        self.assertIsInstance(fp_tree, FPTree)
        self.assertIn("A", fp_tree.root.children)
        self.assertIn("B", fp_tree.root.children["A"].children)
        self.assertIn("C", fp_tree.root.children["A"].children)

    def test_mine_fp_tree(self):
        transactions = [["A", "B"], ["A", "C"], ["A", "B", "D"]]
        fp_tree = FrequentPatternManager.build_fp_tree(transactions)
        frequent_itemsets = FrequentPatternManager.mine_fp_tree(fp_tree.header_table, min_support=2)

        expected_itemsets = [
            (["A"], 3),
            (["B"], 2),
            (["B", "A"], 2),
        ]

        self.assertCountEqual(frequent_itemsets, expected_itemsets)

    def test_filter_items_with_duplicates(self):
        frequent_itemsets = [
            (["A", "B"], 2),
            (["A", "A"], 3),
            (["B", "C", "C"], 1),
        ]
        filtered = FrequentPatternManager.filter_items_with_duplicates(frequent_itemsets)

        expected_filtered = [
            (["A", "B"], 2),
        ]
        self.assertEqual(filtered, expected_filtered)

if __name__ == "__main__":
    unittest.main()
