import xlwt
import xlrd
from xlutils.copy import copy

def write_excel(data):
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('sheet 1')
    for i in range(len(data)):
        for j in range(len(data[i])):
            sheet.write(i, j, data[i][j])
    wbk.save('data.xls')

def read_excel():
    data = []
    wb = xlrd.open_workbook('data.xls')
    sheet = wb.sheet_by_index(0)
    for i in range(sheet.nrows):
        data.append(sheet.row_values(i))
    return data

def add_excel(data):
    rb = xlrd.open_workbook('data.xls')
    wb = copy(rb)
    ws = wb.get_sheet(0)
    for i in range(len(data)):
        for j in range(len(data[i])):
            ws.write(i, j, data[i][j])
    wb.save('data.xls')

    