import pandas as pd

def calculate_positive_ratios(input_file, output_file):
    data = []  # 存储处理后的数据

    # 打开文件读取数据
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            lines = file.readlines()
            print(f"Total lines read (including header): {len(lines)}")

            # 检查文件是否为空或只有标题
            if len(lines) <= 1:
                print("Input file contains no valid data.")
                return

            for line in lines[1:]:  # 跳过标题行
                line = line.strip()  # 移除首尾空格
                if not line:
                    continue  # 跳过空行

                parts = line.split(",")
                if len(parts) != 4:
                    print(f"Skipping line due to invalid format: {line}")
                    continue

                try:
                    company_id = parts[0]
                    year = parts[1]
                    total_sentences = int(parts[2])
                    positive_sentences = int(parts[3])

                    # 计算正向句子比例，避免除以0
                    ratio = positive_sentences / total_sentences if total_sentences > 0 else 0.0
                    data.append([company_id, year, ratio])

                except ValueError as e:
                    print(f"Skipping line due to value error: {line} - {e}")

    except FileNotFoundError:
        print(f"Input file '{input_file}' not found.")
        return

    # 检查是否有有效数据
    if not data:
        print("No valid data processed. Results file will be empty.")
        return

    # 创建 DataFrame
    df = pd.DataFrame(data, columns=["公司编号", "年份", "正向句子比例"])

    # 保存到 Excel 文件
    try:
        # 不使用 `encoding` 参数
        df.to_excel(output_file, index=False, engine="openpyxl")
        print(f"Data saved to {output_file}")
    except Exception as e:
        print(f"Failed to save data to Excel file: {e}")

# 输入和输出文件路径
input_file = "result.txt"  # 输入文件路径，确保文件存在且格式正确
output_file = r"C:\Users\gxy\Desktop\气候政策不确定性对于企业“漂绿”行为的影响\因变量企业漂绿.xlsx"  # 输出的Excel文件路径

# 执行比例计算并保存
calculate_positive_ratios(input_file, output_file)
