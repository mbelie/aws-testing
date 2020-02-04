import time
import uuid
import boto3
import json
import signal
import RPi.GPIO as gpio
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

ledPin = 11
relayPin = 7

# Topic to subscribe to. Same as what web-client is publishing to
topic = "3669"
clientId = str(uuid.uuid1())
mqttClient = AWSIoTMQTTClient(clientId)

# Substitute the host from AWS IoT
endpoint = "<endpoint from IoT Settings>"
port = 443
region = "<region>"
poolId = "<region>:<pool id>"
rootCaPath = "<path on IoT device to root pem>"

def Energize(durationMs):
    gpio.output(ledPin, True)
    gpio.output(relayPin, False)

    time.sleep(durationMs/1000)
    
    gpio.output(ledPin, False)
    gpio.output(relayPin, True)

def MessageReceived(client, userData, message):
    temp = json.loads(message.payload)
    durationMs = int(temp["duration"])
    print("Energizing for {}ms".format(durationMs))
    Energize(durationMs)


def Cleanup():
    gpio.cleanup()

def Setup():
    # Cleanup
    signal.signal(signal.SIGTERM, Cleanup)

    # GPIO
    gpio.setmode(gpio.BOARD)
    gpio.setup(ledPin, gpio.OUT)
    gpio.setup(relayPin, gpio.OUT)
    gpio.output(ledPin, False)
    gpio.output(relayPin, True)

    # MQTT
    cognitoIdentityClient = boto3.client('cognito-identity', region_name=region)
    temporaryIdentityId = cognitoIdentityClient.get_id(IdentityPoolId=poolId)
    identityId = temporaryIdentityId["IdentityId"]

    temporaryCredentials = cognitoIdentityClient.get_credentials_for_identity(IdentityId=identityId)
    accessKeyId = temporaryCredentials["Credentials"]["AccessKeyId"]
    secretKey = temporaryCredentials["Credentials"]["SecretKey"]
    sessionToken = temporaryCredentials["Credentials"]["SessionToken"]

    mqttClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
    mqttClient.configureEndpoint(endpoint, port)
    mqttClient.configureCredentials(rootCaPath)
    mqttClient.configureIAMCredentials(accessKeyId, secretKey, sessionToken)
    
    # Base back off(s), max back off(s), stable time(s)
    mqttClient.configureAutoReconnectBackoffTime(1, 32, 20)

    # 0: disabled, -1: infinite queueing
    mqttClient.configureOfflinePublishQueueing(-1)  

    # Frequency of draining in seconds when connection is established
    mqttClient.configureDrainingFrequency(2)

    # Time in seconds to wait for CONNACK or disconnect
    mqttClient.configureConnectDisconnectTimeout(10)

    # General timeout in seconds for MQTT operations
    mqttClient.configureMQTTOperationTimeout(5)

    mqttClient.connect()
    mqttClient.subscribe(topic, 1, MessageReceived)
    
Setup()

while True:
    time.sleep(2)

gpio.cleanup()