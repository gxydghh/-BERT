# 输入文件路径
input_file = 'company_sentence_counts_and_sentences.txt'

# 输出文件路径
output_file = 'company_year_sentence_counts2.txt'

# 用于存储结果
result = []

with open(input_file, 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        # 跳过空行或不符合格式的行
        if not line.strip() or not line.startswith("公司"):
            continue

        # 分割行内容，确保分割后的列表长度足够
        parts = line.split()
        if len(parts) < 3:  # 如果长度不足，跳过当前行
            continue

        company_id = parts[1]  # 公司编号
        year = parts[2].strip("年的")  # 年份
        count = parts[-1].split("：")[-1].strip()  # 句子数量

        # 添加到结果列表
        result.append(f"{company_id} {year} {count}")

# 写入结果文件
with open(output_file, 'w', encoding='utf-8') as file:
    for item in result:
        file.write(item + "\n")

print(f"统计完成，结果已保存到 '{output_file}' 文件中。")
