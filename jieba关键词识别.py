"""
jieba关键词识别
时间：2024/8/8 下午2:02
"""
import jieba


def read_keywords_from_file(filename):
    """
    从文件中读取关键词和关键程度到字典中
    :param filename: .txt文件
    :return: 字典
    """
    keywords = {}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            keyword, score = line.strip().split()
            keywords[keyword] = int(score)
    return keywords


# 加载自定义词典
jieba.load_userdict('custom_dict.txt')

# 读取关键词文件
epidemic_keywords = read_keywords_from_file('epidemic_keywords.txt')
zhengzhou_locations = read_keywords_from_file('zhengzhou_locations.txt')


def extract_most_important_keyword_and_location(text):
    """
    提取最关键疫情关键词和地名
    :param text: 字符串文本
    :return: 关键词字典
    """
    # 使用 jieba.cut 进行分词
    words = jieba.cut(text)

    keyword_scores = {}
    location_scores = {}

    for word in words:
        # 检查是否是关键词
        if word in epidemic_keywords:
            keyword_scores[word] = (keyword_scores.get(word, 0)
                                    + epidemic_keywords[word])
        # 检查是否是地名
        elif word in zhengzhou_locations:
            location_scores[word] = (location_scores.get(word, 0)
                                     + zhengzhou_locations[word])

    # 确定最关键关键词
    most_important_keyword = max(keyword_scores,
                                 key=keyword_scores.get,
                                 default=None)
    most_important_location = max(location_scores,
                                  key=location_scores.get,
                                  default=None)

    return {"most_important_keyword": most_important_keyword,
            "most_important_location": most_important_location}


# 示例文本列表
texts = [
    "今天早上我去了郑大一附院做核酸检测，人非常多，队伍排到了医院门口。",
    "郑州东站最近加强了防疫措施，进出站都需要出示健康码。",
    "昨天晚上，我在郑州市区散步的时候，看到很多地方都贴上了疫情防控的宣传海报。",
    "我们公司的员工昨天接到了通知，由于疫情形势严峻，建议大家尽量减少外出。",
    "郑州市教育局发布通知，所有学校要加强校园封闭管理，确保师生安全。",
    "最近，金水区的一些小区开始实行严格的出入登记制度，外来人员不得进入。",
    "为了配合疫情防控工作，郑州动物园宣布暂时闭园，恢复开放时间另行通知。",
    "郑州市政府召开新闻发布会，通报了最新的疫情情况，并呼吁市民做好个人防护。",
    "我的朋友住在二七区，他们那边已经开始了第二轮全员核酸检测。",
    "今天我在中原万达广场购物时，工作人员提醒每位顾客要佩戴口罩并测量体温。"
]

for i, text in enumerate(texts, start=1):
    # 提取最关键关键词和地名
    result = extract_most_important_keyword_and_location(text)

    print(f"示例 {i}:\n"
          f"文本: '{text}'\n"
          f"最关键疫情关键词: {result['most_important_keyword']}\n"
          f"最关键地名关键词: {result['most_important_location']}\n")
