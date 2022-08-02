# Endpoints Monitoring

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
    
## Configuration

There's a template under environments/dev.ini that could be used. More details could be found in [Config reference](docs/config_reference.md).

# Additional dcoumentation

- [Usage](docs/usage.md)
- [Config reference](docs/config_reference.md)
- [Config example](environments/dev.ini)

# Attributions

The following sources have been used for reference purposes.
- [Daemon] https://web.archive.org/web/20160320091458/http://www.jejik.com/files/examples/daemon3x.py
- [Kafka] https://towardsdatascience.com/kafka-python-explained-in-10-lines-of-code-800e3e07dad1
- [PostgreSQL] https://www.psycopg.org/docs/usage.html
