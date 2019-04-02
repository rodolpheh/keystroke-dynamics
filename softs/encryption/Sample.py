
class Sample():
    i = 1
    j = 2
    y = 3

    def __str__(self):
        return "Sample : {{i={},j={},y={}}}".format(self.i, self.j, self.y)