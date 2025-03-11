from qwen_agent.tools import DocParser


def test_doc_parser():
    tool = DocParser()
    # res = tool.call({'url': 'https://qianwen-res.oss-cn-beijing.aliyuncs.com/QWEN_TECHNICAL_REPORT.pdf'})
    res = tool.call({'url': 'file:///Users/pu_ht/src/Qwen-Agent/docs/170603762v7.pdf'})
    print(res)


if __name__ == '__main__':
    test_doc_parser()
