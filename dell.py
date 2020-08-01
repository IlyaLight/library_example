import pickle
from datetime import datetime



simple = dict(int_list=[1, 2, 3],
             text='string',
             number=3.44,
             boolean=True,
             none=None)


class A(object):

    def __init__(self, simple):
        self.simple = simple

    def __eq__(self, other):
        if not hasattr(other, 'simple'):
            return False

        return self.simple == other.simple

    def __ne__(self, other):
        if not hasattr(other, 'simple'):
            return True

        return self.simple != other.simple


complex = dict(a=A(simple), when=datetime(2016, 3, 7))


pickle.dumps(simple)

pickle.dumps(simple, protocol=pickle.HIGHEST_PROTOCOL)

x = pickle.loads(
    b"(dp1\nS'text'\np2\nS'string'\np3\nsS'none'\np4\nNsS'boolean'\np5\nI01\nsS'number'\np6\nF3.4399999999999999\nsS'int_list'\np7\n(lp8\nI1\naI2\naI3\nas.")

assert x == simple

x = pickle.loads(
    b'\x80\x02}q\x01(U\x04textq\x02U\x06stringq\x03U\x04noneq\x04NU\x07boolean\x88U\x06numberq\x05G@\x0b\x85\x1e\xb8Q\xeb\x85U\x08int_list]q\x06(K\x01K\x02K\x03eu.')

assert x == simple