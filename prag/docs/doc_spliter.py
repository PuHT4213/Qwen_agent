import sys
import os
from doc_loader import DocLoader
import re

MAX_TOKENS = 3000

class DocSpliter:
    '''
    read files from input_dir using DocLoader which return a dict of dict, {'file_name':{'title': title, 'content': content},...}
    then
    split them into small files with MAX_TOKENS tokens.
    simple version only split by paragraph, which is defined by '\n\n'. Keep tring to \
        add more paragraph until the number of tokens exceed MAX_TOKENS, then split the file.
    advanced version will split by sentence, but it's not implemented yet.
    split files will be saved in output_dir, each with title as file name, and title pasted at the beginning of the file.

    if tokens exceed MAX_TOKENS, raise an error and do nothing.
    
    arg:
    input_dir: str, input directory
    output_dir: str, output directory

    method:
    simple_split: split by paragraph, then goto paragraph merge
    advanced_split: split by sentence, not implemented yet
    merge: merge paragraphs if the sum of tokens is less than MAX_TOKENS
    save: save paragraphs to output_dir

    '''
    default_input_dir = 'prag/docs/raw_data'
    default_output_dir = 'prag/docs/database'

    def __init__(self, input_dir=default_input_dir, output_dir=default_output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.doc_loader = DocLoader(input_dir)
        self.doc_dict = self.doc_loader.load_doc()
        self.doc_num = len(self.doc_dict)
        
    def simple_split(self):
        for file_name, doc in self.doc_dict.items():
            title = doc['title']
            paragraphs = doc['content'].split('\n\n')
            current_tokens = 0
            current_paragraphs = []
            part_num = 1

            for paragraph in paragraphs:
                tokens = len(paragraph)
                if current_tokens + tokens > MAX_TOKENS:
                    if current_tokens == 0:
                        raise ValueError(f"Paragraph in {file_name} exceeds MAX_TOKENS")
                    self.save(title, current_paragraphs, part_num)
                    part_num += 1
                    current_tokens = 0
                    current_paragraphs = []

                current_paragraphs.append(paragraph)
                current_tokens += tokens

            if current_paragraphs:
                self.save(title, current_paragraphs, part_num)

    def separator_split(self, separators: list):
        '''
        split by separators, e.g. ['一、', '二、', '三、', '四、', '五、', '六、', '七、', '八、', '九、', '十、',]
        no merge, just split
        '''
        for file_name, doc in self.doc_dict.items():
            title = doc['title']
            content = doc['content']
            regex_pattern = '|'.join(map(re.escape, separators))
            parts = re.split(regex_pattern, content)
            paragraphs = [part.strip() for part in parts if part.strip()]
            paragraphs = self.merge(paragraphs)
            for i, paragraph in enumerate(paragraphs):
                self.save(title, [paragraph], i+1)

    def merge(self, paragraphs):
        current_tokens = 0
        current_paragraphs = []
        merged_paragraphs = []
        for paragraph in paragraphs:
            tokens = len(paragraph)
            if current_tokens + tokens > MAX_TOKENS:
                merged_paragraphs.append('\n\n'.join(current_paragraphs))
                current_tokens = 0
                current_paragraphs = []
            current_paragraphs.append(paragraph)
            current_tokens += tokens
        if current_paragraphs:
            merged_paragraphs.append('\n\n'.join(current_paragraphs))
        return merged_paragraphs

    def save(self, file_name, paragraphs, part_num):
        output_file_name = f"{file_name}_part{part_num}.txt"
        output_path = os.path.join(self.output_dir, output_file_name)
        with open(output_path, 'w') as f:
            f.write(file_name + '\n')
            f.write(file_name + '\n\n')
            f.write('\n\n'.join(paragraphs))

if __name__ == '__main__':
    # clear output directory
    output_dir = 'prag/docs/database'
    for file in os.listdir(output_dir):
        os.remove(os.path.join(output_dir, file))
    doc_spliter = DocSpliter()
    # doc_spliter.simple_split()
    doc_spliter.separator_split(['一、', '二、', '三、', '四、', '五、', '六、', '七、', '八、', '九、', '十、','（一）', '（二）', '（三）', '（四）', '（五）', '（六）', '（七）', '（八）', '（九）', '（十）'])