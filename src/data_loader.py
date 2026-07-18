import pandas as pd


def load_data(file_path: str) -> pd.DataFrame | None:
    """
    Read a CSV file and return a pandas DataFrame.

开始读取数据
↓
读取成功？
↓
如果成功：
    打印：
    数据读取成功！
    数据共有 xxx 行 xxx 列
↓
返回 DataFrame
↓
如果失败：
    打印错误原因
    """
    try:
        df = pd.read_csv(file_path, encoding="latin1")
        print("数据读取成功！")
        print(f"数据共有 {df.shape[0]} 行 {df.shape[1]} 列")
        return df
    except Exception as e:
        print(f"数据读取失败：{e}")
        return None
