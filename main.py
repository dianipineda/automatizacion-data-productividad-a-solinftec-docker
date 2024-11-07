from flask import Flask
from src.controllers.ins_productividad import ins_productividad

# print("establish_connection-----> ", establish_connection())
app = Flask(__name__)

# @app.route('/',methods=['GET','POST'])
def main():
    ins_productividad()
    

if __name__ == '__main__':
    main()
    # app.run(host="0.0.0.0", port=4000, debug=False)