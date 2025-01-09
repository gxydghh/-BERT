from gensim.models import KeyedVectors

# 加载词向量模型（只加载一次）
model_path = 'C:\\DDDDDDDDD\\python课文件\\企业漂绿\\data\\tencent-ailab-embedding-zh-d100-v0.2.0\\tencent-ailab-embedding-zh-d100-v0.2.0.txt'
model = KeyedVectors.load_word2vec_format(model_path, binary=False, unicode_errors='ignore')

# 需要查询的种子词
words = [
    '环境', '环保',
    '绿色', '低碳',
]

# 存储所有相似词的列表
all_similar_words = []

# 查询每个词的相似词，并合并到 all_similar_words 中
for word in words:
    similar_words = model.most_similar(word, topn=80)  # 获取每个词的前 20 个相似词
    for similar_word, score in similar_words:
        all_similar_words.append((similar_word, score))

# 按相似度降序排序
all_similar_words.sort(key=lambda x: x[1], reverse=True)

# 输出所有 320 个相似词
print("前 320 个相似词：")
for i, (similar_word, score) in enumerate(all_similar_words[:320]):
    print(f"{similar_word}")
