from data.ingredientes import ingredientes
from data.compatibilidad import compatibilidad


def calcular_propiedades(mezcla):
    propiedades = {
        "Fuerza": 0,
        "Dulzor": 0,
        "Acidez": 0,
        "Efervescencia": 0,
        "Frialdad": 0,
        "Sabor": 0
    }

    if not mezcla:
        return propiedades

    for nombre in mezcla:
        for propiedad in propiedades:
            propiedades[propiedad] += ingredientes[nombre][propiedad]

    cantidad = len(mezcla)
    for propiedad in propiedades:
        propiedades[propiedad] /= cantidad

    return propiedades


def calcular_equilibrio(propiedades):
    # Excluimos "Sabor" (dominancia) para evaluar solo el balance sensorial real
    claves_sensoriales = ["Fuerza", "Dulzor", "Acidez", "Efervescencia", "Frialdad"]
    valores = [propiedades[k] for k in claves_sensoriales]

    distancia = sum((valor - 2.5) ** 2 for valor in valores) / len(valores)
    puntuacion = 30 * (1 - distancia / 6.25)

    return max(0, puntuacion)


def calcular_compatibilidad(mezcla):
    total = 0
    parejas = 0

    for i in range(len(mezcla)):
        for j in range(i + 1, len(mezcla)):
            ingrediente1 = mezcla[i]
            ingrediente2 = mezcla[j]

            total += compatibilidad[ingrediente1][ingrediente2]
            parejas += 1

    if parejas == 0:
        return 50

    return total / parejas

def calcular_variedad(mezcla):
    cantidad = len(set(mezcla))
    return min(cantidad, 4) * 5


def calcular_puntuacion(mezcla, propiedades):
    compat = calcular_compatibilidad(mezcla)
    equilibrio = calcular_equilibrio(propiedades)
    variedad = calcular_variedad(mezcla)
    tecnica = 10

    puntuacion = (
        compat * 0.4
        + equilibrio
        + variedad
        + tecnica
    )

    return puntuacion

