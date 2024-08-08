"""
输入内容
时间：2024/8/7 下午4:07
"""
import jieba
import jieba.posseg as pseg

# 加载自定义词典
# jieba.load_userdict('custom_dict.txt')

# 示例文本
text = "学习是一件很重要的事，我正在学习。，"

# 使用 jieba.cut 进行分词
words = pseg.cut(text)
for w, t in words:
    print(w, t)
# 打印分词结果
print(" ".join(words))

