"""
输入内容
时间：2024/8/7 下午4:07
"""
import jieba


def read_stopwords(filename):
    """
    从文件中读取停用词到集合中
    :param filename: .txt文件
    :return: 集合
    """
    stopwords = set()
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            stopwords.add(line.strip())
    return stopwords

# 加载停用词表
stopwords = read_stopwords('stopwords.txt')


def filter_stopwords(words):
    """
    过滤停用词
    :param words: 分词结果
    :return: 过滤后的分词结果
    """
    return [word for word in words if word not in stopwords]


# 示例文本
text = "今天早上我去了郑大一附院，发现健康码变成了红码。"
# 提取最关键关键词和地名
words = jieba.cut(text)
# 过滤停用词
stop_add_words = filter_stopwords(words)
# 打印过滤后的结果
for word in stop_add_words:
    print(word)
