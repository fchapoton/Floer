try:
    import Tkinter as tkinter
except ImportError:
    import tkinter

from .visu import drawBraid

import copy


class OLink:
    def __init__(self, c, entry):
        self.word = copy.deepcopy(c)
        self.entry = entry

    def toStringRepr(self):
        return "OLink({},{})".format(self.word, self.entry)

    def draw(self):
        root = tkinter.Tk()
        fig = tkinter.Canvas(root, width=800, height=800)
        fig.pack()
        drawBraid(10, 10, 790, 790, self.word, self.entry, 10, fig)
        root.mainloop()


if __name__ == "__main__":
    k = OLink([(2, 0), (3, 0)], 0)
    k.draw()
