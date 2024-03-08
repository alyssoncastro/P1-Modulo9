import paho.mqtt.client as mqtt
import json



def on_message(client, userdata, message):

    payload = json.loads(message.payload.decode())
    temperature = payload["temperatura"]
    sensor_id = payload["id"]
    sensor_type = payload["tipo"]



    if (sensor_type == "freezer" and (temperature > -15 or temperature < -25)) or \
       (sensor_type == "geladeira" and (temperature > 10 or temperature < 2)):
        print(f"Lj {sensor_id}: {sensor_type.capitalize()} {temperature}°C [ALERTA: Temperatura {'ALTA' if temperature > 10 else 'BAIXA'}]")
    else:
        print(f"Lj {sensor_id}: {sensor_type.capitalize()} {temperature}°C")


def main():

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "python_publisher")
    client.connect("localhost", 1883, 60)


    client.subscribe("sensor/freezer/#")
    client.subscribe("sensor/geladeira/#")
    client.on_message = on_message


    client.loop_forever()


if __name__ == "__main__":
    main()
