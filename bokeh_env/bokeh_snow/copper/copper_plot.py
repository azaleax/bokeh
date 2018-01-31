import pandas as pd
import numpy as np
from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool
from scipy import interpolate
import calendar


def to_timestamp_arr(dt_arr):
  ts_arr = [0] * len(dt_arr)

  for i in range(0, len(dt_arr)):
    ts_arr[i] = calendar.timegm((dt_arr[i]).timetuple())
  
  return ts_arr

def smooth_function(x, y):
  tck = interpolate.splrep(x_ts, y, s = 50)
  y_smooth = interpolate.splev(x_ts, tck, der = 0)

  return y_smooth


headers = ['date','snow_depth']
df = pd.read_csv('SNWD__value_415.csv', names = headers, comment = '#', header=0)

x = pd.to_datetime(df['date'])
y = df['snow_depth']

x_ts = to_timestamp_arr(x)

y_smooth = smooth_function(x_ts, y)

output_file('copper_plot.html')

hover = HoverTool(tooltips = [('Date', '@x{%F}'),
                              ('Depth', '@y')],
                  formatters = {'x' : 'datetime'}, 
                  mode = 'vline',
                  names = ['y'])

plot = figure(title = 'Copper Sensor Snow Depth Reading',
              x_axis_type ='datetime',
              x_axis_label='date',
              y_axis_label='snow depth',
              tools = [hover],
              plot_width = 800,
              plot_height = 500)

y_scatter = y

plot.line(x, y_smooth, line_alpha = 0.5, line_width = 2)
plot.line(x, y, line_alpha = 0, name = 'y')
plot.circle(x, y_scatter)

show(plot)