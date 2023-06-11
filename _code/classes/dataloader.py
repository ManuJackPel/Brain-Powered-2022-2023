class LockableDeque:
    def __init__(self,  maxlen: int ):
        self._deque = deque(maxlen=maxlen)
        self._lock = False

    def append(self, item):
        if not self._lock:
            self._deque.append(item)
        else:
            raise Exception("Deque is locked, append operation not allowed.")

    def lock(self):
        self._lock = True

    def unlock(self):
        self._lock = False

    def __getitem__(self, index):
        return self._deque[index]

    def __len__(self):
        return len(self._deque)

    def __str__(self):
        return str(self._deque)
       
