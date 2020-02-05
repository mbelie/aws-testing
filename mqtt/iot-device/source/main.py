import time
import uuid
import boto3
import json
import signal
import gpiozero
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

durationLedGpioId = 17
activeLedGpioId = 27
relayGpioId = 4

relay = gpiozero.OutputDevice(relayGpioId, active_high=False, initial_value=False)
durationLed = gpiozero.OutputDevice(durationLedGpioId, active_high=True, initial_value=False)
activeLed = gpiozero.OutputDevice(activeLedGpioId, active_high=True, initial_value=False)

# Topic to subscribe to. Same as what web-client is publishing to
topic = "3669"
clientId = str(uuid.uuid1())
mqttClient = AWSIoTMQTTClient(clientId)

port = 443
endpoint = "<endpoint from IoT Settings>"
region = "<region>"
poolId = "<region>:<pool id>"
rootCaPath = "<path on IoT device to root pem>"

def Energize(durationMs):
    relay.on()
    durationLed.on()

    time.sleep(durationMs/1000)
    
    relay.off()
    durationLed.off()

def MessageReceived(client, userData, message):
    payload = message.payload.decode("utf-8")
    print("payload: {}".format(payload))
    temp = json.loads(payload)
    durationMs = int(temp["duration"])
    print("Energizing for {}ms".format(durationMs))
    Energize(durationMs)

def Cleanup():
    activeLed.off()
    durationLed.off()
    relay.off()

    activeLed.close()
    durationLed.close()
    relay.close()

def Setup():
    # Cleanup
    signal.signal(signal.SIGTERM, Cleanup)

    # Stat
    activeLed.on()

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

Cleanup()