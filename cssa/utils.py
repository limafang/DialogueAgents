import re
import json


def get_text_inside_tag(html_string: str, tag: str):
    pattern = f"<{tag}>(.*?)<\/{tag}>"
    try:
        result = re.findall(pattern, html_string, re.DOTALL)
        return result
    except SyntaxError as e:
        raise ("Json Decode Error: {error}".format(error=e))


def read_json_file(file_path):
    """
    读取指定路径的JSON文件，并返回其内容。
    :param file_path: 要读取的JSON文件的路径。
    :return: 解析JSON文件内容后的Python对象。
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"文件未找到: {file_path}")
    except json.JSONDecodeError:
        print(f"JSON文件解析错误: {file_path}")
    except Exception as e:
        print(f"读取文件时出现错误: {e}")


def get_script(file_path):
    """
    读取指定路径的JSON文件，并返回其内容。
    :param file_path: 要读取的JSON文件的路径。
    :return: 返回两个三个列表[[]],[[]]。
    """
    data = read_json_file(file_path)
    text_batches = []
    speakers = []
    for i in data["scripts"]:
        text = []
        speaker = []
        for j in i["conversation"]:
            speaker.append(j["speaker"])
            text.append(j["text"])
        text_batches.append(text)
        speakers.append(speaker)
    return text_batches, speakers


def replace_(text):
    return re.sub(r"[?！]", ".", text)