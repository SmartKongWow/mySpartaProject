from flask import Flask
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/performance', methods=['GET'])
def my_performance():
    return

@app.route('/performance', methods=['GET'])
def performance_get():

    return jsonify({'result':'success', 'msg':'이 요청은 GET!'})

@app.route('/plan', methods=['POST'])
def test_post():
    title_receive = request.form['title_give']
    print(title_receive)
    return jsonify({'result': 'success', 'msg': '이 요청은 POST!'})



if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)