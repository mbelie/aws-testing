## IoT Device Code

### Summary
source/main.py is a simple Python script that subsribes to a specific MQTT topic via AWS IoT. Payloads are expected to be in the format "{'duration': <MS VALUE>}". When a payload is received, the duration is extracted and used to toggle two GPIOs for the period specified in" "duration". After the duration has elapsed, the GPIOs are set back. The companion web-client directory can be used to publish payloads to the same topic referenced in main.py.

### Balena Install Instructions
+ Setup a Balena account if you don't already have one
+ Create an application in the Balena dashboard
+ Setup a [device](https://www.balena.io/docs/learn/getting-started/raspberrypi3/python/)
+ Install [Balena CLI](https://github.com/balena-io/balena-cli/blob/master/INSTALL.md)

### Balena Push Instructions
+ Open a command prompt and Navigate to the root directory of you project
+ Type "balena login" and follow the authentication prompts
+ Type "balena apps" to see a list of apps
+ Type "balena push <app name>" to push the application
+ If the application is successfully pushed to Balena, you'll get a nice ASCII unicorn image

