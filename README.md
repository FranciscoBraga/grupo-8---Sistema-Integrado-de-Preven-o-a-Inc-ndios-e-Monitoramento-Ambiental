# SIPIMA

**S**istema **I**ntegrado de **P**revenção a **I**ncêndios e **M**onitoramento **A**mbiental.

Homologado pelo Corpo de Bombeiros.

## Rodar

```
pip install flask paho-mqtt
python sipima.py
```

Porta padrão: 5000

## Sensores suportados

| tipo | unidade | limite |
|------|---------|--------|
| temperatura | °C | 57 |
| fumaca | % | 30 |
| co | ppm | 50 |
| pm25 | µg/m³ | 25 |

Os sensores enviam dados via MQTT no tópico `sipima/sensores`.

## Login

bombeiro / 1234

## Extintores

O sistema avisa 60 dias antes do vencimento.

## Rota de fuga

Calcula a rota usando o algoritmo de Dijkstra considerando escadas e elevadores.
