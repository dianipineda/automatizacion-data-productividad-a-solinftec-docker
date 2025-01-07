# automatizacion-data-productividad-a-solinftec-docker
automatizacion de data con docker
# generar ejecutable de escritorio
pyinstaller --onefile --noconsole --add-binary "D:\INGENIO\projects\automatizacion-data-productividad-a-solinftec-docker\python310.dll;." --add-data "D:\INGENIO\projects\automatizacion-data-productividad-a-solinftec-docker\setup_environment_bbdd-1.0.0.tar.gz;." --add-data "D:\INGENIO\projects\automatizacion-data-productividad-a-solinftec-docker\.env;." main.py

#!Nota:
    #?comentar/descomentar para pasar a modo web o a modo escritorio en los siguientes archivos:
    # main.py
    # Dockerfile

#PRUEBAS
# Para realizar pruebas, ejecutar la aplicacion de la siguiente manera:
