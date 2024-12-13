from PIL import Image
import pytesseract
import pandas as pd

# Tesseract 실행 파일 경로 설정 (Windows 사용자만 필요)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 이미지 경로 설정
image_path = "주문경고보류1.png"

# OCR로 텍스트 추출
text = pytesseract.image_to_string(Image.open(image_path), lang="kor")

# 텍스트를 라인 단위로 나누고 데이터프레임으로 변환
lines = [line.split() for line in text.split("\n") if line.strip()]
df = pd.DataFrame(lines)

# 엑셀로 저장
output_excel = "output.xlsx"
df.to_excel(output_excel, index=False, header=False)
print(f"엑셀 파일로 저장 완료: {output_excel}")
