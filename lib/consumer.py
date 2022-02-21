import json
import psycopg2
from psycopg2 import sql
from kafka import KafkaConsumer

class Consumer:
    def __init__(self, configs, logger):
        self.kafka_config = json.loads(configs["kafka_general"])
        self.kafka_consumer_config = json.loads(configs["kafka_consumer"])
        self.database_config = json.loads(configs["database"])
        self.db_connection = psycopg2.connect(self.database_config["service_uri"])
        self.logger = logger

    def consume_data(self):
        self.logger.info("Start consuming data")

        messages = self._retrieve_messages_from_topic()

        self._send_messages_to_database(messages)

        self.logger.info("Process done!")

    def _retrieve_messages_from_topic(self):
        self.logger.info("Retrieving messages from Kafka")

        retrieved_messages = []

        consumer = self._get_kafka_consumer()

        for message in consumer:
            self._add_kafka_message_to_list(message, retrieved_messages)

        self._close_kafka_consumer(consumer)

        return retrieved_messages

    def _get_kafka_consumer(self):
        consumer = KafkaConsumer(bootstrap_servers = self.kafka_config["service_uri"],
                                ssl_cafile = self.kafka_config["ca_path"],
                                ssl_certfile = self.kafka_config["cert_path"],
                                ssl_keyfile = self.kafka_config["key_path"],
                                security_protocol = self.kafka_config["security_protocol"],
                                group_id = self.kafka_consumer_config["group_id"],
                                auto_offset_reset = self.kafka_consumer_config["auto_offset_reset"],
                                consumer_timeout_ms = self.kafka_consumer_config["consumer_timeout_ms"])

        consumer.subscribe(self.kafka_consumer_config["topics"])

        return consumer

    def _add_kafka_message_to_list(self, kafka_message, retrieved_messages):
        decoded_message = json.loads(kafka_message.value.decode('utf-8'))

        self.logger.info(f"Message retrieved from topic '{kafka_message.topic}': {decoded_message}")

        retrieved_messages.append({
            "topic": kafka_message.topic,
            "value": decoded_message
        })

    def _close_kafka_consumer(self, consumer):
        consumer.close()

    def _send_messages_to_database(self, messages):
        self.logger.info(f"Sending {len(messages)} messages to database")

        cursor = self.db_connection.cursor()

        for message in messages:
            try:
                cursor.execute(sql.SQL("INSERT INTO {} (url, timestamp, status_code, response_time_in_millisecond, regex, content_matched, kafka_topic) VALUES (%s, %s, %s, %s, %s, %s, %s)").
                                        format(sql.Identifier(self.database_config["table"])),
                                        (message["value"]["url"],
                                        message["value"]["status"]["timestamp"],
                                        message["value"]["status"]["status_code"],
                                        message["value"]["status"]["response_time_in_millisecond"],
                                        message["value"]["status"]["content_validation"]["regex"],
                                        message["value"]["status"]["content_validation"]["content_matched"],
                                        message["topic"]))

            except Exception as err:
                self.logger.error(f"Failed to add message to table '{self.database_config['table']}: {message}'")
                self.logger.error(f"Error type: {type(err)}")

                self.db_connection.rollback()

            else:
                self.db_connection.commit()

        cursor.close()
