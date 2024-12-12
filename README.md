# automatizacion-data-productividad-a-solinftec-docker
automatizacion de data con docker
# generar ejecutable de escritorio
# todo: quitarle la salida de consola cuando se abre el modal, ver si con --noconsole funciona
pyinstaller --onefile --add-binary "D:\INGENIO\projects\automatizacion-data-productividad-a-solinftec-docker\python310.dll;." --add-data "D:\INGENIO\projects\automatizacion-data-productividad-a-solinftec-docker\setup_environment_bbdd-1.0.0.tar.gz;." main.py
# nota: el ejecutable del primer proyecto que no era docker estaba asi:
pyinstaller --onefile --add-binary "D:\INGENIO\projects\localapp-distribution-cecos\python310.dll;." --noconsole --add-data "D:\INGENIO\projects\localapp-distribution-cecos\setup_environment_bbdd-1.0.0.tar.gz;." --hidden-import requests main.py
