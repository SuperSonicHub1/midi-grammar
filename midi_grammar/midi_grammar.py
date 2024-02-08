"""
TODO: Support "chords"
TODO: Support rests
TODO: Support text notation fo notes and chords
TODO: Add quantization
"""

from collections.abc import Iterable
from dataclasses import dataclass
from itertools import chain
from fractions import Fraction

from mido import Message, MidiFile, MidiTrack, bpm2tempo, MetaMessage

from .grammar import Node, Set, Grammar, Terminal

@dataclass
class Note:
    note: Node[int]
    velocity: Node[int]
    length: Node[Fraction]

def note(note: int | set[int] | Iterable[int], velocity: int = 64, length: Fraction = Fraction(1, 4)):
    if isinstance(note, set):
        note_node = Set(note)
    elif isinstance(note, Iterable):
        note_node = Set(set(note))
    else:
        note_node = Terminal(note)

    return Terminal(
        Note(
            note_node,
            Terminal(velocity),
            Terminal(length),
        )
    )

@dataclass
class MidiGrammar:
    grammar: Grammar[Note]
    ticks_per_beat: int
    bpm: int

    def __init__(self, *symbols: Node[Note], ticks_per_beat: int = 480, bpm: float = 120.) -> None:
        self.grammar = Grammar(symbols)
        self.ticks_per_beat = ticks_per_beat
        self.bpm = bpm

    def generate(self) -> MidiFile:
        """
        TODO: Allow user to set their own time sig
        """

        mid = MidiFile(ticks_per_beat=self.ticks_per_beat)
        track = MidiTrack()
        mid.tracks.append(track)
        # TODO: Allow user to set time sig
        track.append(MetaMessage('set_tempo', tempo=bpm2tempo(self.bpm)))        

        for note in self.grammar.generate():
            midi_note = note.note()
            velocity = note.velocity()
            length = note.length()
            ticks = int(length * self.ticks_per_beat * 4)

            track.append(Message('note_on', note=midi_note, velocity=velocity, time=0))
            track.append(Message('note_off', note=midi_note, velocity=velocity, time=ticks))
        
        return mid
