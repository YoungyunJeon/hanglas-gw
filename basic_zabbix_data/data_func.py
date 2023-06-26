import db_conn as dbcon



# def cupdata(dataList):
#     cpuList = []
#     for data in dataList:
#         item_name = data[2]
#         if 'CPU' in item_name:
#             #print(data)
#             hs_name = data[0]
#             server_name = data[1]
#             it_name = data[2]
#             value_max = data[3]
#             time = data[4]
#
#             data_tuple = (
#                 hs_name,
#                 server_name,
#                 it_name,
#                 time,
#                 value_max
#             )
#             cpuList.append(data_tuple)
#     return cpuList


def cpudata(dataList,cpu_max_value):
    cpuList = []
    for data in dataList:
        item_name = data[2]
        if 'CPU' in item_name:
            #print(data)
            hs_name = data[0]
            server_name = data[1]
            it_name = data[2]
            value_max = data[3]
            time = data[4]

            if value_max >= cpu_max_value:
                data_tuple = (
                    hs_name,
                    server_name,
                    it_name,
                    time,
                    value_max
                )
                cpuList.append(data_tuple)
    return cpuList

def memdata(dataList, mem_max_value):
    memList = []
    for data in dataList:
        item_name = data[2]
        if 'Memory' in item_name:
            hs_name = data[0]
            server_name = data[1]
            it_name = data[2]
            value_max = data[3]
            time = data[4]

            if value_max >= mem_max_value:
                data_tuple = (
                    hs_name,
                    server_name,
                    it_name,
                    time,
                    value_max
                )
                memList.append(data_tuple)
    return memList

#