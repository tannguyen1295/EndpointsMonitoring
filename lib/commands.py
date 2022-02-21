import os
import json
import psycopg2
from psycopg2 import sql
from configparser import ConfigParser
from lib.websites_monitoring_daemon import WebsitesMonitoringDaemon
from lib.logger import Logger

def daemon(namespace, extra_args):
    configs = _parse_config(namespace.environment)
    settings = configs["settings"]

    #Prepare for daemon
    app_name = _set_app_name(settings['app_name'], "producer" if namespace.producer else "consumer")
    logger = _set_logger(app_name, settings["log_path"], namespace.log_level)
    pid_file = _get_pid_file(settings["pid_path"], app_name)

    #Set up daemon
    websites_monitoring_daemon = WebsitesMonitoringDaemon(pid_file, logger=logger)
    websites_monitoring_daemon.set_settings(configs["websites_monitoring"], namespace.verify_ssl, namespace)

    if "start" in extra_args:
        websites_monitoring_daemon.start()
    elif "stop" in extra_args:
        websites_monitoring_daemon.stop()
    elif "restart" in extra_args:
        websites_monitoring_daemon.restart()
    else:
        print("Cannot find a correct action for the daemon.")

def _set_app_name(app_name, running_mode):
    return f"{app_name}_{running_mode}"

def _get_pid_file(pid_path, app_name):
    return os.path.join(pid_path, f"{app_name}_daemon.pid")

def _set_logger(app_name, log_path, log_level):
    return Logger(app_name, log_path=log_path, log_level=log_level).logger

def cmd_retrive_data_from_database(namespace, extra_args):
    configs = _parse_config(namespace.environment)
    database_config = json.loads(configs["websites_monitoring"]["database"])
    table_name = database_config["table"]

    #Setup database connection
    db_conn = psycopg2.connect(database_config["service_uri"])
    cursor = db_conn.cursor()

    #Execute SQL
    cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name)))

    #Display the result
    for row in cursor.fetchall():
        print(row)

def _parse_config(environment):
    #Parse environment config
    
    if os.path.isfile(environment):
        env_file =  environment

    #Retrieve *.ini file in environments directory
    #Since this commands.py file is in lib directory, we need to go back to its parent by adding os.pardir
    else:
        env_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "environments", f"{environment}.ini")

        if not os.path.isfile(env_file):
            exit(f"File {env_file} not found")

    config = ConfigParser()
    config.read(env_file)

    return config
