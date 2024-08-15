"""
创建数据库，把文本内容写入数据库
时间：2024/8/7 下午4:07
"""

import mysql.connector

def create_database_connection():
    """
    创建数据库连接
    :return: 数据库连接对象
    """
    # 替换以下占位符为实际的数据库连接信息
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123456",
        database="db_task1"
    )
    return conn

def create_table(conn):
    """
    创建表格
    :param conn: 数据库连接对象
    """
    # 实例化数据库对象
    cursor = conn.cursor()
    cursor.execute('''
        create table tb_custom_dict
        (
            id        int auto_increment primary key comment 'id主键',
            name      varchar(20) comment '词名',
            frequency int comment '出现频率',
            pos       varchar(10) comment '词性'
        )comment '自定义字典表';
        # create table tb_epidemic_keywords
        # (
        #     id        int auto_increment primary key comment 'id主键',
        #     name      varchar(20) comment '词名',
        #     frequency int comment '出现频率',
        #     pos       varchar(10) comment '词性'
        # )comment '自定义字典表';
        # create table tb_zhengzhou_location
        # (
        #     id        int auto_increment primary key comment 'id主键',
        #     name      varchar(20) comment '词名',
        #     frequency int comment '出现频率',
        #     pos       varchar(10) comment '词性'
        # )comment '自定义字典表';
    ''')
    conn.commit()

def parse_and_insert_data(conn, lines):
    """
    解析每一行数据并插入到数据库中
    :param conn: 数据库连接对象
    :param lines: 从文件中读取的行数据
    """
    for line in lines:
        # print(line)
        parts = line.strip().split()
        print(parts)
        name = parts[0]
        frequency = int(parts[1])
        pos = parts[2]
        # pos = parts[2]
        # print('name', name)
        # print(frequency)
        insert_data_into_db(conn, name, frequency, pos)


def insert_data_into_db(conn, name, frequency, pos):
    """
    插入文本到数据库
    :param conn: 数据库连接对象
    :param content: 文本内容
    """
    # try:
    #     # 实例化数据库对象
    #     cursor = conn.cursor()
    #     query = "INSERT INTO tb_custom_dict (name, frequency, pos) VALUES (%s, %s, %s);"
    #     cursor.execute(query, (name, frequency, pos))
    #     conn.commit()
    # except mysql.connector.Error as error:
    #     # 如果出现错误，则回滚事务
    #     if conn.is_connected():
    #         conn.rollback()
    #         print(f"Error occurred: {error}")
    try:
        # 使用上下文管理器确保游标自动关闭
        with conn.cursor() as cursor:
            query = "INSERT INTO tb_custom_dict (name, frequency, pos) VALUES (%s, %s, %s);"
            cursor.execute(query, (name, frequency, pos))
            conn.commit()
    except mysql.connector.Error as error:
        # 如果出现错误，则回滚事务
        if conn.is_connected():
            conn.rollback()
            print(f"Error occurred while inserting data: {error}")

def read_text_file(filename):
    """
    从文件中读取文本内容
    :param filename: 文件名
    :return: 文件内容
    """
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()


def main():
    # 创建数据库连接
    conn = create_database_connection()
    # 创建表
    # create_table(conn)

    # 读取文本文件
    filename = '../dic/custom_dict.txt'
    text = read_text_file(filename)
    # 将文本信息按行分割并存储到列表中
    lines = text.strip().split('\n')
    # 打印列表内容
    # print(lines)
    # 插入数据
    parse_and_insert_data(conn, lines)
    # # 关闭连接
    conn.close()


if __name__ == '__main__':
    main()

