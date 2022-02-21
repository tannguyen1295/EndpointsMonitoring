import argparse
from lib.commands import daemon, cmd_retrive_data_from_database

COMMANDS = {}
COMMANDS["daemon"] = daemon
COMMANDS["retrive_data_from_database"] = cmd_retrive_data_from_database

def main():
    #Parsing given arguments
    namespace, extra_args = parse_args()

    #According function will be run based on the given arguments
    for name, function in COMMANDS.items():
        if name == namespace.cmd:
            function(namespace, extra_args)

def parse_args():
    parser = argparse.ArgumentParser(description="Parsing command line arguments")

    parser.add_argument("--verify-ssl", action="store_true",
                        help="Indicate whether to use certificate for the checking requests")

    parser.add_argument("--environment", "-e", nargs="?", default="dev",
                        help="The environment that the daemon will work on")

    parser.add_argument("--log-level", nargs="?", default="info",
                        help="Set log level (info, debug, etc)")

    parser.add_argument("--producer", action="store_true",
                        help="Run Kafka producer")

    parser.add_argument("--consumer", action="store_true",
                        help="Run Kafka consumer")

    parser.add_argument('cmd', nargs="?",
                        help='Determine which function will be run')

    namespace, extra_args = parser.parse_known_args()

    validate_args(namespace, extra_args)

    return namespace, extra_args

def validate_args(namespace, extra_args):
    #Either producer or consumer need to be given when running daemon
    if "daemon" in extra_args:
        if namespace.producer and namespace.consumer:
            fail("--producer and --consumer are mutually exclusive")

        elif not namespace.producer and not namespace.consumer:
            fail("--producer or --consumer are required")

def fail(message):
    print(message)
    exit(1)

if __name__ == "__main__":
    main()
