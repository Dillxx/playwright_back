import csv
import os


def get_csv_data(file_name):
    # 1. 获取当前文件 (read_data.py) 的绝对路径
    current_path = os.path.abspath(__file__)

    # 2. 获取项目根目录 (假设 data 文件夹在项目根目录下)
    # os.path.dirname 返回上一级目录，根据你的目录结构可能需要调用两次
    project_root = os.path.dirname(os.path.dirname(current_path))

    # 3. 拼接出 CSV 的绝对路径
    full_path = os.path.join(project_root, "data", file_name)

    data_list = []
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"找不到 CSV 文件，请检查路径: {full_path}")

    with open(full_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data_list.append(row)
    return data_list