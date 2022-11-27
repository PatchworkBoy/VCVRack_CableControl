# For Raspberry Pi Pico...
# GPIO2-14 are stackable outputs mapped to MIDI CC1-13 Ch1
# GPIO15-27 are non-stackable inputs mapped to MIDI CC14-26 Ch1
# When outputs are shorted to inputs, the matching pair of MIDI CC transmit
# level 127. When disconnected, transmits level 0.
# Use with Stoermelder's Pack-Tau T7 modules to map to module ports in VCVRack
# Attach tip connector of TRS socket to each GPIO pin. Short with mono 3.5mm patch leads!

import board
import time
import usb_midi
import adafruit_midi
from adafruit_midi.control_change import ControlChange
from digitalio import DigitalInOut, Direction, Pull

midi = adafruit_midi.MIDI(
    midi_in=usb_midi.ports[0], in_channel=0, midi_out=usb_midi.ports[1], out_channel=0
)

# Convert channel numbers at the presentation layer to the ones musicians use
print("Default output channel:", midi.out_channel + 1)
print("Listening on input channel:", midi.in_channel + 1)

print("Monitoring matrix for connections...")
outpins = (board.GP2, board.GP3, board.GP4, board.GP5, board.GP6, board.GP7, board.GP8,
           board.GP9, board.GP10, board.GP11, board.GP12, board.GP13, board.GP14)
out_pin_start = 0
out_pin_count = len(outpins)
inpins = (board.GP15, board.GP16, board.GP17, board.GP18, board.GP19, board.GP20,
          board.GP21, board.GP22, board.GP23, board.GP24, board.GP25, board.GP26,
          board.GP27)
in_pin_start = 0
in_pin_count = len(inpins)

statematrix = {}
outswitches = []
inswitches = []

def build_state_matrix():
    global in_pin_start
    global in_pin_count
    global out_pin_start
    global out_pin_count
    global statematrix
    x = 0
    while x < out_pin_count:
        y = in_pin_start
        row = {}
        while y < in_pin_count:
            z = f"{y}"
            row[z] = 0
            y += 1
        m = f"{x}"
        statematrix[m] = row
        x += 1

def build_gpio_matrix():
    global in_pin_start
    global in_pin_count
    global out_pin_start
    global out_pin_count
    global outswitches
    global inswitches
    x = out_pin_start
    while x < out_pin_count:
        outswitch = DigitalInOut(outpins[x])
        outswitch.direction = Direction.INPUT
        outswitch.pull = Pull.UP
        outswitches.append(outswitch)
        x += 1
    y = in_pin_start
    while y < in_pin_count:
        inswitch = DigitalInOut(inpins[y])
        inswitch.direction = Direction.INPUT
        inswitch.pull = Pull.UP
        inswitches.append(inswitch)
        y += 1

def do_MIDI(outpin, inpin, state):
    global midi
    out_cc = outpin + 1
    in_cc = inpin + out_pin_count + 1
    midi.send(ControlChange(out_cc, state))
    time.sleep(0.1)
    midi.send(ControlChange(in_cc, state))
    if state == 127:
        status = "Connected"
    else:
        status = "Disconnected"
    print(f"cc{out_cc} (output) to cc{in_cc} (input) - {status}")

def checkpin(outpin):
    global in_pin_start
    global in_pin_count
    global statematrix
    global outswitches
    global inswitches
    switch = outswitches[outpin]
    switch.direction = Direction.OUTPUT
    switch.value = 0
    y = in_pin_start
    row = {}
    curr_row = statematrix[f"{outpin}"]
    while y < in_pin_count:
        inp = inswitches[y]
        val = inp.value
        z = f"{y}"
        if val == 0:
            row[z] = 1
        else:
            row[z] = 0
        if row[z] != curr_row[z]:
            if val == 0:
                state = 127
            else:
                state = 0
            do_MIDI(outpin, y, state)
        y += 1
    statematrix[f"{outpin}"] = row
    switch.direction = Direction.INPUT
    switch.pull = Pull.UP

build_state_matrix()
build_gpio_matrix()

y = out_pin_start
start_time = time.monotonic_ns()
while y < out_pin_count:
    lastrow = time.monotonic_ns()
    checkpin(y)
    if y == out_pin_count - 1:
        y = out_pin_start
        # now = time.monotonic_ns()
        # run_time = now - start_time
        # print(f"completed matrix {run_time}ms")
        # print(statematrix)
        # start_time = time.monotonic()
    else:
        y += 1
        # now = time.monotonic()
        # run_time = now - lastrow
        # print(f"row time {run_time}ms")
