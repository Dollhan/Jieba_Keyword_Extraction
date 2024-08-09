"""
创建基于 Flask 的简单 RESTful API 接口
时间：2024/8/8 下午7:08
"""
from flask import Flask, request, jsonify
import jieba

app = Flask(__name__)

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
    app.run(debug=True)