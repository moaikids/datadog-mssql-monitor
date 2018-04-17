import os
import glob
import argparse
import pyodbc
import yaml
import concurrent.futures
from datetime import datetime
from datadog import initialize
from datadog import api

def monitor(server):
    print("server : {0}".format(server))
    currentdir = os.path.dirname(os.path.abspath(__file__))
    mssql_type = os.environ.get('MSSQL_TYPE')
    driver = '{ODBC Driver 13 for SQL Server}'

    for monitor_conf in glob.glob(currentdir + "/conf.d/*.yaml"):
        print("  monitor it : {0}".format(monitor_conf))

        # configuration
        ## load env.yaml
        env = yaml.load(open(monitor_conf))

        ## db
        ### currently specific use of MSSQL
        svr = server + ".database.windows.net" if mssql_type == 'sqldatabase' else server
        user = os.environ.get('MSSQL_USER') + "@" + server if mssql_type == 'sqldatabase' else os.environ.get('MSSQL_USER')
        print("  user : {0}".format(user))
        conn = pyodbc.connect("DRIVER={0};SERVER={1};PORT={2};UID={3};PWD={4}".format(driver, svr, os.environ.get('MSSQL_PORT'), user, os.environ.get('MSSQL_PASSWORD')))

        ## datadog
        dd_tags = []
        for key in env['dd_tags'].keys():
            dd_tags.append(key + ":" + env['dd_tags'][key])

        # execution
        cursor = conn.cursor()
        cursor.execute(env['monitor_sql'])
        row = cursor.fetchone()
        if row and len(row) > env['monitor_value_position']:
            metric = row[env['monitor_value_position']]
        else:
            metric = -1

        metric_to_datadog(env['metrics_name'], metric, server, dd_tags)
        print("")
        conn.close()

def metric_to_datadog(metric_name, value, host, tags):
    print("    metric : {0}: {1}".format(metric_name, value)) 
    print("    tags : {0}".format(tags))
    api.Metric.send(metric=metric_name, points=value, host=host, tags=tags)

# datadog
dd_api_key = os.environ.get('DATADOG_API_KEY')
dd_app_key = os.environ.get('DATADOG_APP_KEY')
options = {
    'api_key':dd_api_key,
    'app_key':dd_app_key
}
initialize(**options)

# monitor
print("exec at {0}".format(datetime.now()))
print("")

mssql_servers = os.environ.get('MSSQL_SERVER')
executor = concurrent.futures.ThreadPoolExecutor(max_workers=8)
is_parallel = True if os.environ.get('RUNNING_MODE') == 'parallel' else False
for mssql_server in mssql_servers.split(','):
    if is_parallel:
        executor.submit(monitor,mssql_server)
    else:
        monitor(mssql_server)


