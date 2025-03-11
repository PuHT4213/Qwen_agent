from qwen_agent.agents.doc_qa import ParallelDocQA
from qwen_agent.agents import Assistant
import pprint
import time

llm={
    'model': 'qwen2.5:0.5b',
    'model_server': 'http://localhost:11434/v1',  # base_url，也称为 api_base
    'api_key': 'ollama',
    }

# Policy RAG: 
class Prag():
    def __init__(self, llm=llm):
        self.bot = Assistant(llm=llm)
        self.messages = []
        self.response = []
    def run(self, messages):
        return self.bot.run(messages)        

def main():
    messages = []
    while True:
        bot = Prag()
        query = input('用户请求: ')
        # 将用户请求添加到聊天历史。
        messages.append({'role': 'user', 'content': query})
        response = []
        for response in bot.run(messages=messages):
            pass
        messages.extend(response)
        
        output ="机器人回应：" +  response[0]['content']
        for i in output:
            print(i, end='', flush=True)
            time.sleep(0.02)
        print()

if __name__ == '__main__':
    main()
    # test()