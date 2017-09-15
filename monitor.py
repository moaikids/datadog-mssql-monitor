import os
import glob
import argparse
import pymssql
import yaml
from datetime import datetime
from datadog import initialize
from datadog import api

def monitor():
    currentdir = os.path.dirname(os.path.abspath(__file__))
    for monitor_conf in glob.glob(currentdir + "/conf.d/*.yaml"):
        print("  monitor it : {0}".format(monitor_conf))

        # configuration
        ## load env.yaml
        env = yaml.load(open(monitor_conf))

        ## db
        ### currently specific use of MSSQL
        conn = pymssql.connect(
                 server=os.environ['MSSQL_SERVER'],
                 port=os.environ['MSSQL_PORT'],
                 user=os.environ['MSSQL_USER'],
                 password=os.environ['MSSQL_PASSWORD'],
                 timeout=os.environ['MSSQL_TIMEOUT'],
                 login_timeout=os.environ['MSSQL_TIMEOUT'],
                 database=os.environ['MSSQL_DATABASE']
               )

        ## datadog
        dd_tags = []
        for key in env['dd_tags'].keys():
            dd_tags.append(key + ":" + env['dd_tags'][key])

        # execution
        cursor = conn.cursor()
        cursor.execute(env['monitor_sql'])
        row = cursor.fetchone()
        if row and row[env['monitor_value_position']]:
            metric = row[env['monitor_value_position']]
        else:
            metric = -1

        metric_to_datadog(env['metrics_name'], metric, os.environ['MSSQL_SERVER'], dd_tags)
        print("")
        conn.close()


def metric_to_datadog(metric_name, value, host, tags):
    print("    metric : {0}: {1}".format(metric_name, value)) 
    print("    tags : {0}".format(tags))
    api.Metric.send(metric=metric_name, points=value, host=host, tags=tags)

# datadog
dd_api_key = os.environ['DATADOG_API_KEY']
dd_app_key = os.environ['DATADOG_APP_KEY']
options = {
    'api_key':dd_api_key,
    'app_key':dd_app_key
}
initialize(**options)

# monitor
print("exec at {0}".format(datetime.now()))
print("")

monitor()


