# DialogueAgents: A Hybrid Agent-Based Speech Synthesis Framework for Multi-Party Dialogue

Our website is available at [https://icassp.vercel.app/](https://icassp.vercel.app/).

Check our dataset [here](https://drive.google.com/file/d/1iiJ6Nc7RTE2kFVZm_mK4-oBvglLeh7DG/view?usp=sharing).

## 🚀 Quickstart
### 1. Clone the Repository
```bash
git clone --recursive https://github.com/FunAudioLLM/DialogueAgents.git
cd DialogueAgents
```
### 2. Download TTS Model
Download the CosyVoice-300M TTS model from [ModelScope](https://www.modelscope.cn/studios/iic/CosyVoice-300M).

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Run the Demo
#### Baseline Mode
Generate dialogue using the baseline mode:

```bash
python demo.py --mode baseline \
    --model_path /path/to/your/tts/model \
    --output_dir test/ \
    --script_path /data/demo.json
```
#### Refine Mode
Before using `refine` and `reflection` mode, configure your OpenAI API key:

```bash
export OPENAI_API_KEY="your_openai_api_key"
export OPENAI_API_BASE_URL="your_openai_base_url"
```
Run the refine mode:

```bash
python demo.py --mode refine \
    --model_path /path/to/your/tts/model \
    --output_dir test/ \
    --script_path /data/demo.json
```
#### Reflection Mode
Use Reflection Mode for iterative, context-aware dialogue generation:

```bash
python demo.py --mode reflection \
    --model_path /path/to/your/tts/model \
    --output_dir reflect/ \
    --script_path /data/demo.json \
    --audio_model_path /path/to/your/audio/llm/path \
    --max_loop 1
```
## 🛠 Adding Custom Speakers and Scripts
### 1. Add Speaker Data
Define new speakers in DialogueAgents/data/speaker/speaker.json. Each speaker should have a unique configuration like this:

```json
{
    "李秀娟": {
        "label": "中文女",
        "description": "和蔼可亲的奶奶，喜欢给孩子们讲小时候的故事，说话缓慢，声音略沙哑。总是喜欢回忆过去的往事。张忠是她的儿子，李建国是她老伴儿",
        "wav": "data/audios/lixiujuan.wav"
    },
    "王娟": {
        "label": "中文女",
        "description": "青年女教师，性格稳重且温柔，说话很有条理性，给人一种很亲和的感觉。通常会很耐心地聆听别人的遭遇，并给出友好的建议。张志强是她的丈夫，李小雪是她的女儿，刘燕是她的好朋友",
        "wav": "data/audios/wangjuan.wav"
    }
}
```
### 2. Add Script Data
Create or update a dialogue script in DialogueAgents/data/script/demo.json. Ensure all speakers are registered in the speaker.json file. Example:

```json
{
    "scripts": [
        {
            "id": 421,
            "topic": "本地剧院新剧首演",
            "conversation": [
                {
                    "speaker": "李秀娟",
                    "text": "王娟，本周五我们本地剧院有一部新剧首演，是一部关于历史的剧目，你感兴趣一起去观看吗？"
                },
                {
                    "speaker": "王娟",
                    "text": "听起来不错，我很喜欢历史剧。它讲述什么时期的故事？"
                },
                {
                    "speaker": "李秀娟",
                    "text": "讲的是文艺复兴时期的故事，非常引人入胜。我相信你会喜欢的。"
                },
                {
                    "speaker": "王娟",
                    "text": "那太好了，我一直对那个时期很感兴趣。我们周五见！"
                }
            ]
        }
    ]
}
```