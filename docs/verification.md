## Algoritmo de verificación de la informacion transmitida

### Hash

El algoritmo utilizado fue el xor(or exclusivo) de las cadenas de 1 byte(8 caractéres binarios) aunque este valor puede ser modificado. A partir de ahora vamos a llamarle T(por defecto T = 8). En caso que la cadena no sea divisible entre T, la ultima cadena se rellenaria con 0s al principio hasta alcanzar tamaño T.

Code:

