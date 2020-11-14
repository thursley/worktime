import ui
import datetime as dt

def log_in(sender):
    sender.title = 'clicked'

def log_out(sender):
    label_time = sender.superview['label_time']
    time = dt.datetime.now()
    label_time.text = str(time)
    
with open('file.txt', 'w') as file:
	file.write('hello')


v = ui.load_view()
v.present('sheet')

