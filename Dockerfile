FROM python:3.6

RUN apt-get update && \
    apt-get install -y gcc cron freetds-dev && \
    pip install --upgrade pip

ADD requirements.txt ./
RUN pip install -r requirements.txt

ADD ./monitor.py /bin/monitor.py
RUN chmod +x /bin/monitor.py

RUN mkdir /bin/conf.d/
ADD ./conf.d/ /bin/conf.d/

ADD ./cron /etc/cron.d/monitor
RUN chmod 0644 /etc/cron.d/monitor && chmod +x /bin/monitor.py

# for debug
RUN apt-get install -y nodejs npm
RUN npm install -g sql-cli

ENV DATADOG_API_KEY=your_api_key \
    DATADOG_APP_KEY=your_app_key \
    MSSQL_SERVER=localhost \
    MSSQL_PORT=1433 \
    MSSQL_USER=sa \
    MSSQL_PASSWORD=VeryVerySercret@ \
    MSSQL_DATABASE=master \
    MSSQL_TIMEOUT=1


CMD cron && touch /etc/cron.d/monitor && tail -f /dev/null


