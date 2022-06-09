import rtmidi

class MidiSubscriber():
    def __init__(self, pianoName):
        self.midiin = rtmidi.RtMidiIn()
        self.midiPort = self.__getPort(pianoName)
        self.maxSeqenceSize = 1000
        self.noteSequence = []
        self.currentChord = {}
        self.sequenceSubscriptions = []
        self.chordSubscriptions = []

        print("Opening port", self.midiPort)
        self.midiin.openPort(self.midiPort)

    def registerSequence(self, sequence, callback):
        self.sequenceSubscriptions.append((sequence, callback))

    def printSequence(self):
        while True:
            m = self.midiin.getMessage(250) # some timeout in ms
            if m:
                if m.isNoteOn():
                    print("'", m.getMidiNoteName(m.getNoteNumber()), "', ", end='', sep='', flush=True)

    def registerChord(self, chord, callback):
        self.chordSubscriptions.append((chord, callback))

    def run(self):
        while True:
            m = self.midiin.getMessage(250) # some timeout in ms
            if m:
                self.__printMessage(m)
                self.__saveMessage(m)

    def __getPort(self, pianoName):
        ports = range(self.midiin.getPortCount())
        if ports:
            pianoPort = None
            for i in ports:
                portName = self.midiin.getPortName(i)
                print(portName)
                if pianoName in portName:
                    pianoPort = i

            if pianoPort is None:
                raise Exception("Piano not found")
            return pianoPort
        else:
            raise Exception("NO MIDI INPUT PORTS!")

    def __saveMessage(self, m):
        noteName = m.getMidiNoteName(m.getNoteNumber())
        if m.isNoteOn():
            self.__updateChord(noteName, 1)
            self.__addToSequence(noteName)
        if m.isNoteOff():
            self.__updateChord(noteName, 0)

        self.__checkSequenceSubscriptions()
        self.__checkChordSubscriptions()

    def __updateChord(self, noteName, state):
        self.currentChord[noteName] = state

    def __addToSequence(self, noteName):
        if (len(self.noteSequence) == self.maxSeqenceSize):
            self.noteSequence.pop(0)
        self.noteSequence.append(noteName)

    def __checkChordSubscriptions(self):
        for chord, callback in self.chordSubscriptions:
            if (all(noteName in self.currentChord and self.currentChord[noteName] == 1 for noteName in chord)):
                callback()

    def __checkSequenceSubscriptions(self):
        for sequence, callback in self.sequenceSubscriptions:
            if len(sequence) > len(self.noteSequence):
                continue

            startIndex = len(self.noteSequence) - len(sequence)
            if (all(self.noteSequence[startIndex + i] == sequence[i] for i in range(len(sequence)))):
                self.__addToSequence(None) # clear out the sequence so it doesn't trigger on the OFFs
                callback()
        
    def __printMessage(self, midi):
        if midi.isNoteOn():
            print('ON: ', midi.getMidiNoteName(midi.getNoteNumber()), midi.getVelocity())
        elif midi.isNoteOff():
            print('OFF:', midi.getMidiNoteName(midi.getNoteNumber()))
        elif midi.isController():
            print('CONTROLLER', midi.getControllerNumber(), midi.getControllerValue())

