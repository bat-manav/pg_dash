from logging import fatal
import re
import psycopg2
from rich.console import Console
from rich.table import Table
from rich import box
from rich.layout import Layout
from rich import print as rprint
from rich.panel import Panel
from datetime import datetime
import platform
import psutil
import time
from rich.live import Live
from rich.progress import track
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint
from time import sleep
from threading import Thread
import pyfiglet
import os
from contextlib import contextmanager
from rich.align import Align
import shutil
from connect import *
connection,cursor=connect1()


os.system('clear')
title = pyfiglet.figlet_format('PG-DASH V1', font="starwars" , justify="center",width=150)
rprint(f'[yellow]{title}[/yellow]')
title2 = pyfiglet.figlet_format('LOADING..... ',font="small" , justify="center", width=150)
rprint(f'[yellow]{title2}[/yellow]')
time.sleep(2)

def make_layout() -> Layout:
        """Define the layout."""
        layout = Layout(name="root")

        layout.split(
                Layout(name="header", size=3),
                Layout(name="main", ratio=1),
#               Layout(name="footer", size=1),
        )
        layout["main"].split_row(
                Layout(name="side", ratio=1, minimum_size=40),
                Layout(name="body", ratio=1, minimum_size=40),
        )
        layout["side"].split(Layout(name="box1"), Layout(name="box2"))
        layout["body"].split(Layout(name="box3"), Layout(name="box4"))
        layout["box3"].split(Layout(name="box3_U"), Layout(name="box3_D"))
        layout["box3_U"].split_row(Layout(name="box3_U_L"), Layout(name="box3_U_R"))

        layout["box3_D"].split_row(Layout(name="box3_D_L"), Layout(name="box3_D_R"))

#       layout["box3"].split_row(Layout(name="sub_box1"), Layout(name="sub_box2"))
        layout["box4"].split_row(Layout(name="sub_box3"), Layout(name="sub_box4",size=30))
        layout["sub_box3"].split(Layout(name="sub_box31",size=10), Layout(name="sub_box32"))
        layout["sub_box32"].split_row(Layout(name="sub_box32_L"), Layout(name="sub_box32_R"))

        layout["box3_U_L"].size=50
        layout["box3_D_L"].size=40
        layout["box2"].split(Layout(name="box2_U"), Layout(name="box2_D"))
        layout["box1"].size=15


#       layout["sub_box31"].size=


        return layout



layout = make_layout()


def monit_layout() -> Layout:
        """Define the layout."""
        layout1 = Layout(name="root")

        layout1.split(
                Layout(name="header", size=3),
                Layout(name="main", ratio=1),
#               Layout(name="footer", size=1),
        )
        layout1["main"].split_row(
                Layout(name="side", ratio=1, minimum_size=40),
                Layout(name="body", ratio=1, minimum_size=40),
        )
        layout1["side"].split(Layout(name="box1"), Layout(name="box2"))
        layout1["body"].split(Layout(name="box3"), Layout(name="box4"))
        return layout1

layout1 = monit_layout()

def maintenance_layout() -> Layout:
        """Define the layout."""
        layout2 = Layout(name="root")

        layout2.split(
                Layout(name="header", size=3),
                Layout(name="main", ratio=1),
#               Layout(name="footer", size=1),
        )
        layout2["main"].split_row(
                Layout(name="side", ratio=1, minimum_size=40),
                Layout(name="body", ratio=1, minimum_size=40),
        )
        layout2["side"].split(Layout(name="box1"), Layout(name="box2"))
        layout2["body"].split(Layout(name="box3"), Layout(name="box4"))
        return layout2

layout2 = monit_layout()

def process_data():
    time.sleep(0.02)
class Header:
        """Display header with clock."""

        def __rich__(self) -> Panel:
                grid = Table.grid(expand=True)
                grid.add_column(justify="center", ratio=1)
                grid.add_column(justify="right")
                grid.add_row(
                        "[b]POSTGRES INFORMATION TOOL V1[/b]",
                        datetime.now().ctime().replace(":", "[blink]:[/]"),
                )
                return Panel(grid, style="white on blue")

#connection = psycopg2.connect(user="enterprisedb",
#                                                                  password="edb#123",
#                                                                  host="54.91.137.21",
#                                                                  port="5432",
#                                                                  database="postgres")
#cursor = connection.cursor()

def db_detail_layout():
        table = Table(title="DB DETAILS",title_style='Green',box=box.ASCII)
        table.add_column("DB_NAME", style="cyan", no_wrap=True)
        table.add_column("DB_SIZE", style="bright_magenta")
        table.add_column("CONNECTION", style="magenta")
        db_details_Query = "select p.datname, pg_size_pretty(pg_database_size(p.datname)) as size, \
                p.numbackends::text as connections  from \
                pg_stat_database p, pg_database d where p.datid=d.oid and d.datistemplate = false order by p.datid;"
        cursor.execute(db_details_Query)
        mobile_records = cursor.fetchall()
        for row in mobile_records:
                table.add_row(*list(row))
        return table;
#def imp_file_layout():
#       table1 = Table(title="FILE LOCATIONS")
#       table1.add_column("FILE_NAME", style="cyan", no_wrap=True)
#       table1.add_column("LOCATION", style="magenta")
#       directory_detail_Query = "select name,setting from pg_settings where name in ('data_directory','config_file','hba_file');"
#       cursor.execute(directory_detail_Query)
#       directory_records = cursor.fetchall()
#       for row in directory_records:
#               table1.add_row(*list(row))
#       console=Console(markup=False)
#       with console.capture() as capture:
#               console.print(table1)
#       return capture.get()



def pg_Info_layout():
        pg_info_tbl = Table(title="POSTGRES INFORMATION",box=box.ASCII)
        pg_info_tbl.add_column("INFORMATION", style="cyan", no_wrap=True)
        pg_info_tbl.add_column("VALUE", style="bright_magenta")
        pg_database="SELECT current_database();"
        pg_version="SELEct  version();"
        pg_statup_time="SELEct  to_char(pg_postmaster_start_time(),'MON-DD-YYYY HH12: MIPM');"
        pg_config_reload="SELEct  to_char(pg_conf_load_time(),'MON-DD-YYYY HH12: MIPM');"
        pg_timezone="SELEct  current_setting('TIMEZONE');"
        pg_port="select setting from pg_settings where name='port';"
        directory_detail_Query = "select name,setting from pg_settings where name in ('data_directory','config_file');"
        cluster_state_query="select pg_is_in_recovery();"
        data_dir_query="select setting from pg_settings where name in ('data_directory');"
        cursor.execute(pg_database)
        pg_database = cursor.fetchall()
        cursor.execute(pg_version)
        pg_version = cursor.fetchall()
        cursor.execute(pg_statup_time)
        pg_statup_time = cursor.fetchall()
        cursor.execute(pg_config_reload)
        pg_config_reload = cursor.fetchall()
        cursor.execute(pg_timezone)
        pg_timezone = cursor.fetchall()
        cursor.execute(pg_port)
        pg_port=cursor.fetchall()
        cursor.execute(directory_detail_Query)
        directory_records = cursor.fetchall()
        cursor.execute(data_dir_query)
        data_dir_path=cursor.fetchall()
        data_dir_path=str(data_dir_path)
        for char in data_dir_path:
            if char in "[]()',":
                data_dir_path=data_dir_path.replace(char,'')

        cursor.execute(cluster_state_query)
        cluster_state = cursor.fetchall()
        if str(cluster_state)[2:7]=='False':
                cls_state='MASTER'
        else:
                cls_state='SLAVE'
        disk_stat = 'total=' + str(psutil.disk_usage(data_dir_path).total/1024/1024/1024)[0:1] + 'GB' + ',' + 'percentage_use=' + str(psutil.disk_usage(data_dir_path).percent) + '%'
        pg_info_tbl.add_row("CURRENT_DB",re.sub('[^A-Za-z0-9]+', '', str(pg_database)))
        pg_info_tbl.add_row("PG_VERSION",str(pg_version)[3:40])
        pg_info_tbl.add_row("PG_STARTUP_TIME",str(pg_statup_time)[3:32])
        pg_info_tbl.add_row("CONFIG_RELOAD",str(pg_config_reload)[3:32])
        pg_info_tbl.add_row("TIMEZONE",re.sub('[^A-Za-z0-9]+', '', str(pg_timezone)))
        pg_info_tbl.add_row("PORT",str(pg_port)[3:7])
        pg_info_tbl.add_row("PGDATA DISK INFO",disk_stat)
        for row in directory_records:
                pg_info_tbl.add_row(*list(row))
        pg_info_tbl.add_row("CLUSTER_STATE",cls_state)
        return pg_info_tbl;



def system_info_layout():
        system_tbl = Table(title="SYSTEM INFORMATION",box=box.ASCII)
        system_tbl.add_row("NODE_NAME",platform.node())
        system_tbl.add_row("OS",platform.platform()[0:10])
        system_tbl.add_row("CORES",str(psutil.cpu_count(logical=False)))
        system_tbl.add_row("TOTAL_MEMORY",str(round(psutil.virtual_memory().total/1000000000, 2)) +"GB")
        system_tbl.add_row("MEM_USAGE", str(psutil.virtual_memory().percent)+"%")
        return system_tbl;



def top_tables():
        top_table_tbl = Table(title="TOP 5 TABLES(SIZE)",box=box.ASCII)
        top_table_tbl.add_column("TABLE_NAME", style="bright_magenta")
        top_table_tbl.add_column("TOTAL", style="bright_magenta")
        top_table_tbl.add_column("FREE", style="bright_magenta")
        top_table_query = "select concat(schemaname,'.',relname),pg_size_pretty(pg_total_relation_size(relid)) as total_size , \
                pg_size_pretty(pg_total_relation_size(relid) - pg_relation_size(relid)) \
                as free_space \
                from pg_catalog.pg_statio_user_tables \
                order by pg_total_relation_size(relid) desc, \
                pg_relation_size(relid) desc \
                limit 5;"
        cursor.execute(top_table_query)
        top_table_records = cursor.fetchall()
        for row in top_table_records:
                top_table_tbl.add_row(*list(row))
        return top_table_tbl;


def ts_details():
        ts_tbl = Table(title="TABLESPACES",box=box.ASCII)
        ts_tbl.add_column("TABLESPACE", style="magenta")
        ts_tbl.add_column("PATH", style="magenta")
        ts_tbl.add_column("SIZE", style="magenta")
        ts_tbl_query = "SELECT spcname AS TABLESPACE, \
                 pg_catalog.pg_tablespace_location(oid) AS Location, \
                 pg_catalog.pg_size_pretty(pg_catalog.pg_tablespace_size(oid)) AS Size \
                 FROM pg_catalog.pg_tablespace \
                 ORDER BY 1;"
        cursor.execute(ts_tbl_query)
        ts_tbl_records = cursor.fetchall()
        for row in ts_tbl_records:
                ts_tbl.add_row(*list(row))
        return ts_tbl;

def superuser_list():
        superuser_tbl = Table(title="",box=box.ASCII)
        superuser_tbl.add_column("SUPERUSERS(MAX 5)", style="magenta")
        superuser_tbl_query = "select usename  from pg_user where usesuper='t';"
        cursor.execute(superuser_tbl_query)
        superuser_tbl_record = cursor.fetchall()
        for row in superuser_tbl_record:
                superuser_tbl.add_row(*list(row))
        return superuser_tbl;

def memoryparam_list():
        memoryparam_tbl = Table("PG MEMORY COMPONENT",box=box.ASCII)
        memoryparam_tbl.add_column("VALUE", style="magenta")
#        memoryparam_tbl_query = " select name,  trunc(to_number(setting)/1024 ) || ' MB' Value  from pg_settings \
#                where name in ('work_mem','shared_buffers','maintenance_work_mem','effective_cache_size');"
        memoryparam_tbl_query=" select name,cast(setting as integer)/1024 || ' MB' Value  from pg_settings where name in ('work_mem','shared_buffers','maintenance_work_mem','effective_cache_size');"

        cursor.execute(memoryparam_tbl_query)
        memoryparam_record = cursor.fetchall()
        for row in memoryparam_record:
                memoryparam_tbl.add_row(*list(row))
        return memoryparam_tbl;

def schema_list():
        schemalist_tbl = Table(title="TOP 5 SCHEMAS",box=box.ASCII)
        schemalist_tbl.add_column("NAME", style="magenta")
        schemalist_tbl.add_column("SIZE", style="magenta")

        schemalist_query = "select schemaname,\
                pg_size_pretty(sum(pg_relation_size(quote_ident(schemaname) || '.' || quote_ident(tablename)))::bigint) as schema_size \
                FROM pg_tables where schemaname not in ('sys','pg_catalog','information_schema') group by schemaname order by schema_size;"
        cursor.execute(schemalist_query)
        schemalist_record = cursor.fetchall()
        for row in schemalist_record:
                schemalist_tbl.add_row(*list(row))
        return schemalist_tbl;

def replication_list():
        replication_tbl = Table(title="REPLICATION DETAILS",box=box.ASCII)
        replication_tbl.add_column("ADDRESS", style="magenta")
        replication_tbl.add_column("STATE", style="magenta")
        replication_tbl.add_column("SYNC", style="magenta")
        replication_tbl.add_column("SLOT_NAME", style="magenta")
        replication_tbl.add_column("SEND_LAG", style="magenta")
        replication_tbl.add_column("TOTAL_LAG", style="magenta")

        replication_query = "SELECT r.client_addr AS client_addr,r.state, r.sync_state AS MODE, s.slot_name, \
         ((pg_wal_lsn_diff(pg_current_wal_lsn(), r.sent_lsn) / 1024)::int)::text AS send_lag, \
         ((pg_wal_lsn_diff(pg_current_wal_lsn(), r.replay_lsn))::int/1024)::text AS total_lag \
    FROM pg_stat_replication r LEFT JOIN pg_replication_slots s ON (r.pid = s.active_pid);"
        cursor.execute(replication_query)
        replication_record = cursor.fetchall()
        for row in replication_record:
                replication_tbl.add_row(*list(row))
        return replication_tbl;



def extension_list():
        extension_tbl = Table(title="",box=box.ASCII)
        extension_tbl.add_column("INSTALLED EXTENSIONS", style="cyan")

        extension_query = "select extname from pg_extension;"
        cursor.execute(extension_query)
        extension_record = cursor.fetchall()
        for row in extension_record:
                extension_tbl.add_row(*list(row))
        return extension_tbl;

def archive_stats():
        archive_tbl = Table(title="ARCHIVING DETAILS")
        archive_tbl.add_column("pg_walfile_name", style="magenta")
        archive_tbl.add_column("last_archived_wal", style="magenta")
        archive_tbl.add_column("last_archived_time", style="magenta")
#       archive_tbl.add_column("arc_diff", style="magenta")

        archive_query = "select  pg_walfile_name(pg_current_wal_lsn()), last_archived_wal, \
                TO_CHAR(last_archived_time, 'dd.mm.yyyy HH24:MI:SS') as last_archived_time \
      from pg_stat_archiver;"
        cursor.execute(archive_query)
        archive_record = cursor.fetchall()
        for row in archive_record:
                archive_tbl.add_row(*list(row))
        return archive_tbl;


def blocking_stats():
        blocking_tbl = Table(title="BLOCKING DETAILS",box=box.ASCII)
        blocking_tbl.add_column("blocked_id", style="magenta")
        blocking_tbl.add_column("usename", style="magenta")
        blocking_tbl.add_column("blocked_by(pid)", style="magenta")
        blocking_tbl.add_column("blocked_query", style="magenta")

        blocking_query = "select pid::text as blocked_pid, usename, pg_blocking_pids(pid)::text as blocked_by_pid,\
             query as blocked_query from pg_stat_activity where cardinality(pg_blocking_pids(pid)) > 0;"
        cursor.execute(blocking_query)
        block_record = cursor.fetchall()
        for row in block_record:
                blocking_tbl.add_row(*list(row))
        return blocking_tbl;


def locked_status():
        locked_tbl = Table(title="LOCKED OBJECTS",box=box.ASCII)
        locked_tbl.add_column("OBJ_NAME", style="magenta")
        locked_tbl.add_column("LOCK_TYPE", style="magenta")
        locked_tbl.add_column("PID", style="magenta")
        locked_tbl.add_column("MODE", style="magenta")
        blocking_query = "select t.relname,l.locktype,pid,mode from pg_locks l, pg_stat_all_tables t where l.relation=t.relid and t.relname not like 'pg_%' order by relation asc;"
        cursor.execute(blocking_query)
        locked_record = cursor.fetchall()
        for row in locked_record:
                locked_tbl.add_row(*list(row))
        return locked_tbl;


def waitevent_stats():
        waitevent_tbl = Table(title="WAITEVENTS",box=box.ASCII)
        waitevent_tbl.add_column("event_type", style="cyan")
        waitevent_tbl.add_column("wait_event", style="cyan")
        waitevent_tbl.add_column("connections", style="cyan")

        waitevent_query = "select wait_event_type, wait_event, count(*)::text as connections from pg_stat_activity where \
       wait_event_type is not null and wait_event_type <> 'Activity' group by wait_event_type, wait_event order by 3 desc;"
        cursor.execute(waitevent_query)
        waitevent_record = cursor.fetchall()
        for row in waitevent_record:
                waitevent_tbl.add_row(*list(row))
        return waitevent_tbl;


def index_stats():
        index_tbl = Table(title="INDEX CREATION",title_style='Green',box=box.ASCII)
        index_tbl.add_column("pid", style="cyan")
        index_tbl.add_column("query", style="cyan")
        index_tbl.add_column("phase", style="cyan")
        index_tbl.add_column("block_total", style="cyan")
        index_tbl.add_column("blocks_done", style="cyan")
        index_query = "SELECT a.pid::text,a.query,p.phase, p.blocks_total,p.blocks_done FROM pg_stat_progress_create_index p JOIN pg_stat_activity a ON p.pid = a.pid;"
        cursor.execute(index_query)
        index_record = cursor.fetchall()
        for row in index_record:
                index_tbl.add_row(*list(row))
        return index_tbl;

def long_query():
        long_query_tbl = Table(title="LONG QUERIES(> 5 SEC)",box=box.ASCII)
        long_query_tbl.add_column("pid", style="cyan")
        long_query_tbl.add_column("duration", style="cyan")
        long_query_tbl.add_column("state", style="cyan")
        long_query_tbl.add_column("query", style="cyan")
        long_query = "SELECT pid::text, (now() - pg_stat_activity.query_start)::text AS duration, \
            state, query FROM pg_stat_activity \
                WHERE state='active' and  query NOT like  '%pg_stat_activity%' AND (now() - pg_stat_activity.query_start) > interval '5 seconds' \
            ORDER BY duration desc;"
        cursor.execute(long_query)
        long_record = cursor.fetchall()
        for row in long_record:
                long_query_tbl.add_row(*list(row))
        return long_query_tbl;

#def efm_out():
#    with open(r"c:\users\ekrapat\pictures\test.log", 'r') as fp:
#        line_numbers = [1,2,3,4,5,6,7,17,18,19,20,21]
#        lines = []
#        for i, line in enumerate(fp):
#            if i in line_numbers:
#                lines.append(line.strip())
#    butfirst = lines[1:]
#    eachinaseparateline = "\n".join(butfirst)
#    return eachinaseparateline

def dead_tuple_stat():
        dead_tuple_tbl = Table(title="TABLES WITH DEAD TUPLE( TOP 5) ",title_style='Green',box=box.ASCII)
        dead_tuple_tbl.add_column("SCHEMA", style="cyan")
        dead_tuple_tbl.add_column("TABLE_NAME", style="cyan")
        dead_tuple_tbl.add_column("SIZE", style="cyan")
        dead_tuple_tbl.add_column("live_tuples", style="cyan")
        dead_tuple_tbl.add_column("DEAD_TUPLE", style="cyan")
        dead_tuple_tbl.add_column("RATIO", style="cyan")
        dead_tuple_query = "select schemaname, \
                relname, \
                    pg_size_pretty(pg_relation_size(schemaname|| '.' || relname)) as size, \
                n_live_tup::text, \
                n_dead_tup::text, \
                CASE WHEN n_live_tup > 0 THEN round((n_dead_tup::float / n_live_tup::float)::numeric, 4)::text END AS dead_tup_ratio \
                from pg_stat_user_tables \
                order by dead_tup_ratio desc NULLS LAST limit 5;"
        cursor.execute(dead_tuple_query)
        dead_record = cursor.fetchall()
        for row in dead_record:
                dead_tuple_tbl.add_row(*list(row))
        return dead_tuple_tbl;



def vacuum_ops_stats():
        vacuum_ops_tbl = Table(title="VACUUMING OPS PROGRESS ",title_style='Green',box=box.ASCII)
        vacuum_ops_tbl.add_column("PID", style="cyan")
        vacuum_ops_tbl.add_column("OBJECT_NAME", style="cyan")
        vacuum_ops_tbl.add_column("heap_blks_total", style="cyan")
        vacuum_ops_tbl.add_column("live_tuples", style="cyan")
        vacuum_ops_tbl.add_column("heap_blks_vacuumed", style="cyan")
        vacuum_ops_tbl.add_column("max_dead_tuples", style="cyan")
        vacuum_ops_query = "select pid,b.relname,a.phase,a.heap_blks_total,a.heap_blks_vacuumed,a.max_dead_tuples from  \
            pg_stat_progress_vacuum a , pg_stat_user_tables b where a.relid=b.relid;"
        cursor.execute(vacuum_ops_query)
        vacuum_record = cursor.fetchall()
        for row in vacuum_record:
                vacuum_ops_tbl.add_row(*list(row))
        return vacuum_ops_tbl;

#def efm_spool():
#os.system('systemctl status edb-efm*  > /tmp/test.log')
#word = 'ExecStart'
#with open(r'/tmp/test.log','r') as fp:
#     if 'active' in fp.read():
#         fp.seek(0)
#         lines=fp.readlines()
#         for line in lines:
#             if line.find(word) !=-1:
#                 x=line
#         myString=x
#         startString='/usr'
#         endString='/runefm.sh'
#         mySubString=myString[myString.find(startString)+len(startString):myString.find(endString)]
#         cmd='/usr'+mySubString+"/efm cluster-status efm  > /tmp/test1.log"
#         os.system(cmd)
# #        efm_out()

#def efm_out():
#    with open(r"/tmp/test1.log", 'r') as fp:
#        line_numbers = [1,2,3,4,5,6,7,18,19,20,21]
#        lines = []
#        for i, line in enumerate(fp):
#            if i in line_numbers:
#                lines.append(line.strip())
#    butFirst = lines[1:]
#    eachInASeparateLine = "\n".join(butFirst)
#    return eachInASeparateLine

os.system('clear')
title = pyfiglet.figlet_format('PG-DASH V1', font="starwars" , justify="center",width=150)
rprint(f'[yellow]{title}[/yellow]')
title2 = pyfiglet.figlet_format('LOADING...( 50 %) ',font="small" , justify="center", width=150)
rprint(f'[green_yellow]{title2}[/green_yellow]')
time.sleep(2)
layout["header"].update(Header())
layout["box1"].update(pg_Info_layout())
layout["box3_U_L"].update(ts_details())
layout["box3_U_R"].update(system_info_layout())
layout["box3_D_R"].update(memoryparam_list())
layout["box3_D_L"].update(db_detail_layout())
layout["sub_box31"].update(top_tables())
layout["sub_box32_L"].update(schema_list())
layout["sub_box32_R"].update(superuser_list())
layout["box2_U"].update(replication_list())
#layout["box2_D"].update(archive_info_box)
layout["box2_D"].update(archive_stats())
layout["sub_box4"].update(extension_list())
os.system('clear')
title = pyfiglet.figlet_format('PG-DASH V1', font="starwars" , justify="center",width=150)
rprint(f'[yellow]{title}[/yellow]')
title2 = pyfiglet.figlet_format('LOADING...( 75 %) ',font="small" , justify="center", width=150)
rprint(f'[yellow]{title2}[/yellow]')
time.sleep(2)
layout1["header"].update(Header())
layout1["box1"].update(blocking_stats())
layout1["box2"].update(waitevent_stats())
layout1["box3"].update(long_query())


layout2["header"].update(Header())
layout2["box1"].update(dead_tuple_stat())
layout2["box2"].update(vacuum_ops_stats())
layout2["box4"].update(index_stats())





def menu_choice():
    os.system('clear')
    title = pyfiglet.figlet_format('PG-DASH V1', font="starwars" , justify="center",width=150)
    rprint(f'[yellow]{title}[/yellow]')
    #console = Console()
    #console.print("ENTER YOUR CHOICE", style="green",justify="center")
    #console.print("1.POSTGRES INFORMATION DASHBOARD(PRESS 1)", style="green", justify="center")
    #console.print("2.POSTGRES MONITORING DASHBOARD (PRESS 2)", style="green", justify="center")
    TABLE_DATA = [
    [
        "1.",
        "STANDARD PG DASHBOARD",
        "PRESS 1",
    ],
    [
        "2.",
        "ADVANCE PG MONITOR",
        "PRESS 2",

    ],
    [
        "3.",
        "MAINTENANCE DASHBOARD",
        "PRESS 3",

    ],

]

    console = Console()

    BEAT_TIME = 0.001


    @contextmanager
    def beat(length: int = 1) -> None:
        yield
        time.sleep(length * BEAT_TIME)


    table = Table(show_footer=False)
    table_centered = Align.center(table)

    with Live(table_centered, console=console, screen=False, refresh_per_second=20):
        with beat(10):
            table.add_column("TASK NO.", no_wrap=True)

        with beat(10):
            table.add_column("TASK NAME", justify="right")

        with beat(10):
            table.add_column("TASK CODE" )

        with beat(10):
            table.title = "[b]ENTER YOUR CHOICE:[/b]"

        for row in TABLE_DATA:
            with beat(10):
                table.add_row(*row)

        table_width = console.measure(table).maximum

        with beat(10):
            table.columns[2].justify = "right"


        with beat(10):
            table.columns[0].style = "cyan"
            table.columns[1].header_style = "bold cyan"
            table.columns[2].header_style = "bold cyan"

            table.columns[0].header_style = "bold cyan"
            table.columns[1].style = "cyan"
            table.columns[2].style = "cyan"


        with beat(10):
            table.border_style = "yellow"





    choice=input("")
    if int(choice)==1:
        live_fun()
    elif int(choice)==2:
        monit_fun()
    elif int(choice)==3:
        maintenance_fun()
    else:
        print('invalid choice')


def live_fun():
    with Live(layout, refresh_per_second=0.1,screen=True,transient=True) as live:
           for _ in range(3):
                    time.sleep(2)
                    layout["header"].update(Header())
                    layout["box1"].update(pg_Info_layout())
                    layout["box3_U_L"].update(ts_details())
                    layout["box3_U_R"].update(system_info_layout())
                    layout["box3_D_R"].update(memoryparam_list())
                    layout["box3_D_L"].update(db_detail_layout())
                    layout["sub_box31"].update(ts_details())
                    layout["sub_box32_L"].update(schema_list())
                    layout["sub_box32_R"].update(superuser_list())
                    layout["box2_U"].update(replication_list())
#               layout["box2_D"].update(archive_info_box)
                    layout["box2_D"].update(archive_stats())
                    layout["sub_box4"].update(extension_list())
    menu_choice()

#        rprint(layout)


def monit_fun():
    with Live(layout1, refresh_per_second=0.1,screen=True,transient=True) as live:
           for _ in range(3):
                    time.sleep(2)
                    layout1["header"].update(Header())
                    layout1["box1"].update(blocking_stats())
                    layout1["box2"].update(waitevent_stats())
                    layout1["box3"].update(long_query())
                    layout1["box4"].update(index_stats())
#               layout["box2_D"].update(archive_info_box)
    menu_choice()

def maintenance_fun():
    with Live(layout2, refresh_per_second=0.1,screen=True,transient=True) as live:
           for _ in range(3):
                    time.sleep(2)
                    layout2["header"].update(Header())
                    layout2["box1"].update(dead_tuple_stat())
                    layout2["box2"].update(vacuum_ops_stats())
                    layout2["box3"].update(index_stats())



#               layout["box2_D"].update(archive_info_box)
    menu_choice()




#        rprint(layout)
os.system('clear')
title = pyfiglet.figlet_format('PGDASH V1', font="starwars" , justify="center",width=150)
rprint(f'[yellow]{title}[/yellow]')
title2 = pyfiglet.figlet_format('LOADED ',font="small" , justify="center", width=150)
rprint(f'[green]{title2}[/green]')

menu_choice()





#rprint(layout)

def process_data():
    time.sleep(0.02)




cursor.close()
connection.close()

