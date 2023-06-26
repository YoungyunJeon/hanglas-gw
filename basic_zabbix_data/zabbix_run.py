import hg_zabbix_max.db_conn as dbcon
import hg_zabbix_max.data_func as new_zabbix_func
from openpyxl import Workbook
from datetime import datetime



LSA = [
    "LSA Korea", ["LSA KR_SEOUL_EC2_01","LSA KR_SEOUL_EC2_02"]
]

customersList = [
    "Samsung", ["samsung_temp"]]



start_date = '2022-02-01 00:00:00'
end_date = '2022-03-01 00:00:00'
max_value = 85
mem_max_value = 85
cpu_max_value = 85

fname = customersList[0]+"_cpu_mem_max_"+ datetime.now().strftime("%Y%m%d") + '_v1.xlsx'
wb = Workbook()
ws = wb.active


def zabbix_fun(dsname,start_date,end_date,max_value):
    dataList = dbcon.hgMaxDetailtimeInfo(dsname, start_date, end_date,max_value)

    return dataList



for dsname in customersList[1]:
    customer_zabbix_dataList =[]
    cpuList = []
    memList = []


    dataList = zabbix_fun(dsname,start_date,end_date,max_value)
    print(dataList)


    # cpu정보
    cpudata = new_zabbix_func.cupdata(dataList,cpu_max_value)
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
                print(eachdata)
                ws.append(eachdata)

    # for data_row in dataList:
    #     print(data_row)
    #     # for data in data_row:
    #     #     print(data)
    #         # ws.append(data)
    #     ws.append(data_row)



print("끝")
wb.save(fname)

