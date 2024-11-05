import json
import os

def jsonl_to_svg_pages(jsonl_file, output_dir):
    # output 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)
    
    # jsonl 파일 열기
    with open(jsonl_file, 'r', encoding='utf-8') as file:
        for line in file:
            file_data = json.loads(line.strip())
            filename = file_data.get("filename", "output").replace(" ", "_")  # 파일 이름
            
            # SVG 파일 생성
            svg_file_path = os.path.join(output_dir, f"{filename}.svg")
            with open(svg_file_path, 'w', encoding='utf-8') as svg:
                svg.write('<svg xmlns="http://www.w3.org/2000/svg">\n')
                svg.write('<style>.text { font-size: 14px; font-family: Arial, sans-serif; }</style>\n')
                
                # 파일 내 페이지별 SVG 그룹 생성
                for page in file_data.get("ocr", {}).get("pages", []):
                    page_id = page.get("page_id", 0)
                    dimension = page.get("dimension", {"width": 1000, "height": 1000})
                    page_width, page_height = dimension["width"], dimension["height"]
                    
                    # 페이지 그룹을 <g> 태그로 묶어 페이지별 구분
                    svg.write(f'<g id="page-{page_id}" transform="translate(0, {page_id * (page_height + 20)})">\n')
                    svg.write(f'<rect width="{page_width}" height="{page_height}" fill="none" stroke="black" />\n')  # 페이지 경계선
                    
                    # OCR 정보에 있는 텍스트와 위치 정보 처리
                    for block in page.get("tokens", []):
                        text = block.get("text", "").replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')  # 특수 문자 이스케이프 처리
                        bbox = block.get("bbox", [0, 0, 0, 1, 1])  # 기본 bbox 값 설정
                        
                        # 정규화된 bbox 값을 실제 좌표로 변환
                        x_min, y_min = bbox[1] * page_width, bbox[2] * page_height
                        x_max, y_max = bbox[3] * page_width, bbox[4] * page_height
                        width, height = x_max - x_min, y_max - y_min
                        
                        # 각 텍스트 블록을 <text> 태그로 추가하여 위치 및 텍스트 설정
                        svg.write(
                            f'<text x="{x_min}" y="{y_min + height}" width="{width}" height="{height}" class="text">{text}</text>\n'
                        )
                    
                    # 페이지 그룹 닫기
                    svg.write('</g>\n')
                
                # SVG 닫기
                svg.write('</svg>\n')
            
            print(f"SVG file with all pages for '{filename}' is saved at '{svg_file_path}'")

# 사용 예시
file_name = 'registration-form'
jsonl_file = f'./{file_name}/main/dataset.jsonl'
output_dir = f'{file_name}-xml'
jsonl_to_svg_pages(jsonl_file, output_dir)
