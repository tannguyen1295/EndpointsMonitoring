# Usage

## Daemon

Daemon can be run either in producer or consumer mode which can be set using flags

    --producer: Producer mode
    --consumer: Consumer mode

Start daemon with command 

    python websites_monitoring_client.py --environment [env] --producer daemon start
    python websites_monitoring_client.py --environment [env] --consumer daemon start
    
Stop daemon with command

    python websites_monitoring_client.py --environment [env] --producer daemon stop
    python websites_monitoring_client.py --environment [env] --consumer daemon stop

There will be separate pid and log files for each running mode with the naming convention being [app_name]_[mode]. For example:

    [Log] websites_monitoring_producer.log | websites_monitoring_consumer.log 
    [Pid] websites_monitoring_producer.pid | websites_monitoring_consumer.pid

## Log

Log rotation set at midnight.

## Batch job

There're a posibility to run batch job command (e.g. to quickly fetch data from database)

    python websites_monitoring_client.py --environment [env] retrive_data_from_database