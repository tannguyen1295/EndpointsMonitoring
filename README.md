# Websites Monitoring

This project can be run as a Kafka producer to periodically check the availability of certain endpoints and optionally validate the content against regex. The result will be pushed to Kafka. Then this could also be run as a Kafka consumer to take the message from Kafka and put it into a PostgreSQL database.

## Python version

    >= 3.8

## Install dependencies

With pip

    pip install -r requirements.txt

And on dev env these too

    pip install -r requirements-dev.txt

## Testing

Run tests with command

    nosetests

# Additional dcoumentation

- [Usage](docs/usage.md)
- [Config reference](docs/config_reference.md)

# Attributions

The following sources have been used for reference purposes.
- [Daemon] https://web.archive.org/web/20160320091458/http://www.jejik.com/files/examples/daemon3x.py
- [Kafka] https://github.com/aiven/aiven-examples/tree/master/kafka/python
- [Kafka] https://towardsdatascience.com/kafka-python-explained-in-10-lines-of-code-800e3e07dad1
- [PostgreSQL] https://www.psycopg.org/docs/usage.html
- [PostgreSQL] https://github.com/aiven/aiven-examples/blob/master/postgresql/python/main.py
