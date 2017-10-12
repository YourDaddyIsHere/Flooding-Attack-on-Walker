import os
import sys
BASE = os.path.dirname(os.path.abspath(__file__))
if sys.platform == "darwin":
    # Workaround for annoying MacOS Sierra bug: https://bugs.python.org/issue27126
    # As fix, we are using pysqlite2 so we can supply our own version of sqlite3.
    import pysqlite2.dbapi2 as sqlite3
else:
    import sqlite3

import psutil


class sysmonitor(object):
    def __init__(self,database_name=os.path.join(BASE, 'Resource.db')):
        self.conn = sqlite3.connect(database_name)
        cursor = self.conn.cursor()
        create_database_script = u"""
                               CREATE TABLE IF NOT EXISTS usage(
                               cpu       REAL,
                               memory      REAL,
                               network_sent     REAL,
                               network_received    REAL,
                               insert_time          TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
                               )

                               """
        cursor.execute(create_database_script)

    def start(self):
        while True:
            cpu_usage_all = psutil.cpu_percent(interval=1,percpu=True)
            cpu_usage = max(cpu_usage_all)
            print cpu_usage_all
            memory_attributes = psutil.virtual_memory()
            memory_usage = (memory_attributes.used+0.0)/memory_attributes.total
            #print memory_usage
            network_attributes = psutil.net_io_counters()
            network_sent = network_attributes.bytes_sent
            network_received = network_attributes.bytes_recv
            print(network_sent,network_received)

            insert_script = u"INSERT INTO usage (cpu,memory,network_sent,network_received) VALUES(?,?,?,?)"
            data = (cpu_usage,memory_usage,network_sent,network_received)
            cursor = self.conn.cursor()
            cursor.execute(insert_script,data)
            self.conn.commit()







if __name__ == "__main__":
    m = sysmonitor()
    m.start()