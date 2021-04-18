# Load Matplotlib and data wrangling libraries.
import matplotlib.pyplot as plt
import numpy as np

# Create a grouped bar chart, with job as the x-axis
# and gender as the variable we're grouping on so there
# are two bars per job.
fig, ax = plt.subplots(figsize=(12, 8))


# Define bar width. We need this to offset the second bar.
bar_width = 0.3

b1 = ax.barh([0.2, 0.2+1.01*bar_width,0.2+2.02*bar_width], [50,40,30],left=[10,20,30],height=bar_width)

# Same thing, but offset the x.
b2 = ax.barh([2.1,2.1+1.01*bar_width], [70,80],left=[10,20],height=bar_width )


ax.set_yticks([0.45,2.2])
ax.set_yticklabels(['2005','2015'])
ax.tick_params(bottom=False, left=False)
ax.set_axisbelow(True)
ax.xaxis.grid(True, color='#EEEEEE')
ax.yaxis.grid(False)
ax.set_xlim(0, 100)


fig.tight_layout()
# For each bar in the chart, add a text label.
for bar in b1.patches:
  # The text annotation for each bar should be its height.
  bar_value = bar.get_height()
  # Format the text with commas to separate thousands. You can do
  # any type of formatting here though.
  text = f'{bar_value:,}'
  # This will give the middle of each bar on the x-axis.
  text_x = bar.get_x() + bar.get_width() / 2
  # get_y() is where the bar starts so we add the height to it.
  text_y = bar.get_y() + bar_value/2
  # If we want the text to be the same color as the bar, we can
  # get the color like so:
  bar_color = bar.get_facecolor()
  # If you want a consistent color, you can just set it as a constant, e.g. #222222
  ax.text(text_x, text_y, text, ha='center', va='bottom', color='white',
          size=12)

plt.show()
