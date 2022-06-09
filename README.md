# py-midi-subscriber
A simple python module that allows you run code when a midi device sends certain midi data.

You can configure the library with note sequences or chords. Then, when the library receives those sequences or chords,
it notifies your subsribers so that you can run custom code.

## Installation
1. Download midiSubscriber.py directly to your source folder
2. `pip install rtmidi`
3. In your source file: `from midiSubscriber import MidiSubscriber`

## Usage

### Setup
First, plug in your midi device. Then from the linux console, run `aseqdump -l` to get a list of sound devices (works on raspberry pi 0).
Copy the client name of your midi device from this list.

```bash
$: aseqdump -l
 Port    Client name                      Port name
  0:0    System                           Timer
  0:1    System                           Announce
 14:0    Midi Through                     Midi Through Port-0
 20:0    Portable Grand                   Portable Grand MIDI 1
```

Call the MidiSubscriber constructor with that client name:
```py
midi = MidiSubscriber(<client-name>)
```

### Registering Sequences
A sequence is an ordered list of notes played one after the other. Use the `registerSequence` method to subscribe to a
specific sequence. Provide a list of notes (in order), as well as a callback method to run when the sequence of notes is played:

```py
wonkaSeq = ['D3', 'C#3', 'D3', 'C#3', 'D3', 'D3', 'C#3', 'D3', 'E3', 'F#3', 'E3', 'F#3', 'G3', 'A3', 'G#3', 'A3', 'G#3', 'A3']
midi.registerSequence(wonkaSeq, lambda: print("Wonka sequence played"))
```

Instead of hard coding all of the notes, you can use the `printSequence` method to print the notes to the console as you play
them on the midi device. Then you can copy and paste those values into your code.

### Registering Chords
A chord is an unordered list of any number of notes held at the same time. Use the `registerChord` method to subscribe to a
specific chord. Provide a list of notes (in any order), as well as a callback method to run when the chord is played:

```py
midi.registerChord(['C3', 'E3', 'G3'], lambda: print("C chord played"))
```

### Start Listening for Events
After registering subscriptions to all your sequences and chords, start listening for events by calling the `run` method.

## Full Example

```py
from midiSubscriber import MidiSubscriber

PIANO_NAME = "Portable Grand"

def handleCallback(id):
    print(id, "played")

wonkaSeq = ['D3', 'C#3', 'D3', 'C#3', 'D3', 'D3', 'C#3', 'D3', 'E3', 'F#3', 'E3', 'F#3', 'G3', 'A3', 'G#3', 'A3', 'G#3', 'A3']
furElise = ['E4', 'D#4', 'E4', 'D#4', 'E4', 'B3', 'D4', 'C4', 'A3', 'A1', 'E2', 'A2', 'C3', 'E3', 'A3', 'B3', 'E1', 'E2', 'G#2', 'E3', 'G#3', 'B3', 'C4', 'A1', 'E2', 'A2', 'E3', 'E4', 'D#4', 'E4', 'D#4', 'E4', 'B3', 'D4',
 'C4', 'A1', 'A3', 'E2', 'A2', 'C3', 'E3', 'A3', 'B3', 'E1', 'E2', 'G#2', 'E3', 'C4', 'B3', 'A1', 'A3', 'E2', 'A2']
nbc = ['G3', 'E4', 'C4']

midi = MidiSubscriber(PIANO_NAME)

midi.registerChord(['C3', 'E3', 'G3'], lambda: handleCallback("c-chord"))
midi.registerChord(['F3', 'A3', 'C3'], lambda: handleCallback("f-chord"))
midi.registerChord(['D3', 'G3', 'B3'], lambda: handleCallback("g-chord"))
midi.registerChord(['C3', 'A3', 'E3'], lambda: handleCallback("am-chord"))
midi.registerChord(['E3', 'G3', 'C4'], lambda: handleCallback("cfirst-chord"))
midi.registerSequence(['E4', 'G4', 'C5'], lambda: handleCallback("seq-egc"))
midi.registerSequence(['C5', 'G4', 'E4'], lambda: handleCallback("seq-cge"))
midi.registerSequence(['E4', 'C5', 'G4'], lambda: handleCallback("seq-ecg"))
midi.registerSequence(wonkaSeq, lambda: handleCallback("wonka"))
midi.registerSequence(nbc, lambda: handleCallback("nbc"))
midi.registerSequence(furElise, lambda: handleCallback("furElise"))
#midi.printSequence() // Uncomment to print the notes you play to the console.
midi.run()
```

## What's Not Supported
This is meant to be a very simple library, so for simplicity's sake the following are not supported:
* sequences of chords
* flats (I recommend using the `printSequence` helper to ensure that your notes match what your device outputs)
* octave-agnostic chords or sequences
* velocity of notes

However, PRs are always welcome.

