import gspread
from pandas import DataFrame

json_file_path = "architects-recruit-automation-dcd380c15faa.json"
gc = gspread.service_account(json_file_path)
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1HsA4HH5KptEeEUz6MRTHxRMJcAEU7H9_0GO3gMXiEXE/edit?usp=sharing"
doc = gc.open_by_url(spreadsheet_url)

update_sheet = doc.worksheet("사무소 모음")
worksheet_11_1 = doc.worksheet("11월 1주차")

cpn_name = worksheet_11_1.col_values(5)
cpn_people = worksheet_11_1.col_values(6)
cpn_add = worksheet_11_1.col_values(7)
cpn_url = worksheet_11_1.col_values(9)
cpn_rep_name = worksheet_11_1.col_values(10)


#11월 2주차 부터 채용공고를 올리는 사무소마다 중복되지 않으면 추가하기

df = DataFrame({'사무소 명':cpn_name, '직원 수':cpn_people, '위치':cpn_add, '홈페이지':cpn_url, '대표이름':cpn_rep_name})
update_sheet.update([df.columns.values.tolist()] + df.values.tolist())