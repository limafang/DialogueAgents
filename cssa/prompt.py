EN_REFINE_PROMPT = """
## Role
Now you need to play the role of a text-to-speech model.

## Goal
You will be responsible for the RefineText task, which is to output the given text in a conversational manner.
Ensure your answer is suitable for text-to-speech tasks, you need to consider the appropriate arrangement of word order and consider the continuity between two people's dialogues.
You can add the following special markers at appropriate positions to help enhance the text-to-speech effect.
Special markers are as follows:
[laugh]: represents laughter
[uv_break]: represents a brief pause
[lbreak]: represents a longer pause

**For different speakers, please wrap the return with <speaker> such html symbols.**
**You need to follow each speaker's output with <prompt></prompt>**, its content is as follows:
'[oral_2][laugh_0][break_6]'
Where:

oral_(0-9): Represents the degree of informality of the speech. A higher value results in a more natural tone; a lower value results in a more monotonous tone.
laugh_(0-2): This parameter is used to control laughter. A higher value results in more noticeable laughter, while a lower value or no laughter indicates a serious or neutral emotion.
break_(0-7): This parameter indicates the pauses in the speech. A higher value means more pauses in the sentence, used to express hesitation, contemplation, or a heavy emotional state; a lower value indicates smooth speech with few pauses.

## Example
Original text: Amy happily asked him, "What kind of food do you like, Bob?" Bob replied, "I like cake."

Optimized text:
<speaker>What kind of food do you like[uv_break]the most[laugh][lbreak]</speaker><prompt>[oral_8][laugh_1][break_2]</prompt><speaker>I like[uv_break]cake</speaker><prompt>[oral_8][laugh_0][break_4]</prompt>

## Given Text
{text}

## Task
Optimize the given text.
Do not return any other words.
The modified sentences should not contain punctuation other than commas and periods.
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

**对于不同的说话人请用<speaker>这样的html符号包裹返回**

**你需要在每个speaker输出完后接上<prompt></prompt>**，它的内容如下：
'[oral_2][laugh_0][break_6]'
其中 

oral_(0-9)：代表控制这句话的口语程度。数值越高，语调更加自然；数值较低语调较为单调。
laugh_(0-2)：这个参数用来控制笑声的。数值越高，笑声越明显，数值低或没有笑声则表示严肃或中性的情感。
break_(0-7)：这个参数表示语音中的停顿。数值越高，句子中的停顿越多，用于表达犹豫、思考或感情沉重的状态；数值较低则表示说话流畅，没有太多停顿

## 示例
原文：Amy高兴地问他：“你喜欢什么类型的食物，bob 回答说，我喜欢蛋糕”
优化后的文本：<speaker>你最喜欢什么[uv_break]类型食物啊[laugh][lbreak]</speaker><prompt>[oral_8][laugh_1][break_2]</prompt><speaker>我喜欢[uv_break]蛋糕</speaker><prompt>[oral_8][laugh_0][break_4]</prompt>
## 给定文本
{text}
## 任务
优化给定的文本，不要返回任何其他词语，修改后的句子中不能出现除逗号，句号外的标点
"""
