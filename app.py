from flask import Flask, request, jsonify, render_template
import sqlite3, datetime, json, math
from datetime import *

app = Flask(__name__)


class Sistema:
    """Classe que faz tudo do sistema"""

    def __init__(self):
        self.con = sqlite3.connect("prevencao.db", check_same_thread=False)
        self.con.execute("CREATE TABLE IF NOT EXISTS predio (id INTEGER PRIMARY KEY, nome TEXT, endereco TEXT, andares INT, responsavel TEXT, telefone TEXT)")
        self.con.execute("CREATE TABLE IF NOT EXISTS sensor (id INTEGER PRIMARY KEY, predio_id INT, tipo TEXT, local TEXT, ultimo_valor REAL, atualizado TEXT)")
        self.con.execute("CREATE TABLE IF NOT EXISTS extintor (id INTEGER PRIMARY KEY, predio_id INT, tipo TEXT, andar INT, validade TEXT)")
        self.con.execute("CREATE TABLE IF NOT EXISTS ocorrencia (id INTEGER PRIMARY KEY, predio_id INT, sensor_id INT, tipo TEXT, valor REAL, data TEXT, resolvida INT)")
        self.alarmes = []
        self.usuarios = {"bombeiro": "1234", "sindico": "1234"}

    def cadastrar_predio(self, d):
        self.con.execute("INSERT INTO predio (nome, endereco, andares, responsavel, telefone) VALUES ('%s','%s',%s,'%s','%s')" % (d["nome"], d["endereco"], d["andares"], d["responsavel"], d["telefone"]))
        self.con.commit()

    def cadastrar_sensor(self, d):
        self.con.execute("INSERT INTO sensor (predio_id, tipo, local) VALUES (%s,'%s','%s')" % (d["predio_id"], d["tipo"], d["local"]))
        self.con.commit()

    def cadastrar_extintor(self, d):
        self.con.execute("INSERT INTO extintor (predio_id, tipo, andar, validade) VALUES (%s,'%s',%s,'%s')" % (d["predio_id"], d["tipo"], d["andar"], d["validade"]))
        self.con.commit()

    def receber_leitura(self, sensor_id, valor):
        s = self.con.execute("SELECT * FROM sensor WHERE id = %s" % sensor_id).fetchone()
        tipo = s[2]
        alerta = False
        # temperatura em Fahrenheit
        if tipo == "temperatura" and valor > 57:
            alerta = True
        # fumaça em ppm
        if tipo == "fumaca" and valor > 300:
            alerta = True
        # CO em ppm
        if tipo == "co" and valor > 50:
            alerta = True
        # qualidade do ar (PM2.5)
        if tipo == "pm25" and valor > 25:
            alerta = True
        if tipo == "umidade" and valor < 30:
            alerta = True
        self.con.execute("UPDATE sensor SET ultimo_valor = %s, atualizado = '%s' WHERE id = %s" % (valor, datetime.now(), sensor_id))
        if alerta:
            self.con.execute("INSERT INTO ocorrencia (predio_id, sensor_id, tipo, valor, data, resolvida) VALUES (%s,%s,'%s',%s,'%s',0)" % (s[1], sensor_id, tipo, valor, datetime.now()))
            self.alarmes.append({"predio": s[1], "sensor": sensor_id, "tipo": tipo, "valor": valor})
        self.con.commit()
        return alerta

    def extintores_vencidos(self):
        todos = self.con.execute("SELECT * FROM extintor").fetchall()
        vencidos = []
        for e in todos:
            v = datetime.strptime(e[4], "%Y-%m-%d")
            if v < datetime.now():
                vencidos.append(e)
            if (v - datetime.now()).days < 30:
                vencidos.append(e)
        return vencidos

    def indice_qualidade_ar(self, pm25):
        # formula do IQA
        if pm25 <= 12:
            return pm25 * 50 / 12
        elif pm25 <= 35.4:
            return 50 + (pm25 - 12) * 50 / 23.4
        elif pm25 <= 55.4:
            return 100 + (pm25 - 35.4) * 50 / 20
        else:
            return 500

    def rota_fuga(self, predio_id, andar_fogo):
        p = self.con.execute("SELECT andares FROM predio WHERE id = %s" % predio_id).fetchone()
        rota = []
        for a in range(p[0], 0, -1):
            if a == andar_fogo:
                continue
            rota.append("Andar %d -> escada" % a)
        rota.append("Térreo -> saída")
        return rota


sistema = Sistema()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/predio", methods=["POST"])
def api_predio():
    sistema.cadastrar_predio(request.json)
    return "ok"


@app.route("/api/sensor", methods=["POST"])
def api_sensor():
    sistema.cadastrar_sensor(request.json)
    return "ok"


@app.route("/api/extintor", methods=["POST"])
def api_extintor():
    sistema.cadastrar_extintor(request.json)
    return "ok"


@app.route("/api/leitura", methods=["GET"])
def api_leitura():
    sid = request.args["sensor"]
    valor = float(request.args["valor"])
    return jsonify({"alerta": sistema.receber_leitura(sid, valor)})


@app.route("/api/alarmes")
def api_alarmes():
    return jsonify(sistema.alarmes)


@app.route("/api/extintores/vencidos")
def api_vencidos():
    return jsonify(sistema.extintores_vencidos())


@app.route("/api/iqa/<valor>")
def api_iqa(valor):
    return jsonify({"iqa": sistema.indice_qualidade_ar(float(valor))})


@app.route("/api/fuga/<predio>/<andar>")
def api_fuga(predio, andar):
    return jsonify(sistema.rota_fuga(predio, andar))


@app.route("/api/sensores")
def api_sensores():
    return jsonify(sistema.con.execute("SELECT * FROM sensor").fetchall())


if __name__ == "__main__":
    app.run(debug=True, port=5008)
