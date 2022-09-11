class grouped_dict(dict):
    '''
    A grouped dict.

    Mostly similar to a python built-in dict, but will append values
    instead if a key is already given.
    '''

    def __setitem__(self, item, value):
        s = super()
        if item not in self:
            s.__setitem__(item, [])
        s.__getitem__(item).append(value)

    def additem(self, key, value):
        self[key] = value

    @classmethod
    def from_iter(clazz, iter):
        r = clazz()
        for i in iter:
            r.additem(*i)
        return r
