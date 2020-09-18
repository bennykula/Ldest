class Singleton(type):
    _INSTANCES = {}

    def __call__(self, *args, **kwargs):
        if self not in self._INSTANCES:
            self._INSTANCES[self] = super(Singleton, self).__call__(*args, **kwargs)
        return self._INSTANCES[self]
