import json
import os
from tqdm import tqdm
def jsonl_to_single_html(jsonl_file, output_dir):
    # output directory 생성
    os.makedirs(output_dir, exist_ok=True)
    
    # jsonl 파일 열기
    with open(jsonl_file, 'r', encoding='utf-8') as file:
        for idx, line in tqdm(enumerate(file)):
            file_data = json.loads(line.strip())
            filename = file_data.get("filename", "output")  # filename으로 파일 이름 설정
            
            # HTML 파일 경로 설정
            html_file = os.path.join(output_dir, f"{filename}.html")
            
            with open(html_file, 'w', encoding='utf-8') as html:
                # HTML 파일의 기본 구조 작성
                html.write('<!DOCTYPE html>\n<html lang="en">\n<head>\n')
                html.write('<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
                html.write(f'<title>{filename}</title>\n')
                
                # CSS 스타일을 HTML 내부에 포함
                html.write('<style>\n')
                html.write('body {\n  position: relative;\n  font-family: Arial, sans-serif;\n}\n')
                html.write('.page {\n  position: relative;\n  margin: 20px auto;\n  border: 1px solid #ddd;\n}\n')
                html.write('.text-block {\n  position: absolute;\n  font-size: 14px;\n  white-space: pre-wrap;\n}\n')
                html.write('</style>\n')
                
                html.write('</head>\n<body>\n')
                
                # 페이지별 처리
                for page in file_data.get("ocr", {}).get("pages", []):
                    page_id = page.get("page_id", 0)
                    dimension = page.get("dimension", {"width": 1000, "height": 1000})
                    page_width, page_height = dimension["width"], dimension["height"]
                    
                    # HTML에 페이지 섹션 추가
                    html.write(f'<div class="page" id="{filename}-page-{page_id}" style="width: {page_width}px; height: {page_height}px;">\n')
                    
                    # OCR 정보에 있는 텍스트와 위치 정보 처리
                    for i, block in enumerate(page.get("tokens", [])):
                        text = block.get("text", "").replace('\n', '<br>')  # 줄바꿈을 유지
                        bbox = block.get("bbox", [0, 0, 0, 1, 1])  # 기본 bbox 값 설정
                        
                        # 정규화된 bbox 값을 실제 좌표로 변환
                        x_min, y_min = bbox[1] * page_width, bbox[2] * page_height
                        x_max, y_max = bbox[3] * page_width, bbox[4] * page_height
                        width, height = x_max - x_min, y_max - y_min
                        
                        # 각 텍스트 블록의 스타일을 inline 스타일로 지정하여 위치 및 크기 설정
                        html.write(
                            f'<div class="text-block" style="top: {y_min}px; left: {x_min}px; width: {width}px; height: {height}px;">{text}</div>\n'
                        )
                    
                    # 페이지 섹션 닫기
                    html.write('</div>\n')
                
                # HTML 파일 닫기
                html.write('</body>\n</html>\n')
    print(f"HTML files with inline styles are saved in {output_dir}")

# 사용 예시
dataset_name = 'registration-form'
jsonl_file = f'./{dataset_name}/main/dataset.jsonl'
output_dir = f'{dataset_name}-html'
jsonl_to_single_html(jsonl_file, output_dir)
