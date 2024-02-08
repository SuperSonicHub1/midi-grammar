"""
TODO: Connect to clock
"""

from fractions import Fraction

from midi_grammar.grammar import Terminal
from midi_grammar.midi_grammar import MidiGrammar, note
from midi_grammar.util import open_midi_output

def simpler(num_notes: int = 24, start: int = 36):
    """`start` by default is C2 (in Ableton)"""
    return range(start, start + num_notes)

grammar = MidiGrammar(
    *(note(simpler(), length=Fraction(1, 8)) for _ in range(32)),
    bpm=170,
)

out = open_midi_output()
while 1:
    for msg in grammar.generate().play():
        print(msg)
        out.send(msg) 
 