from flask import Flask,request,jsonify
from flask_basicauth import BasicAuth
from textblob import TextBlob
from sklearn.linear_model import LinearRegression
import pickle
import os

colunas = ['tamanho','ano','garagem']
# importando variavel gravada no colab
modelo = pickle.load(open('../../models/modelo.sav','rb'))

app = Flask(__name__)
# app.config['BASIC_AUTH_USERNAME'] = os.environ.get('BASIC_AUTH_USERNAME')
# app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('BASIC_AUTH_PASSWORD')

app.config['BASIC_AUTH_USERNAME'] = 'natan'
app.config['BASIC_AUTH_PASSWORD'] = 'alura'

basic_auth = BasicAuth(app)

#definindo as rotas
@app.route('/')
def home():
    return '''<h1>API DE PAI</h1> 
            <a href="http://127.0.0.1:5000/sentimento/happy">Visit Test Polarity</a>
            <br> <br> <br>
            <a href="http://127.0.0.1:5000/cotacao/">Visit Cotacao House</a>'''

#endpoint da aplicação
@app.route('/sentimento/<frase>')
@basic_auth.required
def sentimento(frase):
    tb = TextBlob(frase)
    polaridade = tb.sentiment.polarity
    return f' <h1>Polaridade:{polaridade}</h1> <a href="http://127.0.0.1:5000">Return Main</a>'

@app.route('/cotacao/',methods=['POST'])
@basic_auth.required
def cotacao():
    dados = request.get_json()
    dados_input = [dados[col] for col in colunas]
    preco = modelo.predict([dados_input])
    return jsonify(preco=preco[0])

app.run(debug=True, host='0.0.0.0')