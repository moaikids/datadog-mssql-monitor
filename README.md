# MSSQL monitor using Datadog
This is the script to notify Datadog of the value of MSSQL for monitoring service.

## usage
This script run on the Docker container.

### file tree
- README.md
  - (this file)
- monitor.py
  - monitor script
- conf.d/*.yaml
  - configuration files for monitor
- cron
  - configuration file for crontab

### configuration file for monitor (conf.d/*yaml)
If you want to add monitoring, add yaml file into `conf.d/` directory.

```example:yaml
metrics_name: sql_server.custom.hoge.fuga
monitor_sql: |
    SELECT-
        count(*)
    FROM-
        sys.databases;
monitor_value_position: 0
dd_tags:
    env: prd
    project: hoge
    application: mssql
```


