import os
import hashlib
import logging
from datetime import datetime

def setup_logging():
    """
    設定日誌記錄
    """
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_filename = datetime.now().strftime("%Y-%m-%d") + "-repeatMp3.log"
    log_filepath = os.path.join(log_dir, log_filename)
    logging.basicConfig(filename=log_filepath, level=logging.INFO, format='%(asctime)s - %(message)s')

def get_file_hash(filepath):
    """
    计算文件的哈希值
    """
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buffer = f.read()
        hasher.update(buffer)
    return hasher.hexdigest()

def remove_duplicate_mp3(directory):
    """
    刪除重複的 MP3 文件，並保留唯一的文件
    """
    setup_logging()
    logging.info(f"Starting duplicate MP3 removal for directory: {directory}")

    print(os.walk(directory))
    mp3_files = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.mp3'):
                filepath = os.path.join(root, file)
                file_hash = get_file_hash(filepath)
                if file_hash in mp3_files:
                    # 刪除重複文件
                    logging.info(f"Removing duplicate: {filepath}")
                    os.remove(filepath)
                else:
                    mp3_files[file_hash] = filepath

    logging.info("Duplicate MP3 removal completed.")

if __name__ == "__main__":
    input_dir = input("Enter a directory to clean: ")
    input_dir = input_dir if input_dir else "downloads"
    current_directory = os.getcwd()
    directory_to_clean = os.path.join(current_directory, input_dir)

    remove_duplicate_mp3(directory_to_clean)
