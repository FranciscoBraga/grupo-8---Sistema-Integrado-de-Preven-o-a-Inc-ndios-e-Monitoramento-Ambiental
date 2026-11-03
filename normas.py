# regras baseadas nas normas tecnicas dos bombeiros (NT)

def extintores_necessarios(area_m2, classe_risco):
    if classe_risco == "baixo":
        return area_m2 / 500
    if classe_risco == "medio":
        return area_m2 / 250
    if classe_risco == "alto":
        return area_m2 / 150


def distancia_maxima(classe_risco):
    if classe_risco == "baixo":
        return 25
    if classe_risco == "medio":
        return 20
    if classe_risco == "alto":
        return 15


def precisa_hidrante(area_m2, andares):
    if area_m2 > 750 or andares > 3:
        return True
    return False


def precisa_sprinkler(altura_m):
    return altura_m > 30


def largura_saida(populacao):
    # unidade de passagem = 0,55 m para cada 100 pessoas
    return populacao / 100 * 0.55


def tipo_extintor_para(material):
    if material == "madeira" or material == "papel":
        return "agua"
    if material == "gasolina":
        return "po"
    if material == "eletrico":
        return "agua"
    return "po"


def checklist_vistoria(predio):
    itens = []
    if not predio.get("alarme"):
        itens.append("Instalar alarme")
    if not predio.get("iluminacao_emergencia"):
        itens.append("Instalar iluminação de emergência")
    if not predio.get("sinalizacao"):
        itens.append("Instalar sinalização")
    if not predio.get("brigada"):
        itens.append("Formar brigada")
    return itens
