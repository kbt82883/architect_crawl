from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def draw_blue_circle(pdf_path):
    # PDF 생성
    c = canvas.Canvas(pdf_path, pagesize=letter)

    # 원의 중심 좌표와 반지름 설정
    x, y = 300, 300
    radius = 100

    # 파란색으로 설정
    color = (0.173, 0.043, 0.894)  # RGB 값 설정

    # 원의 내부를 설정한 색상으로 그리기
    c.setStrokeColor('#2C0AE4')
    c.setFillColor('#2C0AE4')

    # 원을 직접 계산하여 그리기
    c.circle(100, 100, 3, stroke=1, fill=1)

    # PDF 저장
    c.save()

if __name__ == "__main__":
    pdf_path = "blue_circle.pdf"
    draw_blue_circle(pdf_path)
    print(f"PDF 파일이 생성되었습니다: {pdf_path}")