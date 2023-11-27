from analysis import analyze_tone
from parts import Jumla
from tester import test

test()
jumla = Jumla("لئِن مُنيت بنا عن غِبِّ مَعرَكَةٍ")
print(jumla.tone)
determenistic, statistic = analyze_tone(jumla.tone)
print(determenistic)
print(statistic)
print(max(statistic, key=statistic.get))
