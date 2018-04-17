cron && touch /etc/cron.d/monitor && env | grep -v no_proxy > /etc/environment && tail -f /dev/null
