
import seaborn as sns
import matplotlib.pyplot as plt

def plot_corrGraph(spotData, forwardData, ymin, ymax):
    #setting seaborn environment style
    sns.set_style("ticks", {"axes.spines.right":False, "axes.spines.top":False})
    sns.set_context("notebook")
    fig, ax = plt.subplots(figsize = (7, 3))
    ax.set(ylim=(ymin, ymax))
    #plot the spot curve
    sns.lineplot(ax = ax, data = spotData.iloc[0], dashes = False, legend = False)
    #peripherals in plot
    ax.set(ylabel = "Yield %")
    ax.set(xlabel = "Years")
    plt.close()
    
    #save figure, assigning random number to get over issue of cached image
#    try:
#        shutil.rmtree(staticPath)
#        os.mkdir(staticPath)
#    except:
#        os.mkdir(staticPath)
#    tag = str(random.randint(0,999))
#    graphPath = "\\corrGraph"+tag+".png"
#    staticGraphPath = "\\static" + graphPath
#    fig.savefig(staticPath + graphPath, bbox_inches = "tight")

    return fig, staticGraphPath

