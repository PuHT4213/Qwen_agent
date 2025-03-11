import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key='sk-f149f1eb1e224d9497a42ad9768fe7c7',
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-vl-plus",  # 此处以qwen-vl-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=[{"role": "user",
               "content": [
                   {"type": "text", "text": "这是什么"},
                   {"type": "files", "files": "file:///Users/pu_ht/src/Qwen-Agent/docs/170603762v7.pdf"}
               ]
                }
            ]
    )
print(completion.model_dump_json())