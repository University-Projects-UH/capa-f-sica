# Capa Física
 
Para hacer funcionar el programa solo es necesario, introducir la entrada correspondiente en el archivo 'script.txt' y ejectuar el programa usando el comando '**python3 main.py**'.

**MyProtocol** es una clase que su constructor recibe como párametro el nombre de un fichero en el directorio del proyecto, por ejemplo ``` script.txt ```

A continución se muetran las posibles instrucciones que puede tener ```script.txt```.

```html
(1) <time> create hub <name> <cantidad_de_puertos>
◦ ejemplo: 0 create hub h 4
◦ los puertos de los hubs se identifican con el nombre del hub, un guión bajo y un número entre 1 y la cantidad de puertos. En el ejemplo anterior el hub se llama h y los puertos se llaman h_1, h_2, h_3 y h_4

(2) <time> create host <name>
◦ esta instrucción permite adicionar una nueva computadora al sistema
◦ el nombre del único puerto que tiene la computadora es igual al nombre de la computadora concatenado con un “_1”. en el ejemplo siguiente la computadora se llama pc, por lo tanto el puerto se llama pc_1
◦ ejemplo: 0 create host pc

(3) <time> connect <port1> <port2>
◦ conecta 2 puertos de 2 dispositivos
◦ ejemplo: 0 connect h_1 pc_1

(4) <time> send <host> <data>
◦ este comando permite que 1 computadora decida empezar a transmitir una información.
◦ Esta información será siempre múltiplos de un byte, y se especificarán todos los bits
◦ ejemplo: 0 send pc_1 0101010111001100

(5) <time> disconnect <port>
◦ con este comando se desconeta un cable de uno de los puertos
◦ puede ser en medio de una transmisión
◦ ejemplo: 20 disconnect pc_1
```
