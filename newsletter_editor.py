#뉴스레터 생성시 작성해야 할 것
#몇월 몇주차 인지
month = '11'
week = '4'
#언제까지의 채용공고 기준인지
base_date = "23.11.19 까지의 채용공고 기준"
#신입,경력,인턴별로 새로운 채용공고가 몇개인지
new_newcomer_number = 13
new_career_number = 30
new_intern_number = 4

#구글시트에서 데이터 가져오기
import gspread

gc = gspread.service_account('architects-recruit-automation-dcd380c15faa.json')
sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1HsA4HH5KptEeEUz6MRTHxRMJcAEU7H9_0GO3gMXiEXE/edit?usp=sharing")
wks = sh.worksheet("figma 연동")

#신입 데이터
new_dt_1 = wks.col_values(2) #신입_채용 마감일
new_dt_2 = wks.col_values(3) #신입_사무소 명
new_dt_3 = wks.col_values(4) #신입_직원 수 
new_dt_4 = wks.col_values(5) #신입_위치
new_dt_5 = wks.col_values(6) #채용 링크
new_dt_6 = wks.col_values(7) #홈페이지

#경력 데이터
car_dt_1 = wks.col_values(9) #경력_채용 마감일
car_dt_2 = wks.col_values(10) #경력_사무소 명
car_dt_3 = wks.col_values(11) #경력_요구경력
car_dt_4 = wks.col_values(12) #경력_직원 수
car_dt_5 = wks.col_values(13) #경력_위치
car_dt_6 = wks.col_values(14) #채용 링크
car_dt_7 = wks.col_values(15) #홈페이지

#인턴 데이터
int_dt_1 = wks.col_values(17) #인턴_채용 마감일
int_dt_2 = wks.col_values(18) #인턴_사무소 명
int_dt_3 = wks.col_values(19) #인턴_직원 수
int_dt_4 = wks.col_values(20) #인턴_위치
int_dt_5 = wks.col_values(21) #채용 링크
int_dt_6 = wks.col_values(22) #홈페이지


from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

#폰트
pdfmetrics.registerFont(TTFont("나눔고딕a", "./../../fonts/NaverNanumSquareNeo/NanumSquareNeo/TTF/NanumSquareNeo-aLt.ttf"))
pdfmetrics.registerFont(TTFont("나눔고딕b", "./../../fonts/NaverNanumSquareNeo/NanumSquareNeo/TTF/NanumSquareNeo-bRg.ttf"))
pdfmetrics.registerFont(TTFont("나눔고딕c", "./../../fonts/NaverNanumSquareNeo/NanumSquareNeo/TTF/NanumSquareNeo-cBd.ttf"))
pdfmetrics.registerFont(TTFont("나눔고딕d", "./../../fonts/NaverNanumSquareNeo/NanumSquareNeo/TTF/NanumSquareNeo-dEb.ttf"))
pdfmetrics.registerFont(TTFont("나눔고딕e", "./../../fonts/NaverNanumSquareNeo/NanumSquareNeo/TTF/NanumSquareNeo-eHv.ttf"))

#캔버스 생성
pdf = canvas.Canvas("[" + month + "월 " + week + "주차] picky 건축.pdf")

#신입 채용정보 데이터 작성하기---------
pdf.drawImage("뉴스레터 이미지 폴더/건축_신입.png", 0, 0, width=595, height=841)

#00월 0주차 채용공고
pdf.setFont("나눔고딕d", 12)
pdf.setFillColor('#000000')
pdf.drawString(470, 790, month+"월 "+week+"주차 채용공고")

#00.00.00 까지의 채용공고 기준
pdf.setFont("나눔고딕c", 7)
pdf.setFillColor('#9BA2B3')
pdf.drawString(470, 780, base_date)

newcomer_number = len(new_dt_1) - 1 #채용공고 개수

for i in range(1,newcomer_number + 1):
    if i % 30 == 0:  # 30의 배수일 때만 y 값을 초기화하지 않고 그대로 유지
        y = 708 - (22 * 30)
    else:
        y = 708 - (22 * (i % 30))

    pdf.setFont("나눔고딕b", 9)
    pdf.setFillColor('#000000')
    pdf.drawString(32, y, new_dt_1[i])
    pdf.drawString(112, y, new_dt_2[i])
    pdf.drawString(312, y, new_dt_3[i])
    pdf.drawString(370, y, new_dt_4[i])

    pdf.setFont("나눔고딕e", 9)
    pdf.drawString(472, y, "click !")
    link_rect = pdf.linkURL(new_dt_5[i], (472, y, 500, y+9), relative=1)
    pdf.drawString(532, y, "click !")
    link_rect = pdf.linkURL(new_dt_6[i], (532, y, 560, y+9), relative=1)

    if i % 30 == 0:  # 30의 배수일 때 페이지 추가
        pdf.showPage()
        pdf.drawImage("뉴스레터 이미지 폴더/건축_신입.png", 0, 0, width=595, height=841)

        #00월 0주차 채용공고
        pdf.setFont("나눔고딕d", 12)
        pdf.setFillColor('#000000')
        pdf.drawString(470, 790, month+"월 "+week+"주차 채용공고")

        #00.00.00 까지의 채용공고 기준
        pdf.setFont("나눔고딕c", 7)
        pdf.setFillColor('#9BA2B3')
        pdf.drawString(470, 780, base_date)

pdf.showPage()

#경력 채용정보 데이터 작성하기----------------
pdf.drawImage("뉴스레터 이미지 폴더/건축_경력.png", 0, 0, width=595, height=841)

#00월 0주차 채용공고
pdf.setFont("나눔고딕d", 12)
pdf.setFillColor('#000000')
pdf.drawString(470, 790, month+"월 "+week+"주차 채용공고")

#00.00.00 까지의 채용공고 기준
pdf.setFont("나눔고딕c", 7)
pdf.setFillColor('#9BA2B3')
pdf.drawString(470, 780, base_date)

career_number = len(car_dt_1) - 1 #채용공고 개수

for i in range(1,career_number + 1):
    if i % 30 == 0:  # 30의 배수일 때만 y 값을 초기화하지 않고 그대로 유지
        y = 708 - (22 * 30)
    else:
        y = 708 - (22 * (i % 30))

    pdf.setFont("나눔고딕b", 9)
    pdf.setFillColor('#000000')
    pdf.drawString(32, y, car_dt_1[i])
    pdf.drawString(102, y, car_dt_2[i])
    pdf.drawString(292, y, car_dt_3[i])
    pdf.drawString(342, y, car_dt_4[i])
    pdf.drawString(380, y, car_dt_5[i])

    pdf.setFont("나눔고딕e", 9)
    pdf.drawString(472, y, "click !")
    link_rect = pdf.linkURL(car_dt_6[i], (472, y, 500, y+9), relative=1)
    pdf.drawString(532, y, "click !")
    link_rect = pdf.linkURL(car_dt_7[i], (532, y, 560, y+9), relative=1)

    if i % 30 == 0:  # 30의 배수일 때 페이지 추가
        pdf.showPage()
        pdf.drawImage("뉴스레터 이미지 폴더/건축_경력.png", 0, 0, width=595, height=841)

        #00월 0주차 채용공고
        pdf.setFont("나눔고딕d", 12)
        pdf.setFillColor('#000000')
        pdf.drawString(470, 790, month+"월 "+week+"주차 채용공고")

        #00.00.00 까지의 채용공고 기준
        pdf.setFont("나눔고딕c", 7)
        pdf.setFillColor('#9BA2B3')
        pdf.drawString(470, 780, base_date)

pdf.showPage()

#인턴 채용정보 데이터 작성하기----------------
pdf.drawImage("뉴스레터 이미지 폴더/건축_인턴.png", 0, 0, width=595, height=841)

#00월 0주차 채용공고
pdf.setFont("나눔고딕d", 12)
pdf.setFillColor('#000000')
pdf.drawString(470, 790, month+"월 "+week+"주차 채용공고")

#00.00.00 까지의 채용공고 기준
pdf.setFont("나눔고딕c", 7)
pdf.setFillColor('#9BA2B3')
pdf.drawString(470, 780, base_date)

intern_number = len(int_dt_1) - 1 #채용공고 개수

for i in range(1,intern_number + 1):
    if i % 30 == 0:  # 30의 배수일 때만 y 값을 초기화하지 않고 그대로 유지
        y = 708 - (22 * 30)
    else:
        y = 708 - (22 * (i % 30))

    pdf.setFont("나눔고딕b", 9)
    pdf.setFillColor('#000000')
    pdf.drawString(32, y, int_dt_1[i])
    pdf.drawString(112, y, int_dt_2[i])
    pdf.drawString(312, y, int_dt_3[i])
    pdf.drawString(370, y, int_dt_4[i])

    pdf.setFont("나눔고딕e", 9)
    pdf.drawString(472, y, "click !")
    link_rect = pdf.linkURL(int_dt_5[i], (472, y, 500, y+9), relative=1)
    pdf.drawString(532, y, "click !")
    link_rect = pdf.linkURL(int_dt_6[i], (532, y, 560, y+9), relative=1)

    if i % 30 == 0:  # 30의 배수일 때 페이지 추가
        pdf.showPage()
        pdf.drawImage("뉴스레터 이미지 폴더/건축_인턴.png", 0, 0, width=595, height=841)

        #00월 0주차 채용공고
        pdf.setFont("나눔고딕d", 12)
        pdf.setFillColor('#000000')
        pdf.drawString(470, 790, month+"월 "+week+"주차 채용공고")

        #00.00.00 까지의 채용공고 기준
        pdf.setFont("나눔고딕c", 7)
        pdf.setFillColor('#9BA2B3')
        pdf.drawString(470, 780, base_date)

pdf.save()