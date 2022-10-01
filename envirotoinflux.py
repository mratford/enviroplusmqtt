import argparse
import paho.mqtt.client as mqtt
import time

# mqtt callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected OK")
    else:
        print("Bad connection Returned code=", rc)


def on_message(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)


def on_publish(client, userdata, mid):
    print("mid: " + str(mid))


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Receive enviroplus values over mqtt and send to homebridge-mqttthing"
            " and influxdb"
        )
    )
    parser.add_argument(
        "--broker",
        default="127.0.0.1",
        type=str,
        help="mqtt broker IP",
    )
    parser.add_argument(
        "--port",
        default=1883,
        type=int,
        help="mqtt broker port",
    )
    parser.add_argument("--username", default=None, type=str, help="mqtt username")
    parser.add_argument("--password", default=None, type=str, help="mqtt password")
    parser.add_argument(
        "--client_id", default="envirotoinflux", type=str, help="Client id for mqtt"
    )
    args = parser.parse_args()

    mqtt_client = mqtt.Client(args.client_id)

    if args.username is not None:
        mqtt_client.username_pw_set(args.username, password=args.password)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_publish = on_publish
    mqtt_client.on_message = on_message
    mqtt_client.connect(args.broker, port=args.port)
    mqtt_client.subscribe("enviro")

    mqtt_client.loop_start()
    while True:
        time.sleep(100000000)


if __name__ == "__main__":
    main()
