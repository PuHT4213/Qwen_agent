from qwen_agent.agents.doc_qa import ParallelDocQA
from qwen_agent.gui import WebUI
lm_cfg = {
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
    bot = ParallelDocQA(llm=lm_cfg)
    messages = [
        {
            'role': 'user',
            'content': [
                {
                    'text': '介绍实验方法'
                },
                {
                    'file': 'examples/resource/2021.txt'
                },
            ]
        },
    ]
    for rsp in bot.run(messages):
        pass
    print('bot response:', rsp)


def app_gui():
    # Define the agent
    bot = ParallelDocQA(
        llm={
            'model': 'qwen2.5:0.5b',
            'model_server': 'http://localhost:11434/v1',  # base_url，也称为 api_base
            'api_key': 'ollama',
        },
        description='并行QA后用RAG召回内容并回答。支持文件类型：PDF/Word/PPT/TXT/HTML。使用与材料相同的语言提问会更好。',
    )

    chatbot_config = {'prompt.suggestions': [{'text': '介绍实验方法'}]}

    WebUI(bot, chatbot_config=chatbot_config).run()


if __name__ == '__main__':
     test()
    # app_gui()
