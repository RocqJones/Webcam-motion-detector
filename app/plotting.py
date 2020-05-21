"""
    Requirements.
    $ pip3 install bokeh
"""
from MotionDetector import data_frames
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

# ColumnDataSource - standardized way of providing data to bokeh plot
data_frames["Start_string"] = data_frames["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
data_frames["End_string"] = data_frames["End"].dt.strftime("%Y-%m-%d %H:%M:%S")

cds = ColumnDataSource(data_frames)

p = figure(x_axis_type='datetime', height=100, width=500, title="Motion Graph", sizing_mode='scale_width')
p.yaxis.minor_tick_line_color = None

# import hover and implement capabilities here and later add 'ColumnDataSource'
hover=HoverTool(tooltips=[("Start", "@Start_string"),("End", "@End_string")])
p.add_tools(hover)
 
q = p.quad(left="Start",right="End",bottom=0,top=1,color="green", source=cds)

output_file("Graph.html")
show(p)