import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from tqdm import tqdm

# 加载微调后的模型
model_path = "./fine_tuned_model"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path).to(device)


def predict_sentiment(sentence):
    """对句子进行情感分析，返回 1（正向）或 0（非正向）"""
    try:
        inputs = tokenizer(sentence, return_tensors="pt", truncation=True, max_length=511, padding="max_length").to(
            device)
        outputs = model(**inputs)
        predictions = torch.argmax(outputs.logits, dim=-1).item()
        return predictions
    except Exception as e:
        print(f"Error during sentiment prediction: {e}")
        return 0  # 默认返回非正向


def analyze_sentences(input_file, output_file):
    """处理输入文件，进行情感分析并保存结果"""
    results = []
    company_id, company_year = None, None
    total_sentences, positive_sentences = 0, 0

    try:
        with open(input_file, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Input file {input_file} not found!")
        return

    for line in tqdm(lines, desc="Processing lines"):
        line = line.strip()

        # 标题行处理（提取公司编号、年份、总句子数量）
        if line.startswith("公司") and "符合条件句子数量" in line:
            # 保存上一组数据
            if company_id is not None and company_year is not None:
                results.append(f"{company_id},{company_year},{total_sentences},{positive_sentences}")

            # 解析标题行
            parts = line.split(" ")
            try:
                company_id = parts[1]
                company_year = parts[2]
                total_sentences = int(parts[-1].split("：")[-1])
                positive_sentences = 0
            except Exception as e:
                print(f"Error parsing header line: {line} -> {e}")
            continue

        # 句子行处理（仅分析 @ 结尾的句子）
        if line.endswith("@"):
            sentence = line[:-1]  # 去掉 @
            sentiment = predict_sentiment(sentence)
            if sentiment == 1:
                positive_sentences += 1

    # 保存最后一组数据
    if company_id is not None and company_year is not None:
        results.append(f"{company_id},{company_year},{total_sentences},{positive_sentences}")

    # 写入结果文件
    if results:
        try:
            with open(output_file, "w", encoding="utf-8") as file:
                file.write("公司编号,年份,总句子数,正向句子数\n")
                file.write("\n".join(results))
            print(f"Analysis completed. Results saved to {output_file}")
        except Exception as e:
            print(f"Error writing results to file: {output_file} -> {e}")
    else:
        print("No valid data processed. Results file will be empty.")


# 输入和输出文件路径
input_file = "cleaned_company_sentences.txt"
output_file = "result.txt"

# 执行情感分析
analyze_sentences(input_file, output_file)
