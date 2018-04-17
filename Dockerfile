FROM ubuntu:xenial

RUN apt-get update && \
    #apt-get install -y gcc cron freetds-bin freetds-common freetds-dev libct4 libsybdb5 python3 python3-pip && \
    apt-get install -y cron curl apt-utils apt-transport-https debconf-utils gcc build-essential g++-5 && \
    apt-get install -y gcc python3 python3-pip python3-dev python3-setuptools && \
    apt-get update && apt-get install -y locales && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && locale-gen && \
    pip3 install --upgrade pip && \
    rm -rf /var/lib/apt/lists/*

# adding custom MS repository
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/16.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
# install SQL Server drivers
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql unixodbc-dev
# install SQL Server tools
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y mssql-tools
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
RUN /bin/bash -c "source ~/.bashrc"

# add program files
ADD ./requirements.txt ./requirements.txt
RUN pip3 install -r ./requirements.txt
ADD ./monitor.py /bin/monitor.py
RUN chmod +x /bin/monitor.py
RUN mkdir /bin/conf.d/
ADD ./conf.d/ /bin/conf.d/
ADD ./cron /etc/cron.d/monitor
RUN chmod 0644 /etc/cron.d/monitor && chmod +x /bin/monitor.py
ADD ./entrypoint.sh /bin/entrypoint.sh
RUN chmod +x /bin/entrypoint.sh

# env
ENV DATADOG_API_KEY=your_api_key \
    DATADOG_APP_KEY=your_app_key \
    MSSQL_SERVER=localhost \
    MSSQL_PORT=1433 \
    MSSQL_USER=sa \
    MSSQL_PASSWORD=VeryVerySercret@ \
    MSSQL_DATABASE=master \
    MSSQL_TYPE=sqlserver \
    RUNNING_MODE=parallel

# run
ENTRYPOINT /bin/entrypoint.sh

