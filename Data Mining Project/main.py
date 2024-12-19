from data_manager import DataManager
from frequent_pattern_manager import FrequentPatternManager

# Extracts data from text files and save them as csv files
DataManager.prepare_all("Text Data/")

# Merges all csv files into one csv file
DataManager.merge_csv_files("CSV Data/")

# Load all the transactions and sort them to be ready for FP-Tree algorithm
sorted_transactions = DataManager.load_and_sort_csv("transactions.csv")

# Build FP-Tree
fp_tree = FrequentPatternManager.build_fp_tree(sorted_transactions)

# Mine Frequent itemsets using FP-Tree algorithm
frequent_itemsets = FrequentPatternManager.mine_fp_tree(
    fp_tree.header_table, min_support=30
)


print(FrequentPatternManager.filter_items_with_duplicates(frequent_itemsets))
