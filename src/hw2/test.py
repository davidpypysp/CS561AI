s = 'Traitor(Anakin)'

def g(n):
    if n == 0:
        yield n

t = g(5)

print t.next()



