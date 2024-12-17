from data_manager import DataManager
from frequent_pattern_manager import FrequentPatternManager


DataManager.prepare_all("Text Data/")

DataManager.merge_csv_files("CSV Data/")

sorted_transactions = DataManager.load_and_sort_csv("transactions.csv")

fp_tree = FrequentPatternManager.build_fp_tree(sorted_transactions)

frequent_itemsets = FrequentPatternManager.mine_fp_tree(
    fp_tree.header_table, min_support=30
)

print(FrequentPatternManager.filter_items_with_duplicates(frequent_itemsets))
