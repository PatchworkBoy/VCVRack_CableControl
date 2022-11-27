# VCVRack_CableControl
A virtual cable controller for VCVRack which requires nothing more than a Raspberry Pi Pico (or other CircuitPython compatible Microcontroller). Written in CircuitPython. Provides 26x physical sockets which can be distributed as inputs or outputs via entries at lines 23 & 27 of code.py, which are then remapped to MIDI CC gates (1-indexed sequentially, outputs then inputs). MIDI Output channel is set at end of line 17 (0-indexed in code, becomes 1-indexed in reality) 

Use with Stoermelder's (experimental) **VCVRack-PackTau** T7 modules which maps MIDI CC Gates to module i/o ports in VCVRack: https://github.com/stoermelder/vcvrack-packtau

* GPIO2-14 are (potentially stackable) outputs mapped to MIDI CC1-13 Ch1
* GPIO15-27 are (non-stackable) inputs mapped to MIDI CC14-26 Ch1
* When outputs are shorted to inputs, the matching pair of MIDI CC transmit
level 127.
* When disconnected, the matching pair transmit level 0
* Pack-Tau T7-CTRL/T7-MIDI translate the pairs of MIDI CC Gates into a cable link between ports mapped to those CCs via a JSON file loaded into T7-CTRL module (see examples/ folder)

To make a physical patch bay: Attach tip connector of 3.5mm socket to each GPIO pin. Short with mono 3.5mm patch leads. Done!

GPIO0 & 1 are skipped as I intend to use the UART to link multiple Picos to one "master". Really any expansion needs doing over i2c or SPI. This is all just a quick dirty example. They can be added into the lists for 28x total physical sockets.

**What's happening on the Pico:** ALL GPIO PINS are set as input with pull-up, defaulting high in the code. GPIO Pins 2 thru 14 are switched to outputs one at a time and pulled low and then GPIO Pins 15 thru 27 are sequentially scanned for any now pulled low (linked). Their state is compared against and a statematrix dictionary object - if the state changes, the relevant MIDI CC codes are sent to reflect the change - then the statematrix updated to store the latest current (inverted) state. The current GPIO Output is then switched back to a pulled-up input before moving on to the next output pin. 

This prevents any pair of pins being set as an Output simultaneously, as a short between two pins set as Outputs would damage the Pico without additional hardware protection. This scanning process runs in a continuous loop. A full sweep of the matrix takes around 80ms iirc so that's your rough max latency.

![PiPico GPIO Pins](https://cdn-learn.adafruit.com/assets/assets/000/099/339/large1024/raspberry_pi_Pico-R3-Pinout-narrow.png)

If running multiple Picos as the code stands, change MIDI channel in code at line 17 so each Pico outputs on it's own channel (or rewrite the code to remap the ccs from a higher start point to not conflict with an existing Pico on same MIDI Channel), but **don't link across Picos because that isn't handled** and will make a mess (input-bearing Pico will think an input is linked to EVERY output on itself), especially as you now have a situation where an output per Pico may be active *simultaneously*, which could cause Physical Damage if linked **(so definitely don't link outputs of one Pico to outputs of another Pico or you'll risk popping them both)**

## Usage Example

![Image of PiPico with screenshot of VCV Rack Example](https://github.com/PatchworkBoy/VCVRack_CableControl/raw/main/media/demo.jpg)

* Grab Pack-Tau (https://github.com/stoermelder/vcvrack-packtau/releases) and manually install.
* Copy code.py & lib/ folder to Pi Pico running CircuitPython
* Open examples/t7-ctrl_example.vcv in VCVRack (requires Pack-Tau, BogAudio, Instruo & VCV Fundamentals)
* Short any of GPIO2-13 to GPIO15-26. **Be careful NOT to inadvertently short to RUN or GND, which will crash the Pico (no damage) - unplug / replug to restart it**. MIDI CC13 & 26 (GPIO14 & 27) aren't mapped in the example json file. 12x output, 12x input. Add them for 13x of each.

To load a custom map, click ports on your modules and watch the T7-Assistant module. Note the moduleId and portId (you can highlight and copy them from the T7-Assistant display) 

![T7-ASSISTANT](https://github.com/PatchworkBoy/VCVRack_CableControl/raw/main/media/t7-assistant.jpg)

Open examples/t7-ctrl_blank.json in a text editor... add/paste the relevant moduleId and PortId (pay attention to the portType in the JSON file - output portIds for output port types, input portIds for input port types) to the CC to be mapped to that port. This maps to the equivalent GPIO pin [CC + 1].

![codeblock](https://github.com/PatchworkBoy/VCVRack_CableControl/raw/main/media/codeblock.jpg)

![completed codeblock](https://github.com/PatchworkBoy/VCVRack_CableControl/raw/main/media/completedblock.jpg)

Once you've got that done for all the ports in the file (or removed unmapped entries), select all > copy. Right click T7-Ctrl module > Paste JSON Mapping. (This gets stored in the VCVRack file on save)

![Context Menu of T7-CTRL](https://github.com/PatchworkBoy/VCVRack_CableControl/raw/main/media/copy_paste_json.jpg)

**NOTE: T7-MIDI module MUST be adjacent to the right of the T7-CTRL module for MIDI commands to be transmitted from T7-MIDI to T7-CTRL. Select the PiPico midi device in T7-MIDI. For multiple Picos, just add more T7-MIDI modules to the right. All the mapping goes into the single T7-CTRL instance**

Now start shorting your Pins (or if you've added sockets etc, patching your cables) and watch cables appear onscreen between the mapped ports, and disappear when you unshort.

### References: 
* Initial software concept at https://community.vcvrack.com/t/module-to-connect-disconnect-rack-cables-over-midi/9101 - thanks to the fabulous [Stoermelder](https://github.com/stoermelder), [Ligant](https://community.vcvrack.com/u/ligant/summary), and [MudJakub (MidiLar)](https://community.vcvrack.com/u/mudjakub/summary) o'er at VCV communities forum.
* [MudJakub (MidiLar)](https://community.vcvrack.com/u/mudjakub/summary) - Excellent implementation whose video got me investigating - https://midilar-controller.webnode.sk/midilar-knots/
