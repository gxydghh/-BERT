import csv

# 输入文件路径（您的原始数据）
input_file = "s.txt"  # 替换为您的标注数据文件路径
output_file = "dataset.csv"  # 输出的CSV文件路径

# 打开输入文件并读取内容
with open(input_file, "r", encoding="utf-8") as infile:
    lines = infile.readlines()

# 准备写入 CSV 文件
with open(output_file, "w", newline="", encoding="utf-8") as outfile:
    csv_writer = csv.writer(outfile)
    # 写入 CSV 文件头部
    csv_writer.writerow(["sentence", "label"])

    # 逐行处理输入文件
    for line in lines:
        line = line.strip()
        if not line:
            continue  # 跳过空行

        # 将句子和标签分开
        if "@" in line and "," in line:
            sentence, label = line.rsplit(",", 1)  # 分割句子和标签
            sentence = sentence.rstrip("@")  # 去掉句子末尾的 @
            label = label.strip()  # 去掉标签的空白字符
            # 写入到CSV
            csv_writer.writerow([sentence, label])

print(f"数据已成功转换为 CSV 文件，保存为 {output_file}")
