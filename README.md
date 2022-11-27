# VCVRack_CableControl
A virtual cable controller for VCVRack which requires nothing more than a Raspberry Pi Pico. Written in CircuitPython

Use with Stoermelder's VCVRack Pack-Tau T7 modules to map MIDI CC to module ports in VCVRack: https://github.com/stoermelder/vcvrack-packtau

* GPIO2-14 are (potentially) stackable outputs mapped to MIDI CC1-13 Ch1
* GPIO15-27 are non-stackable inputs mapped to MIDI CC14-26 Ch1
* When outputs are shorted to inputs, the matching pair of MIDI CC transmit
level 127.
* When disconnected, the matching pair transmit level 0
* Pack-Tau T7-CTRL/T7-MIDI translate the pairs of MIDI CC Gates into a cable link between ports mapped to those CCs via a JSON file (see examples/ folder)

Attach tip connector of 3.5mm socket to each GPIO pin. Short with mono 3.5mm patch leads. Done!

GPIO0 & 1 are skipped as I intend to use the UART to link multiple Picos to one "master". Really any expansion needs doing over i2c or SPI. This is all just a quick dirty example.

If running multiples as it stands, change MIDI channels in code and **don't link across Picos**.

## Usage Example

![Image of PiPico with screenshot of VCV Rack Example](https://github.com/PatchworkBoy/VCVRack_CableControl/raw/main/media/demo.jpg)

* Grab Pack-Tau (https://github.com/stoermelder/vcvrack-packtau/releases) and manually install.
* Copy code.py & lib/ folder to Pi Pico running CircuitPython
* Open examples/t7-ctrl_example.vcv in VCVRack (requires Pack-Tau, BogAudio, Instruo & VCV Fundamentals)
* Short any of GPIO2-14 to GPIO15-26. **Be careful NOT to inadvertently short to RUN or GND.**

To load a custom map, click ports on your modules and watch T7-Assistant module. Note the moduleId and portId. Open examples/t7-ctrl_blank.json... add the relevant moduleId and PortId (pay attention to the portType in the JSON file - output portIds for output port types, input portIds for input port types) to the CC to be mapped to that port. This maps to the equivalent GPIO pin [CC - 1].

Once you've got that done for the ports you want to play with, select all > copy. Right click T7-Ctrl > Paste JSON. 

![Context Menu of T7-CTRL](https://github.com/PatchworkBoy/VCVRack_CableControl/raw/main/media/copy_paste_json.jpg)

**NOTE: T7-MIDI module MUST be adjacent to the right of the T7-CTRL module. Select the PiPico midi device in T7-MIDI.**
