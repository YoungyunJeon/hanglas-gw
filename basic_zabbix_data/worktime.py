# import 경로 수정
import db_conn as dbcon
import data_func as new_zabbix_func
from openpyxl import Workbook
import calendar
from datetime import datetime


# 1번
customersList = [
    "KISCO",[ "#035 KISCO_DEV", "#035 KISCO_PRD_LNX","#035 KISCO_PRD_WIN"]
]

#2번
Lsa = [
    "LSA_Korea",["LSA Korea"]
]

#날짜, 맥스값 수정
start_date = '2023-01-01 00:00:00'
end_date = '2023-01-31 23:59:59'
max_value = 85
mem_max_value = 85
cpu_max_value = 95

days = ['월','화','수','목','금','토','일']

#1번인지 2번인지 수정
fname = customersList[0]+"_cpu_mem_max_worktime_"+ datetime.now().strftime("%Y%m%d") + '_v1.xlsx'



wb = Workbook()
ws = wb.active

def zabbix_fun(dsname,start_date,end_date,max_value):
    dataList = dbcon.hgMaxDetailtimeInfo(dsname, start_date, end_date,max_value)

    return dataList


# 1번인지 2번인지
for dsname in customersList[1]:
    customer_zabbix_dataList =[]
    cpuList = []
    memList = []


    dataList = zabbix_fun(dsname,start_date,end_date,max_value)
    print(dataList)
# ('#006-2 온다택시 (Monitoring_EBS)', 'onda-op-stat', 'FreeStorageSpace', 96.4085, datetime.datetime(2021, 4, 7, 2, 19, 6)),

    # cpu정보
    cpudata = new_zabbix_func.cpudata(dataList,cpu_max_value)
    cpuList.append(cpudata)

    # mem 정보
    memdata = new_zabbix_func.memdata(dataList,mem_max_value)
    memList.append(memdata)


    customer_zabbix_dataList.append(cpuList)
    customer_zabbix_dataList.append(memList)

    for data_row in customer_zabbix_dataList:
        list_row = list(data_row)
        for data in list_row:
            for eachdata in data:
                this_date = eachdata[3].weekday()
                # print(this_date)

                if this_date < 5 :
                    weekdays = days[this_date]
                    hs_name = eachdata[0]
                    server_name = eachdata[1]
                    it_name = eachdata[2]
                    value_max = eachdata[4]
                    time = eachdata[3]

                    data_tuple = (
                        hs_name,
                        server_name,
                        it_name,
                        time,
                        weekdays,
                        value_max
                    )

                    ws.append(data_tuple)




print("끝")
wb.save(fname)




