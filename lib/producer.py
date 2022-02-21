import requests
import json
import re
import datetime
from kafka import KafkaProducer

class Producer:
    def __init__(self, session, configs, logger):
        self.session = session
        self.kafka_config = json.loads(configs["kafka_general"])
        self.kafka_producer_config = json.loads(configs["kafka_producer"])
        self.logger = logger

    def check_websites(self, websites):
        self.logger.info(f"Start checking websites {[website['url'] for website in websites]}")
        
        results = self._validate_websites(websites)
        
        self._send_websites_statuses_to_kafka(results)

        self.logger.info("Process done!")

    def _validate_websites(self, websites):
        results = []

        for website in websites:
            website_status = self._validate_website(website["url"], website["regex"])
            results.append({
                "url": website["url"],
                "status": website_status,
                "topic": website["topic"]
            })

        return results

    def _validate_website(self, url, regex):
        self.logger.info(f"Validating website '{url}'")
        
        resp = self._send_request(url)

        return self._validate_response(resp, url, regex)

    def _send_request(self, url):
        try:
            self.logger.debug(f"GET: {url}")

            resp = self.session.get(url, timeout=self.kafka_producer_config["request_timeout"])

            self.logger.debug(f"Response status code: {resp.status_code}")
            self.logger.debug(f"Response content: {resp.text}".encode("utf-8"))

            return resp

        except Exception as err:
            self.logger.error(f"Failed to send request to '{url}'. Error message: {err}")
            self.logger.error(f"Error type: {type(err)}")

            return None

    def _validate_response(self, resp, url, regex):
        #Site can be reached
        if resp:
            status_code = resp.status_code
            time = self._convert_http_timestamp_to_utc_timestamp(resp.headers["Date"], format='%a, %d %b %Y %H:%M:%S GMT')
            response_time_in_millisecond = resp.elapsed.total_seconds() * 1000
            is_content_matched = self._validate_content(resp, regex)

            self.logger.info(f"{status_code} Response_time: {response_time_in_millisecond}ms Content_matched:{is_content_matched} {url}")

        #Site cannot be reached
        else:
            self.logger.warn(f"Skip validating '{url}'")

            status_code = None
            time = self._convert_to_utc_timestamp(datetime.datetime.now(datetime.timezone.utc))
            response_time_in_millisecond = None
            is_content_matched = None

        return {
            "timestamp": time,
            "response_time_in_millisecond": response_time_in_millisecond,
            "status_code": status_code,
            "content_validation": {
                "regex": regex,
                "content_matched": is_content_matched
            }
        }

    def _convert_http_timestamp_to_utc_timestamp(self, http_timestamp, format):
        http_datetime = datetime.datetime.strptime(http_timestamp, format)

        http_datetime_utc_timezone = http_datetime.astimezone(datetime.timezone.utc)

        return self._convert_to_utc_timestamp(http_datetime_utc_timezone)

    def _convert_to_utc_timestamp(self, original_datetime):
        return original_datetime.strftime("%d-%m-%YT%H:%M:%SZ")

    def _validate_content(self, resp, regex):
        if regex:
            self.logger.debug(f"Validating content from the request to '{resp.url}' against regex '{regex}'")
            
            matched = re.match(regex, resp.text)
            return bool(matched)

        else:
            self.logger.debug(f"No regex set for website '{resp.url}'")
            return True

    def _send_websites_statuses_to_kafka(self, websites):
        producer = self._get_kafka_producer()

        for website in websites:
            self.logger.info(f"Sending status of {website['url']} to kafka")
            
            data =self._prepare_data_for_kafka(website)

            self.logger.debug(f"Sending to topic '{website['topic']}': {data}")

            producer.send(website["topic"], json.dumps(data).encode("utf-8"))

        producer.flush()

    def _get_kafka_producer(self):
        return KafkaProducer(bootstrap_servers = self.kafka_config["service_uri"],
                            security_protocol = self.kafka_config["security_protocol"],
                            ssl_cafile = self.kafka_config["ca_path"],
                            ssl_certfile = self.kafka_config["cert_path"],
                            ssl_keyfile = self.kafka_config["key_path"])

    def _prepare_data_for_kafka(self, website_data):
        return {
            "url": website_data["url"],
            "status": website_data["status"]
        }
