import time
import json
import requests
import urllib3
from lib.daemon import Daemon
from lib.producer import Producer
from lib.consumer import Consumer

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class WebsitesMonitoringDaemon(Daemon):
    def set_settings(self, configs, verify_ssl, args):
        self.to_be_checked_websites = json.loads(configs.get("to_be_checked_websites"))
        self.checking_interval = int(configs.get("checking_interval"))
        self.args = args

        if args.producer:
            session = requests.Session()
            session.verify = verify_ssl

            self.producer = Producer(session, configs, self.logger)

        elif args.consumer:
            self.consumer = Consumer(configs, self.logger)

    def run(self):
        while True:
            try:
                if self.args.producer:
                    self.producer.check_websites(self.to_be_checked_websites)

                elif self.args.consumer:
                    self.consumer.consume_data()

                time.sleep(self.checking_interval)

            except Exception as err:
                self.logger.error(f"Unexpected error occured: {err}")
                self.logger.error(f"Error type: {type(err)}")
