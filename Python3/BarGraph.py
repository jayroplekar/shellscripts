# Load Matplotlib and data wrangling libraries.
import matplotlib.pyplot as plt
import numpy as np

# Create a grouped bar chart, with job as the x-axis
# and gender as the variable we're grouping on so there
# are two bars per job.
fig, ax = plt.subplots(figsize=(12, 8))

Labels_2005=['labl1','labl2','labl3']
Starts_2005=[20,50,30]
Ends_2005=[40,90,60]

Labels_2015=['xabl1','xabl2','xabl3','xabl4']
Starts_2015=[20,50,30,55]
Ends_2015=[40,90,60,75]

# Define bar width. We need this to offset the second bar.
bar_width = 0.15
Yticks=[]


def Average(lst):
    return sum(lst) / len(lst)
  
def barlocations(datum,LabelList):
  global bar_width
  num_bars=len(LabelList)
  barLocs=[]
  for i in range(num_bars):
    barLocs.append(datum+i*1.02*bar_width)
  return barLocs  

def PlaceLabels(bc, barLocs, Labels):
  # For each bar in the chart, add a text label.
  for bar in bc.patches:
    # The text annotation for each bar should be its height.
    bar_value = bar.get_height()
    # Format the text with commas to separate thousands. You can do
    # any type of formatting here though.
    #text = f'{bar_value:,}'
    #text=bar.label
    # This will give the middle of each bar on the x-axis.
    text_x = bar.get_x() + bar.get_width() / 2
    # get_y() is where the bar starts so we add the height to it.
    text_y = bar.get_y() + bar_value/2.0
    #Let's find the right label based on where we originally placed this bar
    text=Labels[barLocs.index(text_y)]
    # If we want the text to be the same color as the bar, we can
    # get the color like so:
    bar_color = bar.get_facecolor()
    # If you want a consistent color, you can just set it as a constant, e.g. #222222
    ax.text(text_x, text_y, text, ha='center', va='center', color='white', size=18)
    
barLocs=barlocations(0.1, Labels_2005)
Yticks.append(Average(barLocs))
Widths=[m - n for m,n in zip(Ends_2005,Starts_2005)]
b1 = ax.barh(barLocs,Widths ,left=Starts_2005,height=bar_width)
PlaceLabels(b1,barLocs,Labels_2005)

# Same thing, but offset the x.
barLocs=barlocations(1.0, Labels_2015)
Yticks.append(Average(barLocs))
Widths=[m - n for m,n in zip(Ends_2015,Starts_2015)]
b2 = ax.barh(barLocs, Widths,left=Starts_2015,height=bar_width )
PlaceLabels(b2,barLocs,Labels_2015)

ax.set_yticks(Yticks)
ax.set_yticklabels(['2005','2015'],size=16)
ax.tick_params(bottom=False, left=False,size=16)
ax.set_axisbelow(True)
ax.set_xlabel('Power (kW)', fontsize=16)
ax.tick_params(axis='x', which='major', labelsize=14)
ax.xaxis.grid(True, color='#EEEEEE')
ax.yaxis.grid(False)
ax.set_xlim(0, max(Ends_2005+Ends_2015))


fig.tight_layout()


plt.show()
