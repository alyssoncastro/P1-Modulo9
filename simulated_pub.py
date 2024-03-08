import paho.mqtt.client as mqtt
import json
import random
import time


def gerar_payload(sensor_id, sensor_type):
    return {
        "id": sensor_id,
        "tipo": sensor_type,
        "temperatura": round(random.uniform(-30, 30), 2),
        "timestamp": time.strftime("%d/%m/%Y %H:%M")
    }

def publicando(client, topic, payload):
    client.publish(topic, json.dumps(payload), qos=0)


def main():
    try:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "python_publisher")
        client.connect("localhost", 1883, 60)

        sensors = [
            {"id": "lj01f01", "tipo": "freezer"},
            {"id": "lj02f01", "tipo": "freezer"},
            {"id": "lj03g01", "tipo": "geladeira"},
            {"id": "lj04g01", "tipo": "geladeira"}
        ]

        print("Iniciando publicação simulada...")

        while True:
            for sensor in sensors:
                payload = gerar_payload(sensor["id"], sensor["tipo"])
                publicando(client, f"sensor/{sensor['tipo']}/{sensor['id']}", payload)
                time.sleep(5)  # Intervalo entre as leituras simuladas

    except KeyboardInterrupt:
        print("Publicação encerrada")
        client.disconnect()



if __name__ == "__main__":
    main()

