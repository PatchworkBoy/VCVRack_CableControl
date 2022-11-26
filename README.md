# VCVRack_CableControl
A virtual cable controller for VCVRack which requires nothing more than a Raspberry Pi Pico. Written in CircuitPython

Use with Stoermelder's VCVRack Pack-Tau T7 modules to map MIDI CC to module ports in VCVRack: https://github.com/stoermelder/vcvrack-packtau

* GPIO2-14 are stackable outputs mapped to MIDI CC1-13 Ch1
* GPIO15-27 are non-stackable inputs mapped to MIDI CC14-26 Ch1
* When outputs are shorted to inputs, the matching pair of MIDI CC transmit
level 127.
* When disconnected, the matching pair transmit level 0.

Attach tip connector of 3.5mm socket to each GPIO pin. Short with mono 3.5mm patch leads. Done!
