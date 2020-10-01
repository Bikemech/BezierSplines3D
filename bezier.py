from matplotlib import pyplot as plt
from  mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation

# A class for one dimensional B-splines
class bezOD:
    def __init__(self, points):
        self.base = points

    def get_k(self, t):
        vectors = []
        for i in range(len(self.base) - 1):
            vectors.append(self.base[i] + t * (self.base[i + 1] - self.base[i]))

        # This could probably be done more efficiently....
        # this is the part where we 'recursively' extract our
        # value k, which is the parameter value of the entire
        # set of points for this dimension.
        while len(vectors) > 1:
            temp = []
            for i in range(len(vectors) - 1):
                temp.append(vectors[i] + t * vectors[i + 1] - vectors[i])
            vectors = temp

        return vectors[0]


    # use this one to get the line instead of self.get_k()
    def get_k2(self, t):
    	vectors = self.base.copy()
    	for j in range(1, len(vectors)):
    		for i in range(len(vectors) - j):
    			vectors[i] = vectors[i] + t * (vectors[i + 1] - vectors[i])

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


# A class composing n-amount of bez0d objects to
# make up n-dimensional splines.        
class Bezier:
	# points is an array containing arrays of points.
    def __init__(self, points):
        self.dimensions = []
        for k in points:
            self.dimensions.append(bezOD(k))

    def get_k(self, t):
        return tuple([D.get_k2(t) for D in self.dimensions])

    def yield_curve(self, resolution = 100):
        coordinates = []
        # Iterate through 0 to resulution inclusively
        for p in range(resolution + 1):
            # append the x, y and z coordinates in order.
            # p / resultion should be a number between 0 and 1
            coordinates.append(self.get_k(p/resolution))

        return coordinates

    def get_polygon(self):
        A = tuple(D.base for D in self.dimensions)
        return tuple([j for j in B] for B in A)

    def get_structure(self, t):
        return [tuple(D.get_p(t) for D in self.dimensions)]

    # should be called something else..?
    def test(self, t):
        temp = [D.get_full_p(t) for D in self.dimensions]

        new = []
        for i in range(len(temp[0])):
            new.append([])
            for j in range(len(temp)):
                new[i].append(temp[j][i])
                
        return new
'''
if __name__ == "__main__":

	# A = Bezier([[0, 0, 0, 0, 1, 1, 1, 1], [0, 1, 1, 0, 0, 1, 1, 0], [0, 0, 1, 1, 1, 1, 0, 0]])
	# A = Bezier([[0, 1, 2, 1], [0, 0, 0, 1], [0, 2, 0, 1]])
	# A = Bezier([
	#     [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3],
	#     [0, 3, 3, 0, 0, 3, 3, 0, 0, 3, 3, 0, 0, 3, 3, 0],
	#     [0, 0, 3, 3, 0, 0, 3, 3, 0, 0, 3, 3, 0, 0, 3, 3]])
	A = Bezier([[0, 1, 0, 1, 0, 1], [0, 0, 1, 1, 0, 1], [0, 0, 0, 0, 0, 0]])


	fig = plt.figure()
	ax1 = fig.add_subplot(111, projection = '3d')

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
	print(A.get_structure(0.5))'''