from DataManager import DataManager

data_manager = DataManager()

data_manager.prepare_all("Text Data/")

data_manager.merge_csv_files("CSV Data/")
