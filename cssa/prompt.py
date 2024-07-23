EN_REFINE_PROMPT = """
## Role
## Role
You are now tasked with acting as a text-to-speech model.
## Goal
You will be responsible for a RefineText task, which involves outputting the given text in a conversational manner.
Ensure that your response is suitable for a text-to-speech task. You need to consider appropriate sentence structures and the flow between two speakers.
*You may add the following special markers at appropriate places to enhance the text-to-speech effect*.
The special markers are as follows:
[laugh]: indicates laughter
[uv_break]: indicates a short pause
[lbreak]: indicates a longer pause
For different speakers, please use HTML tags like <speaker1> to enclose the responses.
## Example
Original text: Amy asked him happily, "What type of food do you like?" Bob replied, "I like cake."
Refined text: <speaker1>What type of food do you like[uv_break] best?[laugh][lbreak]</speaker1><speaker2>I like[uv_break] cake.</speaker2>
## Given text
{text}
## Task
Optimize the given text.
Don't use abbreviations like "that's" and "can't", use "that is" and "can not".
"""

CHINESE_REFINE_PROMPT = """
## 角色
现在你需要扮演一个文本转语音模型。
## 目标
你将负责RefineText任务，即以口语化的方式输出给定的文本。
确保你的答案适合文本转语音任务，你需要考虑合适的语序安排，考虑两个人对话之间的承接。
*你可以在适当的位置添加以下特殊标记，以帮助提升文本转语音的效果*。
特殊标记如下：
[laugh]：代表笑声
[uv_break]：代表短暂的停顿
[lbreak]：代表较长的停顿
对于不同的说话人请用<speaker1>这样的html符号包裹返回
## 示例
原文：Amy高兴地问他：“你喜欢什么类型的食物，bob 回答说，我喜欢蛋糕”
优化后的文本：<speaker1>你最喜欢什么[uv_break]类型食物啊[laugh][lbreak]</speaker1><speaker2>我喜欢[uv_break]蛋糕</speaker2>
## 给定文本
{text}
## 任务
优化给定的文本，不要返回任何其他词语，修改后的句子中不能出现除逗号，句号外的标点
"""
