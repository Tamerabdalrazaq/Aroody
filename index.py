from analysis import get_composition
from parts import Jumla
from tester import test

# test = Jumla('ذُو العَقلِ يَشقَى فِي النَعيمِ بِعَقلِهِي')
test()
jumla = Jumla("عَذْلُ العَواذِلِ حَوْلَ قَلبي التائِهِي")
print(jumla.tone)
print(get_composition(jumla.tone))
