# automatizacion-data-productividad-a-solinftec-docker
automatizacion de data con docker
# generar ejecutable de escritorio
#TODO: Cuando me entregue mario el nuevo query realizar el versionamiento del segundo entregable con tag
pyinstaller --onefile --noconsole --add-binary "D:\INGENIO\projects\automatizacion-data-productividad-a-solinftec-docker\python310.dll;." --add-data "D:\INGENIO\projects\automatizacion-data-productividad-a-solinftec-docker\setup_environment_bbdd-1.0.0.tar.gz;." --add-data "D:\INGENIO\projects\automatizacion-data-productividad-a-solinftec-docker\.env;." main.py

# nota de ejecutable, en la carpeta del ejecutable deben estar los siguientes archivos para que este programa funcione correctamente:
# - instantclient_19_24.zip
# - logo_carmelita.png

#PRUEBAS
# Para realizar pruebas, ejecutar la aplicacion de la siguiente manera:

#VERSIONAMIENTO
# Actualizar el archivo metadata.py y generar un tag de git

#!Nota:
    #?comentar/descomentar para pasar a modo web o a modo escritorio en los siguientes archivos:
    # main.py
    # Dockerfile