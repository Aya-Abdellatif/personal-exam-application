from DataManager import DataManager
from util import  build_fp_tree, mine_fp_tree

data_manager = DataManager()

data_manager.prepare_all("Text Data/")

data_manager.merge_csv_files("CSV Data/")

sorted_transactions = DataManager.load_and_sort_csv("transactions.csv")

fp_tree = build_fp_tree(sorted_transactions)

frequent_itemsets = mine_fp_tree(fp_tree, fp_tree.header_table, min_support=2)

print(frequent_itemsets)