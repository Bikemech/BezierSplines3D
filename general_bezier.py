# from tkinter import Tk, Canvas, mainloop
from matplotlib import pyplot as plt
from  mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation

class bezOD:
    def __init__(self, points):
        self.base = points

    def get_k(self, t):
        vectors = []
        for i in range(len(self.base) - 1):
            vectors.append(self.base[i] + t * (self.base[i + 1] - self.base[i]))

        while len(vectors) > 1:
            temp = []
            for i in range(len(vectors) - 1):
                temp.append(vectors[i] + t * vectors[i + 1] - vectors[i])
            vectors = temp

        return vectors[0]

    def get_p(self, t):
        p = []
        for i in range(len(self.base) - 1):
            p.append(self.base[i] + t * (self.base[i + 1] - self.base[i]))

        return p

    def get_full_p(self, t):
        if len(self.base) > 2:
            return [bezOD(self.get_p(t)).base] + bezOD(self.get_p(t)).get_full_p(t)
        else:
            return [[self.base[0] + t *(self.base[1] - self.base[0])]]
        
class Bezier:
    def __init__(self, points):
        self.dimensions = []
        for k in points:
            self.dimensions.append(bezOD(k))

    def get_k(self, t):
        return tuple([D.get_k(t) for D in self.dimensions])

    def yield_curve(self, resolution = 100):
        coordinates = []
        for p in range(resolution + 1):
            coordinates.append(self.get_k(p/resolution))

        return coordinates

    def get_polygon(self):
        A = tuple(D.base for D in self.dimensions)
        return tuple([j for j in B] for B in A)

    def get_structure(self, t):

        return [tuple(D.get_p(t) for D in self.dimensions)]

    def test(self, t):
        temp = [D.get_full_p(t) for D in self.dimensions]

        new = []
        for i in range(len(temp[0])):
            new.append([])
            for j in range(len(temp)):
                new[i].append(temp[j][i])
                
        return new

W, H = 500, 500

# root = Tk()
# frame = Canvas(root, width = W, height = H, bg = "#000000")
# frame.pack()

# A = Bezier([[0, 0, 0, 0, 1, 1, 1, 1], [0, 1, 1, 0, 0, 1, 1, 0], [0, 0, 1, 1, 1, 1, 0, 0]])
# A = Bezier([[0, 1, 2, 1], [0, 0, 0, 1], [0, 2, 0, 1]])
A = Bezier([
    [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3],
    [0, 3, 3, 0, 0, 3, 3, 0, 0, 3, 3, 0, 0, 3, 3, 0],
    [0, 0, 3, 3, 0, 0, 3, 3, 0, 0, 3, 3, 0, 0, 3, 3]])
# A = Bezier([[0, 1, 0, 1, 0, 1], [0, 0, 1, 1, 0, 1], [0, 0, 0, 0, 0, 0]])

line = A.yield_curve()

fig = plt.figure()
ax1 = fig.add_subplot(111, projection = '3d')
# ax2 = fig.add_subplot(111, projection = '3d')

x = []
y = []
z = []

for i, j, k in line:
    x.append(i)
    y.append(j)
    z.append(k)

# ax2.plot(x, y, z, c='r')
# ax2.plot(*A.get_polygon(), c='b')

# B = A.test(0.2)
# for b in B:
#     ax.plot(*b, 'g')

t = 0

def animate(i):
    global t
    t += 0.005
    if t > 1:
        t = 0

    structs = A.test(t)
    ax1.clear()
    for C in structs:
        ax1.plot(*C, 'g')

    ax1.plot(*A.get_polygon(), c = 'k')
    ax1.plot(x, y, z, c = 'r')
    ki, kj, kk = A.get_k(t)
    ax1.plot([ki], [kj], [kk], 'bo')

ani = animation.FuncAnimation(fig, animate, interval = 1)

plt.show()

print(A.get_structure(0.5))