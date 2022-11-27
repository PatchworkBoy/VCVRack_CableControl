# VCVRack_CableControl
A virtual cable controller for VCVRack which requires nothing more than a Raspberry Pi Pico. Written in CircuitPython

Use with Stoermelder's VCVRack Pack-Tau T7 modules to map MIDI CC to module ports in VCVRack: https://github.com/stoermelder/vcvrack-packtau

* GPIO2-14 are (potentially stackable) outputs mapped to MIDI CC1-13 Ch1
* GPIO15-27 are (non-stackable) inputs mapped to MIDI CC14-26 Ch1
* When outputs are shorted to inputs, the matching pair of MIDI CC transmit
level 127.
* When disconnected, the matching pair transmit level 0
* Pack-Tau T7-CTRL/T7-MIDI translate the pairs of MIDI CC Gates into a cable link between ports mapped to those CCs via a JSON file (see examples/ folder)

Attach tip connector of 3.5mm socket to each GPIO pin. Short with mono 3.5mm patch leads. Done!

GPIO0 & 1 are skipped as I intend to use the UART to link multiple Picos to one "master". Really any expansion needs doing over i2c or SPI. This is all just a quick dirty example.

**What's happening on the Pico:** ALL GPIO PINS are set as input and pulled high in the code. GPIO Pins 2 thru 14 are switched to outputs one at a time and pulled low and then GPIO Pins 15 thru 27 are scanned for any also pulled low. Their state is compared against and a statematrix dictionary object - if the state changes, the relevant MIDI CC codes are sent to reflect the change - then the statematrix updated to store the latest current state. The current GPIO Output is then switched back to an input pulled high, and moves on to the next output pin. This prevents any pair of pins being set as an Output simultaneously, as a short between two pins set as Outputs would damage the Pico. This scanning process runs in a continuous loop.

![PiPico GPIO Pins](https://cdn-learn.adafruit.com/assets/assets/000/099/339/large1024/raspberry_pi_Pico-R3-Pinout-narrow.png)

If running multiples as it stands, change MIDI channels in code and **don't link across Picos**.

## Usage Example

![Image of PiPico with screenshot of VCV Rack Example](https://github.com/PatchworkBoy/VCVRack_CableControl/raw/main/media/demo.jpg)

* Grab Pack-Tau (https://github.com/stoermelder/vcvrack-packtau/releases) and manually install.
* Copy code.py & lib/ folder to Pi Pico running CircuitPython
* Open examples/t7-ctrl_example.vcv in VCVRack (requires Pack-Tau, BogAudio, Instruo & VCV Fundamentals)
* Short any of GPIO2-14 to GPIO15-26. **Be careful NOT to inadvertently short to RUN or GND.**

To load a custom map, click ports on your modules and watch T7-Assistant module. Note the moduleId and portId (you can highlight and copy them from the T7-Assistant display) 

![T7-ASSISTANT](https://github.com/PatchworkBoy/VCVRack_CableControl/raw/main/media/t7-assistant.jpg)

Open examples/t7-ctrl_blank.json in a text editor... add/paste the relevant moduleId and PortId (pay attention to the portType in the JSON file - output portIds for output port types, input portIds for input port types) to the CC to be mapped to that port. This maps to the equivalent GPIO pin [CC - 1].

![codeblock](https://github.com/PatchworkBoy/VCVRack_CableControl/raw/main/media/codeblock.jpg)

![completed codeblock](https://github.com/PatchworkBoy/VCVRack_CableControl/raw/main/media/completedblock.jpg)

Once you've got that done for all the ports in the file, select all > copy. Right click T7-Ctrl > Paste JSON. 

![Context Menu of T7-CTRL](https://github.com/PatchworkBoy/VCVRack_CableControl/raw/main/media/copy_paste_json.jpg)

**NOTE: T7-MIDI module MUST be adjacent to the right of the T7-CTRL module for MIDI commands to be transmitted from T7-MIDI to T7-CTRL. Select the PiPico midi device in T7-MIDI.**

Now start shorting your Pins and watch cables appear between the mapped ports, and disappear when you unshort.
