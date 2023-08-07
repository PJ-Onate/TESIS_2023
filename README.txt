Bienenido! 

En este documento se explica como ejecutar y utilizar el contendor que servírá para virtualzar la aplicación de proyecto de título y modifcarlo en sistemas Linux

La imagen fue probada sólo en sistemas Debian, SE DEBE TENER INSTALADO DOCKER Y GIT EN HOST LOCAL PARA CORRER LA IMAGEN Y EL CONTENEDOR


1-INSTALAR DOCKER en su sistema Debian, he aquí un tutorial.
https://proyectoa.com/instalar-docker-y-docker-compose-en-linux-debian-11/

2-Después de instalar Docker, ejecutar en terminal "sudo groupadd -f docker"

3-Luego "sudo usermod -aG docker $USER"

4-Después "newgrp docker"

5-Si no tiene interfaz grafica en sus sistema Debian:
	"sudo apt install tasksel"
	"sudo tasksel"
	(elija GNOME y espere instalación)

6-En el terminal de comandos local, ejecute (no con usuario root):
	"xhost +"
	comando que permite el uso del socket X11 a todos los hosts que se conecten via ssh

7-Instalar Git a traves de sudo apt-get install git

8-Ahora, se debe ir al repositorio Git del proyecto (git clone https://github.com/PJ-Onate/TESIS_2023.git). Solamente se ocupará el Dockerfile por el momento

9-El proyecto de Git incluye el Dockerfile dentro de Prueba 1. Una vez que el Dockerfile esté nuestro sistema local, vaya a la carpeta donde se encuentra la imagen dentro del terminal 
de Linux y ejecute "docker build -t "nombre_de_imagen" ." (No con usuario root)

9-ejecute "docker run -ti --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix "nombre-imagen"" (No con usuario root)

10-Dentro del contenedor, podremos ejecutar de nuevo git clone https://github.com/PJ-Onate/TESIS_2023.git para "dockerizar" la app. Para iniciar la aplicación, se debe ir a la carpeta 
"Prueba 1" y se debe ejecutar "python3 main.py", e iniciará la aplicación y su interfaz gráfica.

11-Si queremos editar los códigos y el Dockerfile, nos valdremos del editor "nano" de Linux, que está instalado dentro del contenedor

12-Git también está instalada dentro del contenedor, por lo que desde el contenedor podremos realizar los cambios que queramos, verificar esos cambios y guardarlos en el repositorio remoto.
Para realzar pushs, se pide un token de acceso, lo cuál se puede conseguir siguiendo las instrucciones del tutorial en el enlace de abajo:

https://dev.to/shafia/support-for-password-authentication-was-removed-please-use-a-personal-access-token-instead-4nbk#:~:text=Please%20use%20a%20personal%20access%20token%20instead.,-While%20pushing%20some&text=Starting%20from%20August%2013%2C%202021,in%20place%20of%20your%20password..

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

13-Para salir del contenedor, simplemente se ejecuta "exit" y se borrarán las dependencias instaladas en el contenedor.

*El servidor virtual se utilizará para almacenar la base de datos