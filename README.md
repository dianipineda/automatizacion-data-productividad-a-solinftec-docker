# automatizacion-data-productividad-a-solinftec-docker
automatizacion de data con docker
# generar ejecutable de escritorio
# todo: EJECUTABLE ACTUAL quitarle la salida de consola cuando se abre el modal, ver si con --noconsole funciona
pyinstaller --onefile --add-binary "D:\INGENIO\projects\automatizacion-data-productividad-a-solinftec-docker\python310.dll;." --add-data "D:\INGENIO\projects\automatizacion-data-productividad-a-solinftec-docker\setup_environment_bbdd-1.0.0.tar.gz;." --add-data "D:\INGENIO\projects\automatizacion-data-productividad-a-solinftec-docker\.env;." main.py

# nota: el ejecutable del primer proyecto que no era docker estaba asi:
pyinstaller --onefile --add-binary "D:\INGENIO\projects\localapp-distribution-cecos\python310.dll;." --noconsole --add-data "D:\INGENIO\projects\localapp-distribution-cecos\setup_environment_bbdd-1.0.0.tar.gz;." --hidden-import requests main.py

#!Nota:
    #?comentar/descomentar para pasar a modo web o a modo escritorio en los siguientes archivos:
    # main.py
    # Dockerfile

#PRUEBAS
# Para realizar pruebas, ejecutar la aplicacion de la siguiente manera:
