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

# regresa una lista los factores de n
def factores(n):
    lista = []
    for i in range(1,n+1):
        if n % i == 0:
            lista.append(i)
    return lista

# clase Curva, que representa una curva eliptica
# con la forma  y^2 = x^3 + ax + b
class Curva:

    def __init__(self,a,b,n):
        self.a = a
        self.b = b
        self.n = n

    def __str__(self):
        return "y^2 = x^3 + " + str(self.a) + "x + " + str(self.b) + " mod " + str(self.n)
    

# clase Punto que representa puntos en una curva eliptica
class Punto:

    curva = Curva(1,9,17)

    # constructor de la clase
    # si se omiten las coordenadas, devuelve un punto en el infinito
    def __init__(self,x = None, y = None):
        n =  Punto.curva.n 
        self.x = x 
        self.y =  y 
        self.inf = True if (x == None or y == None) else False

    def __str__(self):
        if self.inf:
            return "0"
        return "(" + str(self.x) + "," + str(self.y) + ")"
    
    # devuelve la suma de dos puntos de la curva
    # usa las formulas vistas en clase
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
            #print("p1 != p2")
            divisor = (p2.x - p1.x) % n
            #print("lambda = " + str(divisor))
            mcd,inverso,_ = euclidesExtendido(divisor,n)
            inverso %= n
            aux = ((p2.y - p1.y)*inverso) % n
        else:
            # Si p1 = -p2 regresa el punto en el infinito
            if p1.y == (-p2.y)%n:
                #print("p1 == -p2")
                return Punto()
            #print("p1 == p2")
            divisor = (2*p1.y) % n
            #print("lambda = " + str(divisor))
            mcd,inverso,_ = euclidesExtendido(divisor,n)
            inverso %= n
            aux = ((3*pow(p1.x,2,n) + a)*inverso) % n
        if mcd != 1:
            #raise Exception(str(divisor) + " no tiene inverso, mcd(" + str(divisor) + "," + str(n) + ") es " + str(mcd))
            #print(str(divisor) + " no tiene inverso, mcd(" + str(divisor) + "," + str(n) + ") es " + str(mcd))
            return None
        x3 = (pow(aux,2,n) - p1.x - p2.x) % n
        y3 = (aux * (p1.x - x3) - p1.y) % n
        #print(str(p1) + "+" + str(p2) + "=" + str(Punto(x3,y3)))
        return Punto(x3,y3) 

    # define el negativo de un punto en la curva
    def __neg__(self):
        if self.inf:
            return self
        return Punto(self.x,(-self.y) % Punto.curva.n)

    # define la resta de dos puntos en la curva
    def __sub__(p1, p2):
        return p1 + (-p2)

    # define el producto por un entero
    # esta optimizado para usar menos llamadas recursivas
    def __rmul__(self,n):
        if n < 0:
            return (-n) * (-self)
        elif n == 0:
            return Punto()
        elif n == 2:
            return self + self
        else:
            if n % 2 == 0:
                return 2 * ((n // 2) * self)
            return 2 * ((n // 2) * self) + self

    # devuelve verdadero si el punto pertenece a la curva de la clase
    def esValido(self):
        if self.inf == True:
            return True
        y2 = (self.y**2) % self.curva.n
        y2p = ((self.x**3) + (self.curva.a * self.x) + self.curva.b) % self.curva.n
        return y2 == y2p

# algoritmo paso grande paso chico para curvas
# recibe dos puntos y el orden de la curva
def pgpc(p,q,n):
    m = ceil(sqrt(n)) + 1
    print(m)
    dicc = {}
    # g = j*P
    g = Punto()
    for j in range(m):
        dicc[str(g)] = j
        print(str(j) + " : " + str(g))
        g = g + p  
    mp = m * p
    # g = i*m*P
    print("mp = " + str(mp))
    g = Punto()
    for i in range(m):
        print(str(i) + " : " + str(q - g))
        value = dicc.get(str(q - g),None)
        if value != None:
            print("i:" + str(i))
            print("j:" + str(value))
            return (i*m + value)%n
        g = g + mp
    