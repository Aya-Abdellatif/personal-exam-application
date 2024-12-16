from DataManager import DataManager
from util import  build_fp_tree, filter_items_with_duplicates, mine_fp_tree


DataManager.prepare_all("Text Data/")

DataManager.merge_csv_files("CSV Data/")

sorted_transactions = DataManager.load_and_sort_csv("transactions.csv")

fp_tree = build_fp_tree(sorted_transactions)

frequent_itemsets = mine_fp_tree(fp_tree.header_table, min_support=30)

print(filter_items_with_duplicates(frequent_itemsets))