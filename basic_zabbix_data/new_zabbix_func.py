import db_conn as dbcon



def zabbix_fun(dsname,start_date,end_date):
    dataList = dbcon.getTotalData(dsname, start_date, end_date)

    return dataList

# class zabbix_dataList:
#
#
#
#     def __init__(self,dsname,start_date,end_date):
#         self.dataList = dbcon.getTotalData(dsname, start_date, end_date)
#
#
#
#     def cupdata(self, dsname, start_date, end_date):
#         dataList = self.dataList_this
#         cpuList = []
#         for data in dataList:
#             item_name = data[5]
#             if item_name == 'ZCPU used percent':
#                 cpuList.append(data)
#         print("----")
#         return cpuList

def diskmix(dataList):
    disktotal = []
    diskfree = []
    disknamef = []
    disknamet= []

    diskList = []

    for data in dataList:
        item_name = data[5].lower()
        # print(data)
        if 'free' in item_name:
            diskFree = data[8]
            tup = data[4]


            if data[8] != None:
                diskFree = data[8] / 1024 / 1024 / 1024


            data_tuple = (
                diskFree,
                tup
            )
            print(data_tuple)
            diskfree.append(diskFree)
            disknamef.append(data_tuple)

        if 'total' in item_name:
            diskTotal = data[8]
            hs_name = data[2]
            server_name = data[3]
            it_name = data[4]

            if data[8] != None:
                diskTotal = data[8] / 1024 / 1024 / 1024

            data_tuple = (
                hs_name,
                server_name,
                it_name,
                diskTotal
            )
            disktotal.append(diskTotal)
            disknamet.append(data_tuple)

    # for i in range(len(disktotal)):
    #     print(disknamet[i])
    #     print(disknamef[i])
    #     print("//////////////////////////////")

    diskList = [disknamet[i]+disknamef[i] for i in range(len(disktotal))]

    # print(diskList)



    return diskList


def cupdata(dataList):
    cpuList = []
    for data in dataList:
        item_name = data[5]
        if 'CPU' in item_name:
            #print(data)
            hs_name = data[2]
            server_name = data[3]
            it_name = data[4]
            value_avg = data[8]
            value_max = data[7]

            data_tuple = (
                hs_name,
                server_name,
                it_name,
                value_avg,
                value_max
            )
            cpuList.append(data_tuple)
            print(data_tuple)
    return cpuList

def memdata(dataList):
    memList = []
    for data in dataList:
        item_name = data[5]
        if 'Memory' in item_name:
            hs_name = data[2]
            server_name = data[3]
            it_name = data[4]
            value_avg = data[8]
            value_max = data[7]

            data_tuple = (
                hs_name,
                server_name,
                it_name,
                value_avg,
                value_max
            )
            memList.append(data_tuple)
    return memList




 # ##85 % 이상 정보
 #    zbxinfo.append("85%")
 #
 #    for maxdata in data[1]:
 #        eachdata = dbcon.getMaxCount(maxdata[1], date)
 #        print(eachdata)
 #        server_name = maxdata[0]
 #        item_count = eachdata[0][2]
 #
 #        maxdata_tuple = (
 #            server_name,
 #            item_count
 #
 #        )
 #        zbxinfo.append(maxdata_tuple)
 #
 #
 #    print(zbxinfo)

#
# start_date = '2020-11-15 00:00:00'
# end_date = '2020-12-14 00:00:00'
#
# dsname = "#013 TSK_01"
#
# test = zabbix_dataList()
# test.cupdata(dsname, start_date, end_date)
