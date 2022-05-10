#%%
from bezier import *
from tkinter import Tk, Canvas
from random import randint

W, H = 500, 500
R = 1000

root = Tk()
frame = Canvas(root, width=W, height=H, bg="#FFFFFF")
frame.pack()

# b1 = Bezier(
#     [[randint(50, 450) for i in range(20)], [randint(50, 450) for j in range(20)]]
# )
# b1 = Bezier(
#     [
#         [50, 450, 450, 50, 50, 450, 450, 50, 50, 450, 450, 50, 50, 450, 450, 50],
#         [50, 50, 450, 450, 50, 50, 450, 450, 50, 50, 450, 450, 50, 50, 450, 450],
#     ]
# )
b1 = Bezier(
    [[250, 250, 10, 490, 10, 490, 250, 250], [490, 250, 250, 250, 250, 250, 250, 10]]
)
line = b1.yield_curve(R)

structures_temp = []

polygon = b1.get_polygon()
for i in range(len(polygon[0]) - 1):
    frame.create_line(
        polygon[0][i],
        polygon[1][i],
        polygon[0][i + 1],
        polygon[1][i + 1],
        fill="#000000",
        width=1,
    )

p_range = iter(range(R + 1))


def animate():
    p = next(p_range, None)
    if p is None:
        return

    t = p / R
    struct = b1.get_structure(t)
    C = struct[:-1]

    while structures_temp:
        frame.delete(structures_temp.pop(-1))

    if p > 0:
        frame.create_line(line[p - 1] + line[p], fill="#FF0000", width=3)

    for j in range(len(C)):
        for k in range(len(C[j]) - 1):
            structures_temp.append(
                frame.create_line(
                    C[j][k][0],
                    C[j][k + 1][0],
                    C[j][k][1],
                    C[j][k + 1][1],
                    fill="#FF0000",
                )
            )
    frame.update()
    frame.after(1, animate)


animate()

while structures_temp:
    frame.delete(structures_temp.pop(-1))

frame.mainloop()
print("Done.")
