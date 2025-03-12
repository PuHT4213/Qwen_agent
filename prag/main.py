from prag_assistant import PragAssistant
from docs.doc_loader import DocLoader
from BAAI.doc_retrieval import DocRetrieval

import time

# threshold for document retrieval
threshold = 0
doc_path = 'prag/docs/database'


def main():
    # load docs
    loader = DocLoader(doc_path=doc_path)
    docs = loader.load_doc()
    print(f"共加载了 {len(docs)} 个文档。")

    retrieval = DocRetrieval()
    assistant = PragAssistant()
    
    print("欢迎使用集成文档检索的聊天机器人，输入 'exit' 或 'quit' 退出。")
    first_run = True
    while True:  
        if first_run:
            query = "2021年的政府工作重点是什么？"
            print(f"实例输入: {query}")
            first_run = False
        else:
            query = input("用户: ")

        if query.strip().lower() in ['exit', 'quit']:
            print("退出程序，再见！")
            break
        
        print("正在检索相关文档，请稍等...")
        retrieved = retrieval.retrieve(query, docs)

        if retrieved and retrieved[0]['score'] > threshold:
            best_doc = retrieved[0]
            context_message = f"系统提示：相关文档【{best_doc.get('title', '')}】的内容如下：\n{best_doc.get('content', '')}"
            context_file = doc_path + '/' + best_doc.get('file_name', '')
            print(f"检索到相关文档【{best_doc.get('title', '')}】，相似度为 {best_doc['score']:.2f}。")
        else:
            context_message = "系统提示：未检索到与查询相关的文档。"
            context_file = None
            print("未检索到相关文档。")
        
        # 构造对话消息，将系统提示作为对话的第一条信息
        messages = [
            {'role': 'user', 'content': [
                {'text': query},
                {'file': context_file}
            ]}
        ]
        
        # 调用对话机器人获取回答
        response = assistant.run_and_output(messages)
        if response:
            # 输出回答时模拟打字效果
            output = "机器人回应：" + response[0]['content'] # + '\n' + context_message[:200] + "..."
            for ch in output:
                print(ch, end='', flush=True)
                time.sleep(0.02)
            print()
        else:
            print("机器人未返回有效回答。")
            
if __name__ == '__main__':
    main()