from buhoor import get_composition
from parts import Jumla

test = Jumla('وَدَارٌ لَهَا بِلرَقمَتَينِ كَأَنَّهَا')
beats = ''.join([str(i) for i in test.tone])
print(get_composition(beats))