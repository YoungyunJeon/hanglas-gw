import pymysql
from sshtunnel import SSHTunnelForwarder




# SSH address mapping setup (not actually connects)
tunnel = SSHTunnelForwarder(('13.209.161.206', 22),  # SSH hosting server
                            ssh_username="ubuntu",
                            ssh_pkey="./monitoring.pem",
                            remote_bind_address=('zabbix-auroradb-zbx5.cluster-cpcv3bnt6lot.ap-northeast-2.rds.amazonaws.com', 3306),  # addr which SSH server can access
                            local_bind_address=('127.0.0.1', 3305))  # mapping addr which python will access

# connect and map remote addr to local addr
tunnel.start()



dblist = []





def getTotalData(dsname,start_date,end_date):
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

    # connect MySQL like local
    conn = pymysql.connect(host=tunnel.local_bind_host,
                           port=tunnel.local_bind_port,
                           user='zabbix',
                           passwd='0(zabbix)',
                           db='zabbix')

    cur = conn.cursor()
    params = {
        'dsname': dsname,
        'start_date': start_date,
        'end_date': end_date
    }
    cur.execute(sql, params)
    results = cur.fetchall()
    dblist = results

    #print(results)

    # close connection
    cur.close()
    conn.close()
    return dblist
# date = "UNIX_TIMESTAMP() and UNIX_TIMESTAMP()"
dsname = "#013 TSK_01"
start_date = '2020-11-15 00:00:00'
end_date = '2020-12-14 00:00:00'
datatest = getTotalData(dsname,start_date,end_date)
#print(datatest)



def getCpuInfo(self, hostid,date):
    sql = '''
    select
       hs.name,
       it.name,
       value_min,
       value_avg,
       value_max
    from (
        select
           hs.hostid,
           it.itemid,
           min(ifnull(tr.value_min, tu.value_min)) as value_min,
           max(ifnull(tr.value_max, tu.value_max)) as value_max,
           avg(ifnull(tr.value_avg, tu.value_avg)) as value_avg
        from hosts hs
            left join items it on hs.hostid = it.hostid and it.name = "ZCPU used percent"
            left join trends tr on it.itemid = tr.itemid and tr.clock between ''' + date +'''
            left join trends_uint tu on it.itemid = tu.itemid and tu.clock between ''' + date +'''
        where hs.hostid =''' + hostid +''' 
        group by hs.hostid, it.itemid
    ) t
    left join hosts hs on t.hostid = hs.hostid
    left join items it on t.itemid = it.itemid
    where t.value_min is not null
    '''
    # connect MySQL like local
    conn = pymysql.connect(host=tunnel.local_bind_host,
                           port=tunnel.local_bind_port,
                           user='zabbix',
                           passwd='0(zabbix)',
                           db='zabbix')

    cur = conn.cursor()

    cur.execute(sql)
    results = cur.fetchall()
    dblist = results

    #print(results)

    # close connection
    cur.close()
    conn.close()
    return dblist


def getMemInfo(self, hostid,date):
    sql = '''
    select
       hs.name,
       it.name,
       value_min,
       value_avg,
       value_max
    from (
        select
           hs.hostid,
           it.itemid,
           min(ifnull(tr.value_min, tu.value_min)) as value_min,
           max(ifnull(tr.value_max, tu.value_max)) as value_max,
           avg(ifnull(tr.value_avg, tu.value_avg)) as value_avg
        from hosts hs
            left join items it on hs.hostid = it.hostid and it.name = "ZMemory used percent"
            left join trends tr on it.itemid = tr.itemid and tr.clock between ''' + date +'''
            left join trends_uint tu on it.itemid = tu.itemid and tu.clock between ''' + date +'''
        where hs.hostid =''' + hostid +''' 
        group by hs.hostid, it.itemid
    ) t
    left join hosts hs on t.hostid = hs.hostid
    left join items it on t.itemid = it.itemid
    where t.value_min is not null
    '''
    # connect MySQL like local
    conn = pymysql.connect(host=tunnel.local_bind_host,
                           port=tunnel.local_bind_port,
                           user='zabbix',
                           passwd='0(zabbix)',
                           db='zabbix')

    cur = conn.cursor()

    cur.execute(sql)
    results = cur.fetchall()
    dblist = results

    # close connection
    cur.close()
    conn.close()
    return dblist


def getDiskInfo(itemid):
    sql = '''
    select
       hs.name,
       it.name,
       tu.itemid,
       tu.value_avg
    from hosts hs
        left join items it on hs.hostid = it.hostid
        left join trends_uint tu on it.itemid = tu.itemid
    where tu.itemid = '''+ itemid +'''
    order by tu.clock desc limit 1
    '''
    # connect MySQL like local
    conn = pymysql.connect(host=tunnel.local_bind_host,
                           port=tunnel.local_bind_port,
                           user='zabbix',
                           passwd='0(zabbix)',
                           db='zabbix')

    cur = conn.cursor()

    cur.execute(sql)
    results = cur.fetchall()
    dblist = results

    # close connection
    cur.close()
    conn.close()
    return dblist


def getMaxInfo(hostid, date):
    sql = '''
    select
       hs.name,
       it.name,
       value_max,
       time
    from (
        select
           hs.hostid,
           it.itemid,     
           ifnull(tr.value_max, tu.value_max) as value_max,
           FROM_UNIXTIME(tr.clock) as time
        from hosts hs
            left join items it on hs.hostid = it.hostid and it.name in ("ZCPU used percent","ZMemory used percent")
            left join trends tr on it.itemid = tr.itemid and tr.clock between ''' + date +'''
            left join trends_uint tu on it.itemid = tu.itemid and tu.clock between ''' + date +'''
        where hs.hostid =''' + hostid +''' 
    ) t
    left join hosts hs on t.hostid = hs.hostid
    left join items it on t.itemid = it.itemid
    where value_max >95
    order by time
    '''
    # connect MySQL like local
    conn = pymysql.connect(host=tunnel.local_bind_host,
                           port=tunnel.local_bind_port,
                           user='zabbix',
                           passwd='0(zabbix)',
                           db='zabbix')

    cur = conn.cursor()

    cur.execute(sql)
    results = cur.fetchall()
    dblist = results

    # close connection
    cur.close()
    conn.close()
    return dblist

def getMaxCount(hostid, date):
    sql = '''
    select
       hs.name,
       it.name,
       count(value_max)
    from (
        select
           hs.hostid,
           it.itemid,     
           ifnull(tr.value_max, tu.value_max) as value_max
        from hosts hs
            left join items it on hs.hostid = it.hostid and it.name in ("ZCPU used percent","ZMemory used percent")
            left join trends tr on it.itemid = tr.itemid and tr.clock between ''' + date +'''
            left join trends_uint tu on it.itemid = tu.itemid and tu.clock between ''' + date +'''
        where hs.hostid =''' + hostid +''' 
        
    ) t
    left join hosts hs on t.hostid = hs.hostid
    left join items it on t.itemid = it.itemid
    where value_max >85
    
    '''
    # connect MySQL like local
    conn = pymysql.connect(host=tunnel.local_bind_host,
                           port=tunnel.local_bind_port,
                           user='zabbix',
                           passwd='0(zabbix)',
                           db='zabbix')

    cur = conn.cursor()

    cur.execute(sql)
    results = cur.fetchall()
    dblist = results

    # close connection
    cur.close()
    conn.close()
    return dblist

'''
try :
     # db 환경변수 -> db 연동 객체
     conn = pymysql.connect(**config)
     # **config : config에 들어있는 7개의 환경변수를 이용해서 DB를 연동한다는 의미

     # sql 실행 객체
     cursor = conn.cursor()
     print("db 연동 성공!")

     sql = "show tables"
     cursor.execute(sql)
     tables = cursor.fetchall()

     if tables :
          print('table 있음')
     else :
          print('table 없음')


except Exception as e :
     print('db 연동 error :', e)
finally :
     cursor.close()
     conn.close()
     
  '''
