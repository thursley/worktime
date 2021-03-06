import ui, appex
import datetime as dt
import os
import json5
import pathlib

json_file: str = f'{pathlib.Path(__file__).parent.absolute()}/times.json5'


def get_today() -> str:
  return dt.datetime.now().strftime("%Y-%m-%d")


def get_time() -> str:
  return dt.datetime.now().strftime('%H:%M:%S')


def to_datetime(s: str) -> dt.datetime:
  return dt.datetime.strptime(s, '%H:%M:%S')


def get_times():
  with open(json_file, 'r') as f:
    times = json5.load(f)
  today = get_today()
  if today not in times:
    times[today] = []
  return times


def get_worked_today():
  times_today = get_times()[get_today()]
  time_worked = dt.timedelta(0)
  for range in times_today:
    if 'out' in range:
      end = to_datetime(range['out'])
      start = to_datetime(range['in'])
      time_worked += end - start
    elif range == times_today[-1]:
      start = to_datetime(range['in'])
      time_worked += to_datetime(get_time())  - start

  return time_worked


def update_json(times):
  with open(json_file, 'w') as file:
    json5.dump(times, file)
    
    
def update_time(sender):
  sender.superview['label_time'].text = str(get_worked_today())
  
  
def log_in(sender):
  times = get_times()
  today = get_today()
  if len(times[today]) > 0 and 'out' not in times[today][-1]:
    raise Exception('last entry has no "out"')
  times[today].append({'in': get_time()})
  update_json(times)
  update_time(sender)


def log_out(sender):
  times = get_times()
  times[get_today()][-1]['out']  = get_time()
  update_json(times)
  update_time(sender)
 

if not os.path.isfile(json_file):
  times = {}
  with open(json_file, 'w') as file:
    json5.dump(times, file)

v = ui.load_view()
# v.present('sheet')
appex.set_widget_view(v)

