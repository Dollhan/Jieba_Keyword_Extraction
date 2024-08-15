"""
接入数据库测试
时间：2024/8/15 上午9:23
"""
import jieba
import mysql.connector

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


def filter_stopwords(words):
    """
    过滤停用词
    :param words: 分词结果
    :return: 过滤后的分词结果
    """
    return [word for word in words if word not in stopwords]


def read_keywords_from_database(table_name):
    """
    从数据库中读取关键词和关键程度到字典中
    :param table_name: 数据库表名
    :return: 字典
    """
    # 连接数据库
    connection = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='123456',
        database='db_task1'
    )

    cursor = connection.cursor()

    # 查询关键词和得分
    query = f"SELECT name, importance FROM {table_name}"
    cursor.execute(query)

    keywords = {row[0]: row[1] for row in cursor.fetchall()}

    cursor.close()
    connection.close()

    return keywords


def extract_most_important_keyword_and_location(text, keywords, locations):
    """
    提取最关键疫情关键词和地名
    :param text: 字符串文本
    :param keywords: 关键词字典
    :param locations: 地点字典
    :return: 关键词字典
    """
    # 使用 jieba.cut 进行分词
    words = jieba.cut(text)
    filtered_words = filter_stopwords(words)

    keyword_scores = {}
    location_scores = {}

    for word in filtered_words:
        print(word)
        # 检查是否是关键词
        if word in keywords:
            keyword_scores[word] = (keyword_scores.get(word, 0) + keywords[word])
        # 检查是否是地名
        elif word in locations:
            location_scores[word] = (location_scores.get(word, 0) + locations[word])

    # 确定最关键关键词
    most_important_keyword = max(keyword_scores, key=keyword_scores.get, default=None)
    most_important_location = max(location_scores, key=location_scores.get, default=None)

    return {"most_important_keyword": most_important_keyword,
            "most_important_location": most_important_location}


def load_userdict_from_mysql():
    """
    从 MySQL 数据库加载词汇到 jieba 的用户词典中
    """
    # 连接 MySQL 数据库
    connection = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='123456',
        database='db_task1'
    )

    cursor = connection.cursor()

    # 查询词汇
    query = "SELECT name, frequency, pos FROM tb_custom_dict"
    cursor.execute(query)

    # 读取词汇
    words = cursor.fetchall()

    # 构建词汇字符串
    user_dict_content = '\n'.join([f'{name} {frequency} {pos}' for name, frequency, pos in words])

    with open('../dic/custom_dict.txt', 'w', encoding='utf-8') as file:
        file.write(user_dict_content)

    # 将词汇字符串加载到 jieba
    jieba.load_userdict('../dic/custom_dict.txt')

    cursor.close()
    connection.close()


# 加载停用词表
stopwords = read_stopwords('../dic/stopwords.txt')

# 从 MySQL 数据库加载词汇
load_userdict_from_mysql()

# 从数据库中读取关键词和地点信息
epidemic_keywords = read_keywords_from_database('tb_epidemic_keywords')
zhengzhou_locations = read_keywords_from_database('tb_zhengzhou_location')

# 单个测试用例
text = "今天早上我去郑大一附院，发现健康码变成了红码和绿码。"
result = extract_most_important_keyword_and_location(text, epidemic_keywords, zhengzhou_locations)

print(f"示例:\n"
      f"文本: '{text}'\n"
      f"最关键疫情关键词: {result['most_important_keyword']}\n"
      f"最关键地名关键词: {result['most_important_location']}\n")