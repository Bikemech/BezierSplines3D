from matplotlib import pyplot as plt
from  mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
from general_bezier import *


''' select one of the splines below or specify one your self. '''

# Barrel roll
A = Bezier([[0, 0, 0, 0, 1, 1, 1, 1], [0, 1, 1, 0, 0, 1, 1, 0], [0, 0, 1, 1, 1, 1, 0, 0]])

# Corkscrew spline
# A = Bezier([[0, 1, 2, 1], [0, 0, 0, 1], [0, 2, 0, 1]])

# Kaleidoscope
# A = Bezier([
#     [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3],
#     [0, 3, 3, 0, 0, 3, 3, 0, 0, 3, 3, 0, 0, 3, 3, 0],
#     [0, 0, 3, 3, 0, 0, 3, 3, 0, 0, 3, 3, 0, 0, 3, 3]])

# Bow tie spline
# A = Bezier([[0, 1, 0, 1, 0, 1], [0, 0, 1, 1, 0, 1], [0, 0, 0, 0, 0, 0]])


# setup plot figures
fig = plt.figure()
ax1 = fig.add_subplot(111, projection = '3d')


# setup containers for line points...
x = []
y = []
z = []
line = A.yield_curve()

for i, j, k in line:
    x.append(i)
    y.append(j)
    z.append(k)


t = 0

def animate(i):
    global t
    t += 0.005
    if t > 1:
        t = 0

    ki, kj, kk = A.get_k(t)
    structs = A.test(t)

    ax1.clear()

    # comment out forloop to hide subvectors
    for C in structs:
        ax1.plot(*C, 'g')


    # comment to hide features.
    ax1.plot(*A.get_polygon(), c = 'k') # comment to hide outer lines.
    ax1.plot([ki], [kj], [kk], 'bo') # comment to hide tracking marker.
    ax1.plot(x, y, z, c = 'r') # comment to hide spline.


ani = animation.FuncAnimation(fig, animate, interval = 1)

plt.show()
print(A.get_structure(0.5))