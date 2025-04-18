import os
import sys
from docx import Document
from PyPDF2 import PdfFileReader
from bs4 import BeautifulSoup
import markdown

class DocLoader():
    '''
        This class is responsible for loading all documentation files and returning the content in a structured format.
        Available documentation formats are Word, TXT, HTML and markdown.
        doc_path: str
            The path to the documentation file. 
            default: prag/docs/raw_data

        methods:
            load_doc: dict
                Load documentation files from target path and return the content.
    '''
    def __init__(self, doc_path: str = 'prag/docs/raw_data'):
        self.doc_path = doc_path

    def load_doc(self) -> dict:
        '''
        Load documentation files from target path and return the content.
        '''
        doc_content = {}
        for root, dirs, files in os.walk(self.doc_path):
            for file in files:
                if file.endswith('.docx'):
                    doc_content[file] = self.load_docx(os.path.join(root, file))
                elif file.endswith('.txt'):
                    doc_content[file] = self.load_txt(os.path.join(root, file))
                elif file.endswith('.html'):
                    doc_content[file] = self.load_html(os.path.join(root, file))
                elif file.endswith('.md'):
                    doc_content[file] = self.load_md(os.path.join(root, file))
                elif file.endswith('.pdf'):
                    doc_content[file] = self.load_pdf(os.path.join(root, file))
        return doc_content

    def load_txt(self, file_path: str) -> str:
        '''
        Load txt file and return the content as dict, key is the first line of the file.
        '''
        file_content = ''
        file_title = ''
        with open(file_path, 'r',encoding='utf-8') as f:
            file_title = f.readline().strip()
            file_content = f.read()
        return dict(title=file_title, content=file_content)

    def load_docx(self, file_path: str) -> str:
        '''
        Load docx file and return the content.
        '''
        doc = Document(file_path)
        content = ''
        for para in doc.paragraphs:
            content += para.text + '\n'
        return content
    def load_html(self, file_path: str) -> str:
        '''
        Load html file and return the content.
        '''
        with open(file_path, 'r') as f:
            return f.read()

    def load_md(self, file_path: str) -> str:
        '''
        Load markdown file and return the content.
        '''
        with open(file_path, 'r') as f:
            return markdown.markdown(f.read())

    def load_pdf(self, file_path: str) -> str:
        '''
        Load pdf file and return the content.
        '''
        with open(file_path, 'rb') as f:
            pdf = PdfFileReader(f)
            content = ''
            for page_num in range(pdf.getNumPages()):
                page = pdf.getPage(page_num)
                content += page.extract_text()
            return content

if __name__ == '__main__':
    doc_loader = DocLoader()
    doc_content = doc_loader.load_doc()
    print(doc_content.keys())
