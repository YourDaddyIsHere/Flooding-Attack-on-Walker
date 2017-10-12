import os
import sys
BASE = os.path.dirname(os.path.abspath(__file__))
if sys.platform == "darwin":
    # Workaround for annoying MacOS Sierra bug: https://bugs.python.org/issue27126
    # As fix, we are using pysqlite2 so we can supply our own version of sqlite3.
    import pysqlite2.dbapi2 as sqlite3
else:
    import sqlite3

import matplotlib.pyplot as plt

class usageplot(object):
    def __init__(self,database_name=os.path.join(BASE, 'Resource.db')):
        self.conn = sqlite3.connect(database_name)
        cursor = self.conn.cursor()
        query_script = "SELECT * from usage where insert_time >= ?"
        start_time = '2017-09-07 14:36:00'
        cursor.execute(query_script,(start_time,))
        self.conn.commit()
        results = cursor.fetchall()
        self.cpu_usage = []
        self.memory_usage = []
        self.network_sent = []
        self.network_received = []
        for result in results:
            self.cpu_usage.append(result[0])
            print(result[0],result[1],result[2],result[3])
        plt.plot(self.cpu_usage)
        plt.show()


if __name__ == "__main__":
    u = usageplot()
