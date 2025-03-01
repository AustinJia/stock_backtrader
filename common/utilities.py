from pathlib import Path
import os

def processing_signal(pre_50, cur_50, pre_200, cur_200):
        if (pre_50 <= pre_200) and (cur_50 >= cur_200):
            return "BUY"
        elif (pre_50 >= pre_200) and (cur_50 <= cur_200):
            return "SELL"
        return "IDLE"

def find_file_in_subdir(path, file_name):
    # file_name = tricker+'_historical_data copy.csv'
    for file in os.listdir(path):
        full_path = os.path.join(path, file)
        if file.endswith(file_name):
            return True
        elif os.path.isdir(full_path) and not full_path.endswith('venv'):
            return find_file_in_subdir(full_path, file_name)
    return False