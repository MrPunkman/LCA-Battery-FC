import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import textwrap


## Import Data
# get path
path = r"C:\Users\Mein\tubCloud\00_Uni\01_Paper-Projekt-LCA-PEMFC\04-Plots\\"

df1 = pd.read_excel(path+'Mappe1.xlsx', index_col=0)
df1 = df1.fillna(0)

#### prepare data for bar chart
labels = df1.columns.values
print(labels)
ledgend = df1.index.values

# ledgend = ['Recycling','Production', 'Use Phase']

valuestoPlot = np.asarray(df1)

print(valuestoPlot)
valuesPlotScaled = valuestoPlot
width = 0.3
data_shape = np.shape(valuesPlotScaled)
print(valuesPlotScaled)
# Take negative and positive data apart and cumulate
def get_cumulated_array(data, **kwargs):
    cum = data.clip(**kwargs)
    cum = np.cumsum(cum, axis=0)
    d = np.zeros(np.shape(data))
    d[1:] = cum[:-1]
    return d  

cumulated_data = get_cumulated_array(valuesPlotScaled, min=0)
cumulated_data_neg = get_cumulated_array(valuesPlotScaled, max=0)

# Re-merge negative and positive data.
row_mask = (valuesPlotScaled<0)
cumulated_data[row_mask] = cumulated_data_neg[row_mask]
data_stack = cumulated_data
print(data_stack)

#### https://medium.com/dunder-data/automatically-wrap-graph-labels-in-matplotlib-and-seaborn-a48740bc9ce
# text wrap for legend 
def wrap_labels(ax, width, break_long_words=False):
    labels = []
    for label in ax.get_xticklabels():
        text = label.get_text()
        labels.append(textwrap.fill(text, width=width,
                      break_long_words=break_long_words))
    ax.set_xticklabels(labels, rotation=0)

# plot bar
colors = plt.cm.tab20(np.linspace(0,1,len(ledgend)))  # color
fig, barPlot = plt.subplots()
for i in range(valuesPlotScaled.shape[0]):
  barPlot.bar(labels, valuesPlotScaled[i], bottom=data_stack[i], color = colors[i]) # bottom = np.sum(valuesPlotScaled[:i], axis = 0)

totals = sum((valuestoPlot))
# for i, val in enumerate(totals):
#     barPlot.text( i, val+0.1, str(round(val)), ha='center')

# for i, bar in enumerate(barPlot.containers):
#     height = bar.get_height()
#     barPlot.annotate(str(round(totals[i])), xy=(bar.get_x() + bar.get_width() / 2, height),
#                 xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')


barPlot.set_ylabel('GWP 100 in kg CO$_2$ eq.')
# upDownPlot[1].label_outer()
barPlot.set_xticklabels(barPlot.get_xticklabels(), rotation=45)
# wrap_labels(upDownPlot[1], 5)
#text = barPlot.text(-0.2,1.05, "", transform=barPlot.transAxes)
#leg = barPlot.legend(ledgend, bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
barPlot.set_xticklabels(labels)
leg = barPlot.legend(ledgend, bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
text = barPlot.text(-0.2,1.05, "", transform=barPlot.transAxes)
#barPlot.legend(ledgend, fancybox=True, framealpha=0.5, ncol= 3)
# barPlot.grid()
# plt.rcParams['figure.figsize'] = [4, 4]
#plt.savefig(path + 'RecycledBar.pdf', format = 'pdf')
plt.savefig("myImagePDF.pdf", format="pdf", bbox_extra_artists=(leg, text), bbox_inches='tight')
plt.show()

