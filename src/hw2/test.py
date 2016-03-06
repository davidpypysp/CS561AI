s = 'Traitor(Anakin)'

def g(n):
    for i in range(n):
        print "test: " + str(i)
        if i % 2 == 0: pass
        else: yield i

t = g(5)

print t.next()



