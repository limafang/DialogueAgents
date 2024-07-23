import dashscope
from dashscope import MultiModalConversation

dashscope.api_key = "sk-2250e5f690cd47afb415002c9164f0f9"


def call_with_local_file():
    local_file_path1 = (
        "/data/xli/speech-agent/CSSA/llm_refine_outputs/llm_refine_conversation.wav"
    )
    messages = [
        {"role": "system", "content": [{"text": "You are a helpful assistant."}]},
        {
            "role": "user",
            "content": [
                {"audio": local_file_path1},
                {
                    "text": "上面是一段人工合成的音频对话，请你总结一下这段音频有什么存在不足的地方，提出改进意见"
                },
            ],
        },
    ]
    response = MultiModalConversation.call(model="qwen-audio-turbo", messages=messages)
    print(response)


if __name__ == "__main__":
    call_with_local_file()
