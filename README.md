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
metrics_name: azure.sql_server_database.custom.moaikids.count_in_1m
monitor_sql: |
    SELECT
        count(*)
    FROM
        dbo.moaikids
    WHERE
        StatusTime > DATEADD(minute, -1, SYSDATETIMEOFFSET());
monitor_value_position: 0
dd_tags:
    env: prd
    application: moaikids
```


