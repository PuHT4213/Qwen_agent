from qwen_agent.agents.doc_qa import ParallelDocQA
from qwen_agent.agents import Assistant
import pprint
import time

llm={
    'model': 'qwen2.5:7b',
    'model_server': 'http://localhost:11434/v1',  # base_url，也称为 api_base
    'api_key': 'ollama',
    }


# Policy RAG: 
class PragAssistant():
    '''
    Pragmatic Assistant is a class that uses the Assistant class from qwen_agent.agents to create a chatbot.
    arg: 
        llm: dict, the configuration of the LLM model.

    method:
        run: run the chatbot with a list of messages.
        run_and_output: run the chatbot with a list of messages and return the last response.
        start: start the chatbot, the user can input the query and the chatbot will response.
    
    '''
    def __init__(self, llm=llm):
        self.system = '根据用户的要求，我会使用RAG模型检索并回答问题。'
        self.bot = ParallelDocQA(llm=llm, system_message=self.system)
        self.messages = []
        self.response = []


    def run(self, messages):
        return self.bot.run(messages)    

    def run_and_output(self, messages):
        response = []
        for response in self.run(messages=messages):
            pass
        return response    

    def start(self):
        messages = []
        while True:
            query = input('用户请求: ')
            if query == 'exit':
                break

            messages.append({'role': 'user', 'content': query})

            # this loop make sure that only last response is saved and printed
            response = []
            for response in self.run(messages=messages):
                pass
            messages.extend(response)
            
            output ="机器人回应：" +  response[0]['content']
            for i in output:
                print(i, end='', flush=True)
                time.sleep(0.02)
            print()
            
            # test
            # if True:
            #     print('response(type: value):', type(response), response)
            #     print('messages(type: value):', type(messages), messages)

            # output_example
            # response(type: value): <class 'list'> [{'role': 'assistant', 'content': 'Hello! How can I help you today?'}]
            # messages(type: value): <class 'list'> [{'role': 'user', 'content': 'hello?'}, {'role': 'assistant', 'content': 'Hello! How can I help you today?'}]

        



def main():
    bot = PragAssistant()
    bot.start()

if __name__ == '__main__':
    main()
    # test()