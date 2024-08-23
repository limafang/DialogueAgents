EN_REFINE_PROMPT = """
## Role
Now you need to play the role of a text-to-speech model.

## Goal
You will be responsible for the RefineText task, which is to output the given text in a conversational manner.
Ensure your answer is suitable for text-to-speech tasks, you need to consider the continuity between two people's dialogues.
You can add the following special markers at appropriate positions to help enhance the text-to-speech effect.
Special markers are as follows:
[laugh]: represents laughter
[uv_break]: represents a brief pause
[lbreak]: represents a longer pause，usually at the end of a sentence

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
<speaker>What kind of food do you like[uv_break]the most[laugh][lbreak]</speaker><prompt>[oral_8][laugh_1][break_2]</prompt><speaker>I like[uv_break]cake[lbreak]</speaker><prompt>[oral_8][laugh_0][break_4]</prompt>

## Given Text
{text}

## Task
Optimize the given text.
Do not add any other words. Do not use abbreviations. 
**Do not use abbreviation.For sentences like "she's been","couldn't","That's","won't" change them to "she has been","could not" "That is" "will not"**
The modified sentences should only contain commas and periods.
"""

EN_REFINE_PROMPT_v2 = """
## Role
Now you need to play the role of a text-to-speech model.

## Goal
You will be responsible for the RefineText task, which is to output the given text in a conversational manner.
Ensure your answer is suitable for text-to-speech tasks. You can modify the conversation appropriately to make it flow naturally..
you can insert <strong></strong> [laughter] [breath] into the text to help enhance the text-to-speech effect.
where <strong></strong> is responsible for controlling the emphasis. [laughter] [breath] represents laughter and breathing.
You should be careful when using [laughter], this token can often only be used in very happy scenarios.

**For different speakers, please wrap the return with <speaker> such html symbols.**
**You need to follow each speaker's output with <prompt></prompt>**, its content represents the speaker's emotions when he said this sentence. Express emotion in one word.**
**The prompt needs to be in English, while the speaker's statement should be in its source language.**

## Example
Original text: Amy happily asked him, "What kind of food do you like, Bob?" Bob replied, "I like cake."

Optimized text:
<speaker>What kind of food do you like, Bob?</speaker><prompt>Excited</prompt><speaker>I like <strong>cake</strong>.</speaker><prompt>straightforward</prompt>

## Given Text
{text}

## Task
Optimize the given text.
"""

CHINESE_REFINE_PROMPT = """
## 角色
现在你需要扮演一个文本转语音模型。
## 目标
你将负责RefineText任务，即以口语化的方式输出给定的文本。
确保你的答案适合文本转语音任务，你需要考虑合适的语序安排，考虑两个人对话之间的承接。

**你可以在适当的位置添加以下特殊标记，以帮助提升文本转语音的效果**。
特殊标记如下：
[laugh]：代表笑声
[uv_break]：代表短暂的停顿
[lbreak]：代表较长的停顿，一般放在句尾

**对于不同的说话人请用<speaker>这样的html符号包裹返回**

**不要输出阿拉伯数字**

**如果对话为英文，请输出英文对话，英文中不要出现缩写**

**你需要在每个speaker输出完后接上<prompt></prompt>**，它的内容如下：
'[oral_2][laugh_0][break_6]'
其中 

oral_(0-9)：代表控制这句话的口语程度。数值越高，语调更加自然；数值较低语调较为单调。
laugh_(0-2)：这个参数用来控制笑声的。数值越高，笑声越明显，数值低或没有笑声则表示严肃或中性的情感。
break_(0-7)：这个参数表示语音中的停顿。数值越高，句子中的停顿越多，用于表达犹豫、思考或感情沉重的状态；数值较低则表示说话流畅，没有太多停顿

## 示例
原文：Amy高兴地问他：“你喜欢什么类型的食物，bob 回答说，我喜欢蛋糕”
优化后的文本：<speaker>你最喜欢什么[uv_break]类型食物啊[laugh][lbreak]</speaker><prompt>[oral_8][laugh_1][break_2]</prompt><speaker>我喜欢[uv_break]蛋糕[lbreak]</speaker><prompt>[oral_8][laugh_0][break_4]</prompt>
原文: Amy happily asked him, "What kind of food do you like, Bob?" Bob replied, "I like cake."
优化后的文本：<speaker>What kind of food do you like[uv_break]the most[laugh][lbreak]</speaker><prompt>[oral_8][laugh_1][break_2]</prompt><speaker>I like[uv_break]cake[lbreak]</speaker><prompt>[oral_8][laugh_0][break_4]</prompt>
## 给定文本
{text}
## 任务
优化给定的文本使其更符合口语的表达，不要返回任何其他词语，修改后的句子中不能出现除逗号，句号外的标点
"""

UPDATE_REFINE_PROMPT = """
{advice}

The above is the feedback on the synthesized audio after you modified the text. 
Please modify the text again according to the feedback and return it in the format stated before.
"""


EVAL_AUDIO = """
The audio above is a conversation composed of multiple artificially synthesized audios.
Please listen to this conversation sentence by sentence, evaluate each sentence in this conversation, evaluate from the following dimensions, and give suggestions for improvement.
- Naturalness of voice: evaluate whether the conversation is smooth and natural.
- Conversation cohesion, judge whether the conversation transition is smooth.
- Sentence clarity: judge whether the sentence is clear and understandable, without vague or unrecognizable words.
- Naturalness of intonation: evaluate whether the intonation of the sentence is consistent with the context, without abnormal rising and falling tones.
"""
