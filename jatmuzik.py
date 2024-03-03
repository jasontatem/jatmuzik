import time
import atexit
import random
import threading
import dac
import pin
import logging
import json
import os


logging.basicConfig(filename='./jatmuzik.log', level=logging.DEBUG, format='%(asctime)s;%(message)s', datefmt='%Y%m%d%H%M%S')
valid_e_types = ['NoOp', 'PinOn', 'PinOff', 'ToneSet', 'KeyPress']



def cleanup():
    dac.cleanup()
    pin.cleanup()


atexit.register(cleanup)


tracks = list()


def play_all():
    threads = list()
    for t in tracks:
        x = threading.Thread(target=play_track, args=(t,))
        x.start()
        threads.append(x)
    for x in threads:
        x.join()


def play_track(track):
    track.play()


class Track():
    def __init__(self, dac_target, pin_target, tick_duration, name=None):
        self.dac_target = dac_target
        self.pin_target = pin_target
        self.tick_duration = tick_duration
        if name is None:
            self.name = f'Track {len(tracks) + 1}'
        else:
            self.name = name
        self.events = list()
        tracks.append(self)
        logging.debug(f'Created track {self.name} with dac {self.dac_target} and pin {self.pin_target}')

    def play(self, start_index=0, end_index=None):
        logging.debug(f'Playing track {self.name} start {start_index} end {end_index}')
        for event in self.events[start_index:end_index]:
            if event.e_type == 'NoOp':
                time.sleep(self.tick_duration * event.ticks)
            elif event.e_type == 'PinOn':
                pin.pin_on(self.pin_target)
                time.sleep(self.tick_duration * event.ticks)
            elif event.e_type == 'PinOff':
                pin.pin_off(self.pin_target)
                time.sleep(self.tick_duration * event.ticks)
            elif event.e_type == 'ToneSet':
                dac.send_command(self.dac_target, event.tone)
                time.sleep(self.tick_duration * event.ticks)
            elif event.e_type == 'KeyPress':
                dac.send_command(self.dac_target, event.tone)
                pin.pin_on(self.pin_target)
                time.sleep(self.tick_duration * event.ticks)
                pin.pin_off(self.pin_target)

    def ticks(self):
        return sum([event.ticks for event in self.events])



class Event():
    def __init__(self, e_type='NoOp', ticks=1, tone=128):
        if e_type not in valid_e_types:
            raise ValueError(f'Supplied e_type {e_type} not in {valid_e_types}')
        else:
            self.e_type = e_type
            self.ticks = ticks
            if type(tone) == int:
                self.tone = tone
            else:
                raise ValueError(f'Supplied tone value {tone} is not an int')


def load_file(filename, track):
    with open(filename, 'r') as f:
        track_data = json.loads(f.read())
    for event in track_data:
        track.events.append(Event(e_type=event['type'], tone=event['tone'], ticks=event['ticks']))
    logging.debug(f'Loaded {len(track_data)} events from {filename} into track {track.name}, total ticks {sum([event["ticks"] for event in track_data])}')


def write_track(track, filename):
    track_data = list()
    for event in track.events:
        track_data.append({
            'type': event.e_type,
            'tone': event.tone,
            'ticks': event.ticks
        })
    with open(filename, 'w') as f:
        f.write(json.dumps(track_data))


def write_all_tracks(path):
    for t in tracks:
        write_track(t, os.path.join(path, f'{t.name}.json'))
