
#dependencias comuns
import sys, json

#dependencias adicionais
sys.path.append('dependencies')
import validation_driver
from flask import Flask, request

app = Flask(__name__)
@app.route('/', methods=['POST'])

def hello():
    data = request.get_data()
    results = validation_driver.run(data)
    return json.dumps(results)

if __name__ == "__main__":
    app.run()
