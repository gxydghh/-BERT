import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
import torch

# 设置设备（如果有GPU，则使用GPU）
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 加载数据集
data = pd.read_csv("dataset.csv")

# 数据清洗和预处理
data['sentence'] = data['sentence'].astype(str)  # 确保句子为字符串类型
data['label'] = data['label'].astype(int)       # 确保标签为整数类型

# 数据拆分为训练集和验证集
train_texts, val_texts, train_labels, val_labels = train_test_split(
    data['sentence'].tolist(),
    data['label'].tolist(),
    test_size=0.2,
    random_state=42
)

# 转换为HuggingFace Dataset格式
train_dataset = Dataset.from_dict({'text': train_texts, 'label': train_labels})
val_dataset = Dataset.from_dict({'text': val_texts, 'label': val_labels})

# 加载预训练模型和分词器
model_name = "hfl/chinese-roberta-wwm-ext"  # 中文RoBERTa模型
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2).to(device)

# 定义Tokenization函数
def tokenize_function(examples):
    return tokenizer(examples['text'], padding="max_length", truncation=True, max_length=512)

# 对数据集进行Tokenization
train_dataset = train_dataset.map(tokenize_function, batched=True)
val_dataset = val_dataset.map(tokenize_function, batched=True)

# 设置需要的列
train_dataset = train_dataset.remove_columns(["text"])  # 保留模型需要的列
val_dataset = val_dataset.remove_columns(["text"])
train_dataset.set_format("torch")
val_dataset.set_format("torch")

# 定义训练参数
training_args = TrainingArguments(
    output_dir="./results",             # 保存模型和结果的文件夹
    learning_rate=2e-5,                # 学习率
    per_device_train_batch_size=8,     # 每设备训练批次大小
    per_device_eval_batch_size=8,      # 每设备验证批次大小
    num_train_epochs=3,                # 总训练Epoch数
    weight_decay=0.01,                 # 权重衰减
    logging_dir="./logs",              # 日志保存位置
    logging_steps=10,                  # 日志打印频率
    save_total_limit=2,                # 最多保存模型的数量
    save_steps=500,                    # 每500步保存一次模型
    load_best_model_at_end=True,       # 训练结束后加载最优模型
    metric_for_best_model="accuracy",  # 选择最佳模型的评价指标
    evaluation_strategy="steps"        # 每步进行评估
)

# 定义评价指标
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = torch.argmax(torch.tensor(logits), axis=1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, predictions, average="binary")
    acc = accuracy_score(labels, predictions)
    return {"accuracy": acc, "f1": f1, "precision": precision, "recall": recall}

# 使用Trainer进行训练
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)

# 开始训练
trainer.train()

# 保存模型和分词器
model.save_pretrained("./fine_tuned_model")
tokenizer.save_pretrained("./fine_tuned_model")
