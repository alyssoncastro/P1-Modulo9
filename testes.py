import unittest
from unittest.mock import patch
from simulated_pub import generate_payload, publish_simulated_data
from monitoramento import Monitoramento 



class TestSimulator(unittest.TestCase):


    def gerar_testes(self):
        payload = generate_payload("test_id", "freezer")
        self.assertIsInstance(payload, dict)
        self.assertIn("id", payload)
        self.assertIn("tipo", payload)
        self.assertIn("temperatura", payload)
        self.assertIn("timestamp", payload)

    @patch("simulated_pub.mqtt.Client")
    def gerar_testes_dados(self, mock_mqtt_client):
        client = mock_mqtt_client.return_value
        publish_simulated_data(client, "test/topic", {"id": "test_id", "tipo": "freezer"})
        client.publish.assert_called_once_with("test/topic", '{"id": "test_id", "tipo": "freezer"}', qos=0)

    def test_on_message(self):
   
        monitoramento = Monitoramento() 
        userdata = {"last_message": None, "callback_called": False}
        message_topic = "sensor/freezer/test_id"
        message_payload = '{"id": "test_id", "tipo": "freezer", "temperatura": -20, "timestamp": "01/03/2024 14:30"}'
        

        monitoramento.on_message(None, userdata, mqtt.MQTTMessage(topic=message_topic, payload=message_payload))

        self.assertEqual(userdata["last_message"], message_payload)
        self.assertTrue(userdata["callback_called"])

if __name__ == '__main__':
    unittest.main()
