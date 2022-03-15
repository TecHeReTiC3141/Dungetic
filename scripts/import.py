class A:
    a = 1

    def ch_a(self):
        self.a += 1

    @classmethod
    def glob_ch_a(cls):
        cls.a += 3

a1 = A()
a2 = A()

a1.ch_a()

a3 = A()
print(a1.a, a2.a, a3.a)
print(a1.__dict__, a2.__dict__, a3.__dict__)
A.glob_ch_a()
a2.ch_a()
print(a1.a, a2.a, A.a)
a3 = A()
print(a3.a)