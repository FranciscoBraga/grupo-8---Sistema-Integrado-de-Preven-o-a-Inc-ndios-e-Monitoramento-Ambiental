var qtdAlarmes = 0

function carregarSensores() {
  fetch("/api/sensores").then(r => r.json()).then(s => {
    var h = "<table><tr><th>id</th><th>tipo</th><th>local</th><th>valor</th></tr>"
    s.forEach(x => {
      h += "<tr><td>" + x[0] + "</td><td>" + x[2] + "</td><td>" + x[3] + "</td><td>" + x[4] + "</td></tr>"
    })
    document.getElementById("sensores").innerHTML = h + "</table>"
  })
}

function enviarLeitura() {
  var s = document.getElementById("sid").value
  var v = document.getElementById("val").value
  fetch("/api/leitura?sensor=" + s + "&valor=" + v).then(r => r.json()).then(d => {
    if (d.alerta) alert("ALERTA!!!")
    carregarSensores()
  })
}

function carregarAlarmes() {
  fetch("/api/alarmes").then(r => r.json()).then(a => {
    if (a.length > qtdAlarmes) {
      document.getElementById("sirene").play()
    }
    qtdAlarmes = a.length
    var h = ""
    for (var i = 0; i < a.length; i++) {
      h += "<div class='alarme'>Prédio " + a[i].predio + " - " + a[i].tipo + ": " + a[i].valor + "</div>"
    }
    document.getElementById("alarmes").innerHTML = h
  })
}

function carregarExtintores() {
  fetch("/api/extintores/vencidos").then(r => r.json()).then(e => {
    var h = ""
    e.forEach(x => h += "<p>Extintor " + x[0] + " (" + x[2] + ") andar " + x[3] + " vence " + x[4] + "</p>")
    document.getElementById("extintores").innerHTML = h
  })
}

function rota() {
  var p = document.getElementById("fpredio").value
  var a = document.getElementById("fandar").value
  fetch("/api/fuga/" + p + "/" + a).then(r => r.json()).then(passos => {
    document.getElementById("rota").innerHTML = passos.map(x => "<li>" + x + "</li>").join("")
  })
}

carregarSensores()
carregarExtintores()
setInterval(carregarAlarmes, 2000)
