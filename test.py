from jatmuzik import *

tick_duration = 0.2
# create tracks

# track 1: sine
track_1 = Track(1, 4, tick_duration, name='Track 1 - Sine')

# track 2: filtered square #1
track_2 = Track(8, 17, tick_duration, name='Track 2 - Square 1')

# track 3: filtered square #2
track_3 = Track(6, 27, tick_duration, name='Track 3 - Square 2')

# track 4: saw (no VCA)
track_4 = Track(3, 22, tick_duration, name='Track 4 - Saw')


print('Loading track 1')
load_file('./songs/testsong/track1.json', track_1)
print('Loading track 2')
load_file('./songs/testsong/track2.json', track_2)
print('Loading track 3')
load_file('./songs/testsong/track3.json', track_3)
print('Loading track 4')
load_file('./songs/testsong/track4.json', track_4)

print(f'Loaded tracks. Tick counts: {track_1.ticks()} {track_2.ticks()} {track_3.ticks()} {track_4.ticks()}')
