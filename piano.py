from fractions import Fraction

from midi_grammar.grammar import Terminal
from midi_grammar.midi_grammar import MidiGrammar, note
from midi_grammar.util import open_midi_output

# C major in the fourth octave
c_major = {60, 62, 64, 65, 67, 69, 71, 72}

grammar = MidiGrammar(
    # third octave
    *(note({n - 12 for n in c_major}, length=Fraction(1, 1)) for _ in range(32)),
    bpm=170,
)

out = open_midi_output()
while 1:
    for msg in grammar.generate().play():
        print(msg)
        out.send(msg) 
 