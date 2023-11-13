import math
import matplotlib.pyplot as plt
import numpy as np
import time


fig = plt.figure()

ax = fig.add_subplot(1,1,1)


# animated=True tells matplotlib to only draw the artist when we
# explicitly request it
x = np.linspace(-100, 100, 100)
y = np.linspace(-100, 100, 100)

(ln,) = ax.plot([0,1.5,2], [0,1,3], animated=True)

# make sure the window is raised, but the script keeps going
plt.show(block=False)

# stop to admire our empty window axes and ensure it is rendered at
# least once.
#
# We need to fully draw the figure at its final size on the screen
# before we continue on so that :
#  a) we have the correctly sized and drawn background to grab
#  b) we have a cached renderer so that ``ax.draw_artist`` works
# so we spin the event loop to let the backend process any pending operations
plt.pause(0.1)

# get copy of entire figure (everything inside fig.bbox) sans animated artist
bg = fig.canvas.copy_from_bbox(fig.bbox)
# draw the animated artist, this uses a cached renderer
ax.draw_artist(ln)

# show the result to the screen, this pushes the updated RGBA buffer from the
# renderer to the GUI framework so you can see it
fig.canvas.blit(fig.bbox)

yData = [0] *100

for j in range(1000):
    
    # reset the background back in the canvas state, screen unchanged
    fig.canvas.restore_region(bg)
    # time.sleep(1)
    # update the artist, neither the canvas state nor the screen have changed
    yData.append(math.sin(j/10))
    yData.pop(0)    
    
    ln.set_ydata(yData)
    ln.set_xdata(range(len(yData)))
    ax.relim()
    ax.autoscale_view()

    # re-render the artist, updating the canvas state, but not the screen
    time.sleep(.01)
    ax.draw_artist(ln)
    
    # copy the image to the GUI state, but screen might not be changed yet
    
    fig.canvas.blit(fig.bbox)
    
    
    # flush any pending GUI events, re-painting the screen if needed
    fig.canvas.flush_events()
    
    # you can put a pause in if you want to slow things down
    