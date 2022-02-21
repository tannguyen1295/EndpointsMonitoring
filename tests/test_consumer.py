import unittest
from unittest import mock
from lib.consumer import Consumer

class TestWebsiteChecker(unittest.TestCase):
    def setUp(self):
        self.configs = {
            "kafka_general": '''{
                "service_uri": "", 
                "ca_path": "", 
                "cert_path": "", 
                "key_path": "", 
                "topic": "", 
                "security_protocol": ""
            }''',
            "kafka_consumer": '''{
                "topics": [], 
                "auto_offset_reset": "", 
                "group_id": "", 
                "consumer_timeout_ms": 10000
            }''',
            "database": '''{
                "service_uri": "", 
                "ca_path": "", 
                "cert_path": "", 
                "key_path": "", 
                "topic": ""
            }'''
        }

        self.mock_logger = unittest.mock.Mock()

    def test_retrieveMessagesFromTopic_twoDifferentTopics_eachMessageShouldHaveCorrectTopic(self):
        message_1_mock_response = mock.Mock()
        message_1_mock_response.topic = "topic_1"
        message_1_mock_response.value = b'''{
            "url": "https://www.test1.com",
            "status": {
                    "timestamp": "06-02-2022T17:15:52Z",
                    "response_time_in_millisecond": 50,
                    "status_code": 200,
                    "content_validation": {
                        "regex": "[a-zA-Z0-9]",
                        "content_matched": true
                }
            }
        }'''

        message_2_mock_response = mock.Mock()
        message_2_mock_response.topic = "topic_2"
        message_2_mock_response.value = b'''{
            "url": "https://www.test2.com",
            "status": {
                "timestamp": "06-02-2022T18:15:52Z",
                "response_time_in_millisecond": 20,
                "status_code": 200,
                "content_validation": {
                    "regex": "[a-zA-Z0-9]",
                    "content_matched": true
                }
            }
        }'''

        Consumer._get_kafka_consumer = mock.Mock()
        Consumer._get_kafka_consumer.return_value = [message_1_mock_response, message_2_mock_response]
        Consumer._close_kafka_consumer = mock.Mock()

        result = Consumer(self.configs, self.mock_logger)._retrieve_messages_from_topic()
        expected_result = [
            {
                "topic": "topic_1",
                "value": {
                    "url": "https://www.test1.com",
                    "status": {
                            "timestamp": "06-02-2022T17:15:52Z",
                            "response_time_in_millisecond": 50,
                            "status_code": 200,
                            "content_validation": {
                                "regex": "[a-zA-Z0-9]",
                                "content_matched": True
                            }
                    }
                }
            },{
                "topic": "topic_2",
                "value": {
                    "url": "https://www.test2.com",
                    "status": {
                            "timestamp": "06-02-2022T18:15:52Z",
                            "response_time_in_millisecond": 20,
                            "status_code": 200,
                            "content_validation": {
                                "regex": "[a-zA-Z0-9]",
                                "content_matched": True
                        }
                    }
                }
            }
        ]

        self.assertEqual(result, expected_result)

    def test_retrieveMessagesFromTopic_sameTopics_allMessagesShouldHaveSameTopic(self):
        message_1_mock_response = mock.Mock()
        message_1_mock_response.topic = "topic_1"
        message_1_mock_response.value = b'''{
            "url": "https://www.test1.com",
            "status": {
                    "timestamp": "06-02-2022T17:15:52Z",
                    "response_time_in_millisecond": 50,
                    "status_code": 200,
                    "content_validation": {
                        "regex": "[a-zA-Z0-9]",
                        "content_matched": true
                }
            }
        }'''

        message_2_mock_response = mock.Mock()
        message_2_mock_response.topic = "topic_1"
        message_2_mock_response.value = b'''{
            "url": "https://www.test2.com",
            "status": {
                "timestamp": "06-02-2022T18:15:52Z",
                "response_time_in_millisecond": 20,
                "status_code": 200,
                "content_validation": {
                    "regex": "[a-zA-Z0-9]",
                    "content_matched": true
                }
            }
        }'''

        Consumer._get_kafka_consumer = mock.Mock()
        Consumer._get_kafka_consumer.return_value = [message_1_mock_response, message_2_mock_response]
        Consumer._close_kafka_consumer = mock.Mock()

        result = Consumer(self.configs, self.mock_logger)._retrieve_messages_from_topic()
        expected_result = [
            {
                "topic": "topic_1",
                "value": {
                    "url": "https://www.test1.com",
                    "status": {
                            "timestamp": "06-02-2022T17:15:52Z",
                            "response_time_in_millisecond": 50,
                            "status_code": 200,
                            "content_validation": {
                                "regex": "[a-zA-Z0-9]",
                                "content_matched": True
                            }
                    }
                }
            },{
                "topic": "topic_1",
                "value": {
                    "url": "https://www.test2.com",
                    "status": {
                            "timestamp": "06-02-2022T18:15:52Z",
                            "response_time_in_millisecond": 20,
                            "status_code": 200,
                            "content_validation": {
                                "regex": "[a-zA-Z0-9]",
                                "content_matched": True
                        }
                    }
                }
            }
        ]

        self.assertEqual(result, expected_result)

    def test_retrieveMessagesFromTopic_message1StatusIsNull_nullValuesShouldBePassedToResult(self):
        message_1_mock_response = mock.Mock()
        message_1_mock_response.topic = "topic_1"
        message_1_mock_response.value = b'''{
            "url": "https://www.test1.com",
            "status": {
                    "timestamp": "06-02-2022T17:15:52Z",
                    "response_time_in_millisecond": null,
                    "status_code": null,
                    "content_validation": {
                        "regex": "[a-zA-Z0-9]",
                        "content_matched": null
                }
            }
        }'''

        message_2_mock_response = mock.Mock()
        message_2_mock_response.topic = "topic_1"
        message_2_mock_response.value = b'''{
            "url": "https://www.test2.com",
            "status": {
                "timestamp": "06-02-2022T18:15:52Z",
                "response_time_in_millisecond": 20,
                "status_code": 200,
                "content_validation": {
                    "regex": "[a-zA-Z0-9]",
                    "content_matched": true
                }
            }
        }'''

        Consumer._get_kafka_consumer = mock.Mock()
        Consumer._get_kafka_consumer.return_value = [message_1_mock_response, message_2_mock_response]
        Consumer._close_kafka_consumer = mock.Mock()

        result = Consumer(self.configs, self.mock_logger)._retrieve_messages_from_topic()
        expected_result = [
            {
                "topic": "topic_1",
                "value": {
                    "url": "https://www.test1.com",
                    "status": {
                            "timestamp": "06-02-2022T17:15:52Z",
                            "response_time_in_millisecond": None,
                            "status_code": None,
                            "content_validation": {
                                "regex": "[a-zA-Z0-9]",
                                "content_matched": None
                            }
                    }
                }
            },{
                "topic": "topic_1",
                "value": {
                    "url": "https://www.test2.com",
                    "status": {
                            "timestamp": "06-02-2022T18:15:52Z",
                            "response_time_in_millisecond": 20,
                            "status_code": 200,
                            "content_validation": {
                                "regex": "[a-zA-Z0-9]",
                                "content_matched": True
                        }
                    }
                }
            }
        ]

        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
