from flask import Flask, jsonify
from src.utils.database import establish_connection

# print("establish_connection-----> ", establish_connection())
app = Flask(__name__)
@app.route('/',methods=['GET','POST'])
def ping():
    return jsonify({"response": establish_connection()})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=False)