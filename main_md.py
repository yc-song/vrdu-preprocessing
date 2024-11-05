import json
import os

def jsonl_to_markdown(jsonl_file, output_dir):
    # output directory 생성
    os.makedirs(output_dir, exist_ok=True)
    
    # jsonl 파일 열기
    with open(jsonl_file, 'r', encoding='utf-8') as file:
        for idx, line in enumerate(file):
            if idx == 0:
                file_data = json.loads(line.strip())
                filename = file_data.get("filename", "output")  # filename으로 파일 이름 설정
                
                # Markdown 파일 경로 설정
                md_file = os.path.join(output_dir, f"{filename}.md")
                
                with open(md_file, 'w', encoding='utf-8') as md:
                    # 파일 제목 작성
                    md.write(f"# OCR Results for {filename}\n\n")
                    
                    # 페이지별 처리
                    for page in file_data.get("ocr", {}).get("pages", []):
                        page_id = page.get("page_id", 0)
                        dimension = page.get("dimension", {"width": 1000, "height": 1000})
                        page_width, page_height = dimension["width"], dimension["height"]
                        
                        # Markdown에 페이지 제목 추가
                        md.write(f"## Page {page_id + 1} (Dimensions: {page_width} x {page_height})\n\n")
                        
                        # OCR 정보에 있는 텍스트와 위치 정보 처리
                        for i, block in enumerate(page.get("blocks", [])):
                            text = block.get("text", "").replace('\n', '  \n')  # 줄바꿈을 Markdown에서 유지
                            bbox = block.get("bbox", [0, 0, 0, 1, 1])  # 기본 bbox 값 설정
                            
                            # 정규화된 bbox 값을 실제 좌표로 변환
                            x_min, y_min = int(bbox[1] * page_width), int(bbox[2] * page_height)
                            x_max, y_max = int(bbox[3] * page_width), int(bbox[4] * page_height)
                            width, height = x_max - x_min, y_max - y_min
                            
                            # 텍스트 블록을 Markdown의 리스트 형식으로 작성
                            md.write(f"- **Text Block {i + 1}**  \n")
                            md.write(f"  - **Text**: {text}  \n")
                            md.write(f"  - **Position**: Top-Left ({x_min}px, {y_min}px), Width: {width}px, Height: {height}px  \n\n")
                        
                        # 페이지 구분을 위한 빈 줄 추가
                        md.write("\n---\n\n")
    
    print(f"Markdown files are saved in {output_dir}")

# 사용 예시
dataset_name = 'registration-form'
jsonl_file = f'./{dataset_name}/main/dataset.jsonl'
output_dir = f'{dataset_name}-markdown'
jsonl_to_markdown(jsonl_file, output_dir)
