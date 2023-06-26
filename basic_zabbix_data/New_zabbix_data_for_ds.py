import db_conn as dbcon
import dsNameList as clist
import new_zabbix_func as new_zabbix_func
from openpyxl import Workbook
from datetime import datetime

fname = "zabbix_rawdata_"+ datetime.now().strftime("%Y%m%d") + '_raw_data_12_cm_pyver.xlsx'
wb = Workbook()
ws = wb.active

customersList = clist.dsnameList
start_date = '2022-12-01 00:00:00'
end_date = '2023-01-01 00:00:00'

def zabbix_fun(dsname,start_date,end_date):
    dataList = dbcon.getTotalData(dsname, start_date, end_date)

    return dataList

for data in customersList:
    customer_zabbix_dataList =[]
    cpuList = []
    memList = []
    diskList = []
    # 고객사 이름
    cname = data[0]
    # ws.append(cname)

    for hsname in data[1]:
        dataList = zabbix_fun(hsname, start_date, end_date)
        # print(dataList)


        # cpu정보
        cpudata = new_zabbix_func.cupdata(dataList)
        cpuList.append(cpudata)

        # mem 정보
        memdata = new_zabbix_func.memdata(dataList)
        memList.append(memdata)

        # # Dsik 정보
        diskdata = new_zabbix_func.diskmix(dataList)
        diskList.append(diskdata)


    customer_zabbix_dataList.append(cpuList)
    # print(cpuList)
    customer_zabbix_dataList.append(memList)
    # print(memList)
    customer_zabbix_dataList.append(diskList)

    for data_row in customer_zabbix_dataList:
        list_row = list(data_row)
        for data in list_row:
            for eachdata in data:
                #print(eachdata)
                ws.append(eachdata)
print("끝")
wb.save(fname)














    # for data_row in zbxinfo:
    #     list_row = list(data_row)
    #     print(list_row)
    #     ws.append(list_row)


wb.save(fname)


