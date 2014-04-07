class SetlxString(str):

    def _zerobased(self, i):
        if type(i) is slice:
            return slice(self._zerobased(i.start),
                         self._zerobased(i.stop), i.step)
        else:
            if i is None or i < 0:
                return i
            elif not i:
                raise IndexError("element 0 does not exist in 1-based string")
            return i - 1

    def __getitem__(self, i):
        n = str.__getitem__(self, self._zerobased(i))
        return SetlxString(n)

    def __setitem__(self, i, value):
        str.__setitem__(self, self._zerobased(i), value)
        
    def __delitem__(self, i):
        str.__delitem__(self, self._zerobased(i))

    def __getslice__(self, i, j):
        """ Setlx slices include the upper limit, whereas Python does not """
        n = str.__getslice__(self, self._zerobased(i or 1), self._zerobased(j + 1))
        return SetlxString(n)

    def __setslice__(self, i, j, value):
        str.__setslice__(self, self._zerobased(i or 1),
                         self._zerobased(j), value)

    def index(self, value, start=1, stop=-1):
        return str.index(self, value, self._zerobased(start),
                         self._zerobased(stop)) + 1

    def pop(self, i):
        return str.pop(self, self._zerobased(i))

    def index(self, value, start=1, stop=-1):
        return str.index(self, value, self._zerobased(start),
                         self._zerobased(stop)) + 1

    def __add__(self, other):
        s = other if isinstance(other, basestring) else str(other)
        return "{0}{1}".format(self, s)

    def __radd__(self, other):
        s = other if isinstance(other, basestring) else str(other)
        return "{0}{1}".format(s, self)