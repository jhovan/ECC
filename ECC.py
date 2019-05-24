from math import ceil,floor,sqrt

# recibe dos enteros a y b
# devuelve d,x,y donde:
# d = mcd(a,b)
# x = a^-1 mod b en caso de d=1
# y = b^-1 mod a en caso de d=1
# NOTA: x y y pueden ser negativos
def euclidesExtendido(a,b):
    if b == 0:
        return a, 1, 0
    d1,x1,y1 = euclidesExtendido(b, a % b)
    d = d1
    x = y1
    y = x1 - (a//b) * y1
    return d, x, y


class Curva:

    #y^2 = x^3 + ax + b
    def __init__(self,a,b,n):
        self.a = a
        self.b = b
        self.n = n

    def __str__(self):
        return "y^2 = x^3 + " + str(self.a) + "x + " + str(self.b) + " mod " + str(self.n)
    

class Punto:

    curva = Curva(1,9,17)

    def __init__(self,x = None, y = None):
        n =  Punto.curva.n 
        self.x = x 
        self.y =  y 
        self.inf = True if (x == None or y == None) else False

    def __str__(self):
        if self.inf:
            return "0"
        return "(" + str(self.x) + "," + str(self.y) + ")"
    
    def __add__(p1, p2):
        #Evalua los casos en los que p1 o p2 es el punto en el infinito
        if p1.inf == True:
            return p2
        if p2.inf == True:
            return p1
        n = Punto.curva.n
        a = Punto.curva.a
        p1 = Punto(p1.x % n,p1.y % n)
        p2 = Punto(p2.x % n,p2.y % n)
        if p1.x != p2.x:
            print("p1 != p2")
            divisor = (p2.x - p1.x) % n
            mcd,inverso,_ = euclidesExtendido(divisor,n)
            inverso %= n
            aux = ((p2.y - p1.y)*inverso) % n
        else:
            # Si p1 = -p2 regresa el punto en el infinito
            if p1.y == (-p2.y)%n:
                print("p1 != p2")
                return Punto()
            print("p1 == p2")
            divisor = (2*p1.y) % n
            mcd,inverso,_ = euclidesExtendido(divisor,n)
            inverso %= n
            aux = ((3*pow(p1.x,2,n) + a)*inverso) % n
        if mcd != 1:
            #raise Exception(str(divisor) + " no tiene inverso, mcd(" + str(divisor) + "," + str(n) + ") es " + str(mcd))
            print(str(divisor) + " no tiene inverso, mcd(" + str(divisor) + "," + str(n) + ") es " + str(mcd))
            return None
        x3 = (pow(aux,2,n) - p1.x - p2.x) % n
        y3 = (aux * (p1.x - x3) - p1.y) % n
        print(str(p1) + "+" + str(p2) + "=" + str(Punto(x3,y3)))
        return Punto(x3,y3) 

    def __neg__(self):
        if self.inf:
            return self
        return Punto(self.x,(-self.y) % Punto.curva.n)

    def __sub__(p1, p2):
        return p1 + (-p2)

    # n*p por definicion
    def __pow__(self,n):
        if n < 0:
            return (-self)**(-n)
        elif n == 0:
            return Punto()
        else:
            return self + (self**(n-1))

    # n*p optimizado
    def __rmul__(self,n):
        if n < 0:
            return (-n) * (-self)
        elif n == 0:
            return Punto()
        else:
            if n % 2 == 0:
                return 2 * ((n / 2) * self)
            return 2 * ((n // 2) * self) + self

        

def pgpc(p,q):
    n = Punto.curva.n
    m = ceil(sqrt(n))
    dicc = {}
    # g = j*P
    g = Punto()
    for j in range(m):
        dicc[str(g)] = j
        print(str(j) + " : " + str(g))
        g = g + p  
    mp = p**m
    # g = i*m*P
    g = Punto()
    for i in range(m):
        print(str(i) + " : " + str(q-g))
        value = dicc.get(str(q-g),None)
        if value != None:
            print("i:" + str(i))
            print("j:" + str(value))
            return (i*m + value)%n
        g = g + mp
    

print("******Ejercicio 1******")
curva = Curva(1,9,17)
print(curva)
p = Punto(0,3)
q = Punto(13,3)
#for i in range(10):
#    print(str(i) + "P=" + str(p**i))
print(pgpc(p,q))
print(p**7)

#desencriptado
a = Punto(12,7)
b = Punto(11,12)
print((a**(-7))+b)

print("******Ejercicio 2******")
Punto.curva = Curva(-20,21,35)
p = Punto(15,-4)
print(p)
print("****3P***** Mod 35")
print(p**3)
print("****4P***** Mod 35")
print(((p**2)**2))
Punto.curva = Curva(-20,21,5)
p = Punto(15,-4)
print("****3P***** Mod 5")
print(p**3)
print("****4P***** Mod 5")
print(p**4)
Punto.curva = Curva(-20,21,7)
p = Punto(15,-4)
print("****3P***** Mod 7")
print(p**3)
print("****4P***** Mod 7")
print(p**4)

print("******Ejercicio 3******")
n = 314423
k = 666
d = 223344
m = 6500
Punto.curva = Curva(217,2006,314159)
P = Punto(123456,43989)
Q = Punto(216438, 187612)
_,kinv,_ = euclidesExtendido(k,n)
G = k * P
print("kP = " + str(G))
r = G.x % n
print("r = " + str(r))
s = (kinv * (m + r * d)) % n
print("s = " + str(s))
_,sinv,_ = euclidesExtendido(s,n)
u1 = (sinv * m ) % n 
u2 = (sinv * r ) % n 
G = (u1 * P) + (u2 * Q) 
r = G.x % n
print("r = " + str(r))