from motionDetect import df
from bokeh.plotting import show,output_file, figure
from bokeh.models import HoverTool
from bokeh.models import ColumnDataSource

df["StartString"] = df["Start"].dt.strftime("%d/%m/%Y %H:%M:%S")
df["EndString"] = df["End"].dt.strftime("%d/%m/%Y %H:%M:%S")

cds = ColumnDataSource(df)

p=figure(x_axis_type="datetime", height=250, width=600, sizing_mode='scale_width',title="Motion Graph")
p.yaxis.minor_tick_line_color = None
p.ygrid[0].ticker.desired_num_ticks=1

hover = HoverTool(tooltips=[("Start","@StartString"),("End", "@EndString")])
p.add_tools(hover)

q=p.quad(left="Start", right="End", bottom=0, top=1, color = "green",source=cds)
# p.yaxis.visible = False  -- to remove the 0 and 1 in the y axis
output_file("motionGraph.html")
show(p)