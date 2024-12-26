__version_web__ = "1.0.0"
__version_desktop__ = "1.0.0"
#?comentar/descomentar Ejecución modo web
# from flask import Flask, jsonify, render_template
#?comentar/descomentar Ejecución modo escritorio
from flask import Flask

from source.oracle_client import install_oracle_client
from src.controllers.ins_productividad import ins_productividad
from src.ui_desktop.ui import vista

app = Flask(__name__, template_folder="src/templates", static_folder="src/static")

#?comentar/descomentar Ejecución modo web
# @app.route('/', methods=['GET'])
# def home_web():
#     return render_template('index.html') 

#?comentar/descomentar Ejecución modo web
# @app.route('/ins_productividad',methods=['POST'])
# def main_web():
#     response = ins_productividad()
#     return jsonify(response)

#?comentar/descomentar Ejecución modo escritorio    
def main_desktop():
    install_oracle_client()
    vista()

if __name__ == '__main__':
    #?comentar/descomentar Ejecución modo web
    # app.run(host="0.0.0.0", port=5000, debug=True)

    #?comentar/descomentar Ejecución modo escritorio
    main_desktop()