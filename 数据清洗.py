import re


# 用于清洗句子的函数，保留中文、逗号、分号，并保留句末的@
def clean_sentence(sentence):
    # 保留中文字符、逗号、分号，删除其他字符，但保留句子末尾的@
    cleaned_sentence = re.sub(r'[^\u4e00-\u9fa5，；@]', '', sentence)  # 清洗掉不需要的符号
    return cleaned_sentence


# 输入和输出文件路径
input_file = 'company_sentence_counts_and_sentences.txt'  # 输入文件路径
output_file = 'cleaned_company_sentences.txt'  # 输出清洗后的文件路径

with open(input_file, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 用于存储清洗后的句子
cleaned_lines = []

# 清洗每一行的内容
for line in lines:
    line = line.strip()

    # 如果是公司编号-年份-句子数量的开头行，不做处理，直接添加到结果
    if line.startswith("公司"):
        cleaned_lines.append(line)
    elif line and line.endswith('@'):  # 处理包含句子的行，确保句子非空且以 @ 结尾
        sentence = line[:-1].strip()  # 去掉末尾的 @
        cleaned_sentence = clean_sentence(sentence)  # 清洗句子
        cleaned_lines.append(cleaned_sentence + '@')  # 重新加上 @ 符号

# 将清洗后的句子写入输出文件
with open(output_file, 'w', encoding='utf-8') as output:
    for cleaned_line in cleaned_lines:
        output.write(cleaned_line + '\n')

print(f"清洗完成，结果已保存到 '{output_file}' 文件中。")
