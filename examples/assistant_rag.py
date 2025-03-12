from qwen_agent.agents import Assistant
from qwen_agent.gui import WebUI

llm_cfg = {
    # 使用 DashScope 提供的模型服务：
    # 'model': 'qwen-max',
    # 'model_server': 'dashscope',
    # 'api_key': 'sk-f149f1eb1e224d9497a42ad9768fe7c7',
    # 如果这里没有设置 'api_key'，它将读取 `DASHSCOPE_API_KEY` 环境变量。

    # 使用与 OpenAI API 兼容的模型服务，例如 vLLM 或 Ollama：
    'model': 'qwen2.5:0.5b',
    'model_server': 'http://localhost:11434/v1',  # base_url，也称为 api_base
    'api_key': 'ollama',

    # （可选） LLM 的超参数：
    # 'generate_cfg': {
    #     'top_p': 0.8
    # }
}

def test():
    bot = Assistant(name='Assistant',llm=llm_cfg)
    messages = [{'role': 'user', 'content': [{'text': '请将文档中的内容复述一遍'}, {'file': 'examples/resource/2021_part1.txt'}]}]
    for rsp in bot.run(messages):
        pass
    print(rsp)

def test2():
    system = '根据用户的要求，我会使用RAG模型检索并回答问题。'
    bot = Assistant(name='Assistant',llm=llm_cfg, system_message=system,
                    files=['file:///Users/pu_ht/src/Qwen-Agent/examples/resource/doc.pdf'])
    messages = [{'role': 'user', 'content': '请介绍附件中的文章'}]
    for rsp in bot.run(messages):
        pass
    print(rsp)
    

def app_gui():
    # Define the agent
    bot = Assistant(llm = llm_cfg,
                    # llm={'model': 'qwen-plus-latest'},
                    name='Assistant',
                    description='使用RAG检索并回答，支持文件类型：PDF/Word/PPT/TXT/HTML。')
    chatbot_config = {
        'prompt.suggestions': [
            {
                'text': '介绍图一'
            },
            {
                'text': '第二章第一句话是什么？'
            },
        ]
    }
    WebUI(bot, chatbot_config=chatbot_config).run()


if __name__ == '__main__':
    test()
    # app_gui()
    # test2()
