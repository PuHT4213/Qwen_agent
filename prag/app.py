from flask import Flask, render_template, request
from prag_assistant import PragAssistant
from docs.doc_loader import DocLoader
from BAAI.doc_retrieval import DocRetrieval
import time

app = Flask(__name__)

# 配置参数
doc_path = 'prag/docs/database'
threshold = 0

# 在启动时加载所有文档
loader = DocLoader(doc_path=doc_path)
docs = loader.load_doc()
print(f"共加载了 {len(docs)} 个文档。")

# 初始化检索器和对话机器人
retrieval = DocRetrieval()
assistant = PragAssistant()

@app.route('/', methods=['GET', 'POST'])
def index():
    response_text = None
    context_message = None
    query = ""

    # 第一次访问时可以默认展示一个示例查询
    if request.method == 'GET':
        query = "2021年的政府工作重点是什么？"
    elif request.method == 'POST':
        query = request.form.get('query', '').strip()

    if query:
        # 检索文档
        retrieved = retrieval.retrieve(query, docs)
        context_file = None
        if retrieved and retrieved[0]['score'] > threshold:
            best_doc = retrieved[0]
            context_message = f"系统提示：相关文档【{best_doc.get('title', '')}】的内容如下：\n{best_doc.get('content', '')}"
            context_file = doc_path + '/' + best_doc.get('file_name', '')
            print(f"检索到相关文档【{best_doc.get('title', '')}】，相似度为 {best_doc['score']:.2f}。")
        else:
            context_message = "系统提示：未检索到与查询相关的文档。"
            print("未检索到相关文档。")
        
        # 构造对话消息，注意这里保持与原代码中一致的消息格式
        messages = [
            {'role': 'user', 'content': [
                {'text': query},
                {'file': context_file}
            ]}
        ]
        
        # 调用机器人接口获取回答
        response = assistant.run_and_output(messages)
        if response:
            # 为了模拟打字效果，我们这里可以简单直接返回回答文本
            response_text = response[0]['content']
        else:
            response_text = "机器人未返回有效回答。"
        # 为方便展示，可延时模拟打字效果（此处仅影响服务器端日志输出）
        for ch in ("机器人回应：" + response_text):
            print(ch, end='', flush=True)
            time.sleep(0.02)
        print()

    return render_template('index.html', query=query, response_text=response_text, context_message=context_message)

if __name__ == '__main__':
    # 运行在本地的 localhost:5000
    app.run(debug=True)
