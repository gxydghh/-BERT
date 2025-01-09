import os
import jieba
import re
from collections import defaultdict


# 读取扩展词文件，并将其加载到列表中
def load_filtered_words(file_path):
    with open(file_path, 'r',  encoding='utf-8') as f:
        words = [line.strip() for line in f if line.strip()]  # 读取文件中的每一行并去除空白字符
    return words


# 扩展词文件路径
filtered_words_file = '200.txt'

# 读取扩展词
filtered_words = load_filtered_words(filtered_words_file)
print(f"加载了 {len(filtered_words)} 个扩展词。")

# 用于存储每个公司编号和年份的符合条件句子数量和句子内容
company_data = defaultdict(lambda: defaultdict(lambda: {'count': 0, 'sentences': []}))


# 提取文本中的句子
def extract_sentences_from_text(text):
    # 使用正则表达式将文本分割为句子（根据中文标点符号）
    sentences = re.split(r'[。！？]', text)
    # 清理句子并添加结束符号 @
    return [s.strip().replace('\n', '').replace('\r', '') + '@' for s in sentences if s.strip()]


# 检查句子是否包含任何过滤词
def contains_filtered_words(sentence):
    words = jieba.lcut(sentence)  # 使用jieba进行分词
    for word in words:
        if word in filtered_words:  # 如果包含任何过滤词
            return True
    return False


# 处理社会责任报告文件夹
def process_responsibility_reports(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            # 假设文件名格式：公司编号-年份-公司名
            parts = filename.split('-')
            company_id = parts[0]  # 公司编号
            year = parts[1]  # 年份
            file_path = os.path.join(folder_path, filename)

            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()

                # 提取句子并检查是否包含过滤词
                sentences = extract_sentences_from_text(text)
                for sentence in sentences:
                    if contains_filtered_words(sentence):
                        company_data[company_id][year]['count'] += 1  # 累加符合条件的句子数量
                        company_data[company_id][year]['sentences'].append(sentence)  # 存储符合条件的句子


# 处理管理层报告文件夹（递归处理年份和文本文件夹）
def process_management_reports(folder_path):
    for year_folder in os.listdir(folder_path):
        year_path = os.path.join(folder_path, year_folder)

        # 确保是文件夹且名称为年份
        if os.path.isdir(year_path) and year_folder.isdigit():
            text_folder = os.path.join(year_path, '文本')  # 进入年份文件夹下的 '文本' 文件夹
            if os.path.exists(text_folder) and os.path.isdir(text_folder):
                # 处理 '文本' 文件夹中的所有文件
                for filename in os.listdir(text_folder):
                    if filename.endswith(".txt"):
                        company_id = filename.split('_')[0]  # 假设文件名格式：公司编号_年份-月份
                        year = filename.split('_')[1].split('-')[0]  # 提取年份
                        file_path = os.path.join(text_folder, filename)

                        with open(file_path, 'r', encoding='utf-8') as file:
                            text = file.read()

                            # 提取句子并检查是否包含过滤词
                            sentences = extract_sentences_from_text(text)
                            for sentence in sentences:
                                if contains_filtered_words(sentence):
                                    company_data[company_id][year]['count'] += 1  # 累加符合条件的句子数量
                                    company_data[company_id][year]['sentences'].append(sentence)  # 存储符合条件的句子


# 输入社会责任报告和管理层报告文件夹路径
responsibility_reports_folder = r"C:\Users\gxy\Desktop\气候政策不确定性对于企业“漂绿”行为的影响\社会责任报告文本（2006-2023年）"  # 请根据实际路径修改
management_reports_folder = r"C:\Users\gxy\Desktop\气候政策不确定性对于企业“漂绿”行为的影响\内网_CMDA_管理层讨论与分析_ALL"  # 请根据实际路径修改

# 处理报告文件
process_responsibility_reports(responsibility_reports_folder)
process_management_reports(management_reports_folder)

# 输出每个公司编号和年份的符合条件句子数量和句子内容
with open('company_sentence_counts_and_sentences.txt', 'w', encoding='utf-8') as output_file:
    for company_id, years_data in company_data.items():
        for year, data in years_data.items():
            output_file.write(f"公司 {company_id} {year} 年的符合条件句子数量：{data['count']}\n")
            output_file.write("符合条件的句子：\n")
            for sentence in data['sentences']:
                output_file.write(f"{sentence}\n")  # 每个句子末尾已有 @
            output_file.write("\n")

print("句子统计完成，结果已保存到 'company_sentence_counts_and_sentences.txt'.")
