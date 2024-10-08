"""
创建基于 Flask 的简单 RESTful API 接口
时间：2024/8/8 下午7:08
"""
from flask import Flask, request, jsonify
import jieba


# 创建一个Flask应用实例
app = Flask(__name__)


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


def extract_most_important_keyword_and_location(text):
    """
    提取最关键疫情关键词和地名
    :param text: 字符串文本
    :return: 关键词字典
    """
    # 使用 jieba.cut 进行分词
    words = jieba.cut(text)
    filtered_words = filter_stopwords(words)

    keyword_scores = {}
    location_scores = {}

    for word in filtered_words:
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


# 加载停用词表
stopwords = read_stopwords('../dic/stopwords.txt')

# 加载自定义词典
jieba.load_userdict('../dic/custom_dict.txt')

# 读取关键词文件
epidemic_keywords = read_keywords_from_file('../dic/epidemic_keywords.txt')
zhengzhou_locations = read_keywords_from_file('../dic/zhengzhou_locations.txt')

# 定义了一个路由，指向应用程序的根 URL
@app.route('/analyze_text', methods=['POST'])
def analyze_text():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Missing required field 'text'"}), 400

    text = data['text']
    result = extract_most_important_keyword_and_location(text)

    response = {
        "keyword": result['most_important_keyword'],
        "address": result['most_important_location']
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=40006)     # 端口号设置为40000左右
