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



def hgMaxDetailtimeInfo(dsname, start_date, end_date,max_value):

    try:
        tunnel.start()
        # db 환경변수 -> db 연동 객체
        conn = pymysql.connect(host=tunnel.local_bind_host,
                           port=tunnel.local_bind_port,
                           user='zabbix',
                           passwd='0(zabbix)',
                           db='zabbix')


        # sql 실행 객체
        global cursor
        cursor = conn.cursor()

        sql = '''
        
            SELECT 
                t.dsname,
                t.hsname,
                t.it_name,
                h.value,
                FROM_UNIXTIME(h.clock)
            FROM (
                select
                   it.hostid as hostid,
                   it.itemid as itemid ,
                   ds.name as dsname,
                   hs.name as hsname,
                   it.name as it_name,
                   tr.value_max as value_max,
                   tr.clock as clock,
                   FROM_UNIXTIME(tr.clock) as time
                from dashboard ds
                    join widget wg on ds.dashboardid = wg.dashboard_pageid
                    join widget_field wf on wg.widgetid = wf.widgetid
                    join graphs gp on wf.value_graphid = gp.graphid
                    join graphs_items gi on gp.graphid = gi.graphid
                    join items it on gi.itemid = it.itemid
                    join hosts hs on hs.hostid = it.hostid and not it.name ='CPU $2 time'
                    left join trends tr on it.itemid = tr.itemid and tr.clock between UNIX_TIMESTAMP(%(start_date)s) and UNIX_TIMESTAMP(%(end_date)s) and tr.value_max > %(max_value)s
                where ds.name = %(dsname)s
            ) t
            inner join history h on h.itemid = t.itemid and h.clock BETWEEN t.clock AND t.clock + 3600 and h.value > %(max_value)s
            UNION ALL
            SELECT 
                t.dsname,
                t.hsname,
                t.it_name,
                h.value,
                FROM_UNIXTIME(h.clock)
            FROM (
                select
                   it.hostid as hostid,
                   it.itemid as itemid ,
                   ds.name as dsname,
                   hs.name as hsname,
                   it.name as it_name,
                   tu.value_max as value_max,
                   tu.clock as clock,
                   FROM_UNIXTIME(tu.clock) as time
                from dashboard ds
                    join widget wg on ds.dashboardid = wg.dashboard_pageid
                    join widget_field wf on wg.widgetid = wf.widgetid
                    join graphs gp on wf.value_graphid = gp.graphid
                    join graphs_items gi on gp.graphid = gi.graphid
                    join items it on gi.itemid = it.itemid
                    join hosts hs on hs.hostid = it.hostid and not it.name ='CPU $2 time'
                    left join trends_uint tu on it.itemid = tu.itemid and tu.clock between UNIX_TIMESTAMP(%(start_date)s) and UNIX_TIMESTAMP(%(end_date)s) and tu.value_max > %(max_value)s
                where ds.name = %(dsname)s
            ) t
            inner join history_uint h on h.itemid = t.itemid and h.clock BETWEEN t.clock AND t.clock + 3600 and h.value > %(max_value)s
            '''
        params = {
            'max_value': max_value,
            'dsname': dsname,
            'start_date': start_date,
            'end_date': end_date
        }

        cursor.execute(sql, params)

        tables = cursor.fetchall()

        cursor.close()
        conn.close()
        tunnel.close()


    except Exception as e:
        print('db 연동 error :', e)
        tables = []
    # finally:
    #     tables = []

        # pass


    return tables



def soulbrain(dsname, start_date, end_date,max_value):
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

        sql = '''           
            
            select t.dsname,t.hsname,t.it_name,t.value_max,t.time,tt.name,tt.value_avg
            from (
                select
                   it.hostid as hostid,
                   it.itemid as itemid ,
                   ds.name as dsname,
                   hs.name as hsname,
                   it.name as it_name,
                   tr.value_max as value_max,
                   tr.clock as clock,
                   FROM_UNIXTIME(tr.clock) as time
                from dashboard ds
                    join widget wg on ds.dashboardid = wg.dashboard_pageid
                    join widget_field wf on wg.widgetid = wf.widgetid
                    join graphs gp on wf.value_graphid = gp.graphid
                    join graphs_items gi on gp.graphid = gi.graphid
                    join items it on gi.itemid = it.itemid
                    join hosts hs on hs.hostid = it.hostid and not it.name ='CPU $2 time'
                    left join trends tr on it.itemid = tr.itemid and tr.clock between UNIX_TIMESTAMP(%(start_date)s) and UNIX_TIMESTAMP(%(end_date)s) and tr.value_max > %(max_value)s
                where ds.name = %(dsname)s and value_max > %(max_value)s
            )t
            inner join (
                select
               hs.hostid as hostid,
               it.name as name,
               tu.itemid as itemid,
               tu.value_avg as value_avg,
               FROM_UNIXTIME(tu.clock) as time
            from hosts hs
                left join items it on hs.hostid = it.hostid
                left join trends_uint tu on it.itemid = tu.itemid
            where it.key_ in ("net.if.in[Amazon Elastic Network Adapter]","net.if.out[Amazon Elastic Network Adapter]","net.if.in[eth0]","net.if.out[eth0]") 
            ) tt on t.hostid = tt.hostid and t.time = tt.time
            '''
        params = {
            'max_value': max_value,
            'dsname': dsname,
            'start_date': start_date,
            'end_date': end_date
        }

        cursor.execute(sql, params)

        tables = cursor.fetchall()


    except Exception as e:
        print('db 연동 error :', e)
    finally:
        cursor.close()
        conn.close()
        tunnel.close()

    return tables


def hgMaxtimeInfo(dsname, start_date, end_date):
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
            SELECT 
            *
            FROM (
                select
                   ds.name as dsname,
                   hs.name as hsname,
                   it.name as it_name,
                   ifnull(tr.value_max, tu.value_max) as value_max,
                   FROM_UNIXTIME(tr.clock) as time
                from dashboard ds
                    join widget wg on ds.dashboardid = wg.dashboard_pageid
                    join widget_field wf on wg.widgetid = wf.widgetid
                    join graphs gp on wf.value_graphid = gp.graphid
                    join graphs_items gi on gp.graphid = gi.graphid
                    join items it on gi.itemid = it.itemid
                    join hosts hs on hs.hostid = it.hostid and not it.name ='CPU $2 time'
                    left join trends tr on it.itemid = tr.itemid and tr.clock between UNIX_TIMESTAMP(%(start_date)s) and UNIX_TIMESTAMP(%(end_date)s)
                    left join trends_uint tu on it.itemid = tu.itemid and tu.clock between UNIX_TIMESTAMP(%(start_date)s) and UNIX_TIMESTAMP(%(end_date)s)
                where ds.name = %(dsname)s
            ) t
            where value_max >95
            order by time;
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
        print("연결 종료")
        tunnel.close()


    return tables


#
# dsname = "#019 HANGLAS_CPU, Memory_1"
# start_date = '2021-02-01 00:00:00'
# end_date = '2021-03-01 00:00:00'
# datatest = hgMaxtimeInfo(dsname,start_date,end_date)
# print(datatest)

