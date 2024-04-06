from PyPDF2 import PdfReader, PdfWriter
import re
import requests


mylist = []
def parse_directory(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

        pattern = re.compile(r'(\d+(\.\d+)*)\s+(.*?)\s+(\d+)')
        # pattern = re.compile(r'(\d+(\.\d+)*)\s+([^.]+)\s+(\d+)')
        matches = pattern.findall(content)

        for match in matches:
            section_number = match[0]
            section_title = match[2].rstrip('. ')
            page_number = int(match[3])
            mytup = (section_number,section_title,page_number)
            mylist.append(mytup)
            print(mytup)

def add_bookmarks(input_pdf, output_pdf, bookmarks):
    with open(input_pdf, 'rb') as file:
        pdf_reader = PdfReader(file)

        pdf_writer = PdfWriter()

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]

            pdf_writer.add_page(page)

        for chapter, title, page_num in bookmarks:
            bookmark_page_num = page_num - 1  # 由于页码是从1开始，而PyPDF2中是从0开始
            bookmark_page_num = bookmark_page_num+16
            title = chapter+" "+title
            bookmark = pdf_writer.add_outline_item(title, bookmark_page_num)

        with open(output_pdf, 'wb') as output_file:
            pdf_writer.write(output_file)


url = 'https://s3.cern.ch/inspire-prod-files-d/da9d786a06bf64d703e5c6665929ca01'
response = requests.get(url, stream=True)
input_pdf_path = "test.pdf"
with open(input_pdf_path, 'wb') as file:
    for chunk in response.iter_content(chunk_size=1024):
        file.write(chunk)
        
file_path = 'content.txt'
parse_directory(file_path)
output_pdf_path = 'output_with_bookmarks.pdf'

add_bookmarks(input_pdf_path, output_pdf_path, mylist)
