"""
jieba关键词识别
包含多个测试用例
时间：2024/8/8 下午2:02
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


# 加载停用词表
stopwords = read_stopwords('../dic/stopwords.txt')

# 加载自定义词典
jieba.load_userdict('../dic/custom_dict.txt')

# 从数据库中读取关键词和地点信息
epidemic_keywords = read_keywords_from_database('tb_epidemic_keywords')
zhengzhou_locations = read_keywords_from_database('tb_zhengzhou_location')

# # 示例文本列表
# texts = [
#     "今天早上我去了郑大一附院做核酸检测，人非常多，队伍排到了医院门口。",
#     "郑州东站最近加强了防疫措施，进出站都需要出示健康码。",
#     "昨天晚上，我在郑州市区散步的时候，看到很多地方都贴上了疫情防控的宣传海报。",
#     "我们公司的员工昨天接到了通知，由于疫情形势严峻，建议大家尽量减少外出。",
#     "郑州市教育局发布通知，所有学校要加强校园封闭管理，确保师生安全。",
#     "最近，金水区的一些小区开始实行严格的出入登记制度，外来人员不得进入。",
#     "为了配合疫情防控工作，郑州动物园宣布暂时闭园，恢复开放时间另行通知。",
#     "郑州市政府召开新闻发布会，通报了最新的疫情情况，并呼吁市民做好个人防护。",
#     "我的朋友住在二七区，他们那边已经开始了第二轮全员核酸检测。",
#     "今天我在中原万达广场购物时，工作人员提醒每位顾客要佩戴口罩并测量体温。",
#     "今天早上我去郑大一附院，发现健康码变成了红码。"
# ]
#
# for i, text in enumerate(texts, start=1):
#     # 提取最关键关键词和地名
#     result = extract_most_important_keyword_and_location(text)
#
#     print(f"示例 {i}:\n"
#           f"文本: '{text}'\n"
#           f"最关键疫情关键词: {result['most_important_keyword']}\n"
#           f"最关键地名关键词: {result['most_important_location']}\n")

# 单个测试用例
text = "今天早上我去郑大一附院，发现健康码变成了红码和绿码。"
result = extract_most_important_keyword_and_location(text, epidemic_keywords, zhengzhou_locations)

print(f"示例:\n"
      f"文本: '{text}'\n"
      f"最关键疫情关键词: {result['most_important_keyword']}\n"
      f"最关键地名关键词: {result['most_important_location']}\n")
