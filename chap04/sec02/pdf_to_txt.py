import pymupdf
import os

# 내려 받은 pdf파일을 PyMuPDF를 사용해 열면 pyMuPDF는 페이지별로 내용을 읽음
pdf_file_path = "../data/미래 기후변화 및 복합영농 시나리오를 고려한 맞춤형 배수개선 기술 개발.pdf"
doc = pymupdf.open(pdf_file_path)

# 불필요한 부분을 없애기 위해 헤더와 푸터의 영역을 정의
header_hight = 60
footer_hight = 60

# doc 객체에서 각 페이지를 반복하여 텍스트를 추출하고, 이를 full_text라는 변수에 한 페이지씩 추가
full_text = ''
for page in doc:
    rect = page.rect # 페이지 크기 가져오기
    header = page.get_text(clip=(0, 0, rect.width, rect.height))
    footer = page.get_text(clip=(0, rect.height - footer_hight, rect.width, rect.height))
    text = page.get_text(clip=(0, header_hight, rect.width, rect.height - footer_hight))
    full_text += text + '\n--------------------------------------------------------------\n'

# pdf파일을 텍스트 파일로 저장하기 위해 원본 pdf파일의 이름을 추출
pdf_file_name = os.path.basename(pdf_file_path)
pdf_file_name = os.path.splitext(pdf_file_name)[0]

# output 폴더에 full_text 내용을 텍스트 파일 형식으로 저장
text_file_path = f'../output/{pdf_file_name}.txt'
with open(text_file_path, 'w', encoding='utf-8') as f:
    f.write(full_text)