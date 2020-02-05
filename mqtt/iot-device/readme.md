## IoT Device Code

### Summary
source/main.py is a simple Python script that subsribes to a specific MQTT topic via AWS IoT. Payloads are expected to be in the format:
```json
{ "duration": 5000 }
```
When a payload is received, the duration is extracted and used to toggle some GPIOs for the period specified in duration. After the duration has elapsed, the GPIOs are set back. The companion web-client directory can be used to publish payloads to the same topic as that referenced in main.py.

### Balena Application & Device Setup
+ Setup a Balena account if you don't already have one
+ Create a new application and setup a device in the Balena dashboard (instructions [here](https://www.balena.io/docs/learn/getting-started/raspberrypi3/python/))
+ Creating a device in the Balena dashboard results in a downloadable image
+ Install [Balena Etcher](https://www.balena.io/etcher/)<sup>1</sup>
+ Follow the prompts in Balena Etcher to flash your SD card
+ Once the flash is complete, place the SD card in your device and wait for the device to appear in the Balena dashboard


### Balena Push Instructions
+ Install [Balena CLI](https://github.com/balena-io/balena-cli/blob/master/INSTALL.md)
+ Open a command prompt and Navigate to the root directory of you project
+ Type "balena login" and follow the prompts to complete authentication
+ Type "balena apps" to see a list of apps
+ Type "balena push <app name>" to push your application
+ If the push is successful, an ASCII image of a unicorn is shown


-----
1. Found that Balena Etcher had problems (blanks screen) on Mac/Catalina and Windows 10 using installers. The portable version works on Windows 10.

