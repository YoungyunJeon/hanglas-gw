import pymysql
from sshtunnel import SSHTunnelForwarder

# SSH address mapping setup (not actually connects)
tunnel = SSHTunnelForwarder(('13.209.161.206', 22),  # SSH hosting server
                            ssh_username="ubuntu",
                            ssh_pkey="./monitoring.pem",
                            remote_bind_address=(
                                'zabbix-auroradb-zbx5.cluster-cpcv3bnt6lot.ap-northeast-2.rds.amazonaws.com', 3306),
                            # addr which SSH server can access
                            local_bind_address=('127.0.0.1', 3305))  # mapping addr which python will access

# connect and map remote addr to local addr


dblist = []


def getTotalData(dsname,start_date,end_date):
    try:
        tunnel.start()
        # db 환경변수 -> db 연동 객체
        conn = pymysql.connect(host=tunnel.local_bind_host,
                               port=tunnel.local_bind_port,
                               user='zabbix',
                               passwd='0(zabbix)',
                               db='zabbix')

        # sql 실행 객체
        cursor = conn.cursor()
        print("db 연동 성공!")

        sql = '''
             select
               hs.hostid,
               it.itemid,
               ds.name,
               hs.name,
               gp.name as gp_name,
               it.name as it_name,
               min(ifnull(tr.value_min, tu.value_min)) as value_min,
               max(ifnull(tr.value_max, tu.value_max)) as value_max,
               avg(ifnull(tr.value_avg, tu.value_avg)) as value_avg
            from dashboard ds
                join widget wg on ds.dashboardid = wg.dashboardid
                join widget_field wf on wg.widgetid = wf.widgetid
                join graphs gp on wf.value_graphid = gp.graphid
                join graphs_items gi on gp.graphid = gi.graphid
                join items it on gi.itemid = it.itemid
                join hosts hs on hs.hostid = it.hostid and not it.name ='CPU $2 time'
                
                left join trends tr on it.itemid = tr.itemid and tr.clock between UNIX_TIMESTAMP(%(start_date)s) and UNIX_TIMESTAMP(%(end_date)s)
                left join trends_uint tu on it.itemid = tu.itemid and tu.clock between UNIX_TIMESTAMP(%(start_date)s) and UNIX_TIMESTAMP(%(end_date)s)
            where ds.name = %(dsname)s
            group by hs.hostid, it.itemid
            order by wg.y, wg.x ;


            '''
        params = {
            'dsname': dsname,
            'start_date': start_date,
            'end_date': end_date
        }

        cursor.execute(sql, params)

        tables = cursor.fetchall()

        if tables:
            print('table 있음')
        else:
            print('table 없음')


    except Exception as e:
        print('db 연동 error :', e)
    finally:
        cursor.close()
        conn.close()
        tunnel.close()
        print("연결 종료")

    return tables

#
# dsname = "#019 HANGLAS_CPU, Memory_1"
# start_date = '2021-02-01 00:00:00'
# end_date = '2021-03-01 00:00:00'
# datatest = hgMaxtimeInfo(dsname,start_date,end_date)
# print(datatest)



