# TESIS_2023
Configuración de Dockerfile:
1-Descargue el Dockerfile y ejecute en terminal el siguiente comando: docker build -t "nombre_de_imagen" "ruta_de_dockerfile_dentro_de_local"
2-Espere a que se instalen las dependencias
3-Ejecute el contenedor Docker de la siguiente forma: docker run -it --rm --name "nombre_de_contenedor" "nombre_de_imagen"
4-Se creará un entorno básico de Debian con Python, Git, y las bibliotecas Tkinter y OpenCV descargadas en ella, así como pip
