import pygame
import sys
from pathlib import Path
import math
from structures import Cola, ColaCircular
from data.ingredientes import ingredientes
from game import calcular_propiedades, calcular_puntuacion

pygame.init()
pygame.mixer.music.set_volume(0.2)

# Dimensiones de la ventana
WIDTH = 1000
HEIGHT = 563

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jonathan Hasta La Ultima Copa")

# BOTONES
botones = {
    "echar": pygame.Rect(100, 460, 240, 70),
    "batir": pygame.Rect(382, 460, 240, 70),
    "servir": pygame.Rect(664, 460, 240, 70)
}

boton_surface = pygame.Surface((240, 70), pygame.SRCALPHA)
boton_surface.fill((0, 255, 0, 0))

clock = pygame.time.Clock()

# Rutas de los recursos
if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent
BACKGROUND_DIR = BASE_DIR / "assets" / "backgrounds"
BOTTLES_DIR = BASE_DIR / "assets" / "bottles"
MUSIC_DIR = BASE_DIR / "assets" / "music"

# Cargar icono de la ventana
icon = pygame.image.load(
    BASE_DIR / "assets" / "logo.png"
).convert_alpha()

# Establecer icono
pygame.display.set_icon(icon)

background = pygame.image.load(
    BACKGROUND_DIR / "fondo.png"
).convert()

background = pygame.transform.scale(
    background, (WIDTH, HEIGHT)
)

# Capa de iluminación
light_surface = pygame.Surface((WIDTH, HEIGHT))

# Nivel de oscuridad (0 = sin oscuridad, 255 = negro)
darkness = 50

# Colores de iluminación
# Colores de iluminación
light_colors = [
    (255, 0, 0),       # Rojo
    (0, 255, 0),       # Verde
    (120, 0, 255),     # Morado
    (0, 0, 120),       # Azul oscuro
    (255, 0, 150)      # Rosa
]

current_color = 0
next_color = 1

light_progress = 0

light_speed = 5
light_intensity = 70

# =====================================
# CARGAR BARTENDER
# =====================================

bartender = pygame.image.load(
    BASE_DIR / "assets" / "characters" / "Jonathan.png"
).convert_alpha()

bartender = pygame.transform.smoothscale(
    bartender, (300, 277)
)

bartender_rect = bartender.get_rect(
    topleft=(705, 104)
)

bartender_frames = [
    pygame.image.load(
        BASE_DIR / "assets" / "characters" / "Jonathan1.png"
    ).convert_alpha(),

    pygame.image.load(
        BASE_DIR / "assets" / "characters" / "Jonathan2.png"
    ).convert_alpha(),

    pygame.image.load(
        BASE_DIR / "assets" / "characters" / "Jonathan3.png"
    ).convert_alpha()
]

bartender_frames = [
    pygame.transform.smoothscale(imagen, (300, 277))
    for imagen in bartender_frames
]

sonido_batido = pygame.mixer.Sound(
    BASE_DIR / "assets" / "effects" / "shake.mp3"
)

sonido_servir = pygame.mixer.Sound(
    BASE_DIR / "assets" / "effects" / "bloxy-cola.mp3"
)

sonido_vertido = pygame.mixer.Sound(
    BASE_DIR / "assets" / "effects" / "pour.mp3"
)

bafle = pygame.image.load(
    BASE_DIR / "assets" / "Bafle.png"
).convert_alpha()

# Dimensiones originales de visualización
BAFLE_WIDTH = 150
BAFLE_HEIGHT = 125

bafle = pygame.transform.smoothscale(
    bafle, (BAFLE_WIDTH, BAFLE_HEIGHT)
)

# Guardar imagen original para las animaciones
bafle_original = bafle.copy()

# Posición del bafle
bafle_rect = bafle.get_rect(
    topleft=(50, 300)
)

# Crear cola de reproducción
cola_musica = Cola()

# Evento que detecta cuando termina una canción
MUSIC_END = pygame.USEREVENT + 1

pygame.mixer.music.set_endevent(MUSIC_END)

# =====================================
# CARGAR BOTELLAS
# =====================================

# Nombre, X, Y, ancho, alto
# Nombre, X, Y, ancho, alto
# Nombre, X, Y, ancho, alto
bottle_data = [

    # Fila superior
    ("SmirnoffTamarindo", 155, 65, 114, 115),
    ("Cachaza",           258, 109, 69, 66),
    ("buchana",           333, 97, 80, 78),
    ("BlueLabel",         419, 74, 67, 97),
    ("Baileys",           482, 88, 95, 85),
    ("Bacardi",           573, 75, 65, 97),
    ("amarillon",         644, 85, 78, 87),

    # Fila intermedia
    ("Ron",               155, 204, 88, 87),
    ("Poker",             225, 181, 110, 115),
    ("Nectar",            313, 206, 93, 86),
    ("FourLoko",          413, 228, 46, 60),
    ("lambrusco",         478, 189, 67, 100),
    ("CocaCola",          543, 200, 86, 92),
    ("cariñoso",          626, 190, 73, 101),

    # Elementos inferiores: sin cambios
    ("Limones",           230, 317, 105, 96),
    ("TasaHielo",         328, 316, 112, 101)
    # ("CocteleraSinTapa",  573, 336, 89, 81)
    # ("Coctelera",         573, 297, 89, 120)
]

coctelera_cerrada = pygame.image.load(
    BOTTLES_DIR / "Coctelera.png"
).convert_alpha()

coctelera_cerrada = pygame.transform.smoothscale(
    coctelera_cerrada, (89, 120)
)

# Cargar imágenes y crear sus rectángulos
bottle_images = []
bottle_rects = []

for name, x, y, width, height in bottle_data:

    image = pygame.image.load(
        BOTTLES_DIR / f"{name}.png"
    ).convert_alpha()

    image = pygame.transform.smoothscale(
        image, (width, height)
    )

    bottle_images.append(image)

    rect = image.get_rect(
        topleft=(x, y)
    )

    bottle_rects.append(rect)

# =====================================
# OBJETOS ESPECIALES
# =====================================

hielo = pygame.image.load(
    BOTTLES_DIR / "hielo.png"
).convert_alpha()

hielo = pygame.transform.smoothscale(
    hielo, (30, 30)
)

rodaja_limon = pygame.image.load(
    BOTTLES_DIR / "rodajaLimon.png"
).convert_alpha()

rodaja_limon = pygame.transform.smoothscale(
    rodaja_limon, (28, 28)
)

DURACION_CAIDA = 400

coctelera_sin_tapa = pygame.image.load(
    BOTTLES_DIR / "CocteleraSinTapa.png"
).convert_alpha()

coctelera_sin_tapa = pygame.transform.smoothscale(
    coctelera_sin_tapa, (89, 81)
)

# =====================================
# SELECCION DE BEBIDAS
# =====================================

cola_bebidas = ColaCircular()
mezcla = []

# Elementos que pueden agregarse a la mezcla
bebidas_seleccionables = [
    name for name, x, y, width, height in bottle_data
    if name not in ["CocteleraSinTapa"]
]

for bebida in bebidas_seleccionables:
    cola_bebidas.encolar(bebida)

# Relacionar cada nombre con su posicion en bottle_data
bottle_indices = {
    name: i
    for i, (name, x, y, width, height) in enumerate(bottle_data)
}

# ANIMACION DE VERTIDO
animacion_vertido = None

DURACION_INCLINACION = 350
DURACION_VERTIDO = 650
DURACION_REGRESO = 350

animacion_batido = None
mezcla_batida = False

DURACION_BATIDO = 2000

ESCALA_SELECCION = 1.25
ESCALA_VERTIDO = 1.45

# PUNTOS DE LA ANIMACION
PUNTO_VERTIDO = (617, 290)
PUNTO_LIQUIDO = (617, 345)

animacion_servir = None
servicio_completado = False

COCTELERA_X_INICIAL = 573
COCTELERA_X_SERVIR = 820
COCTELERA_Y = 336

DURACION_DESPLAZAMIENTO = 500
DURACION_SERVICIO = 4000

coctelera_x = COCTELERA_X_INICIAL

def echar_ingrediente():

    global animacion_vertido

    if animacion_vertido is not None:
        return

    ingrediente = cola_bebidas.obtener_actual()

    if ingrediente is None:
        return

    i = bottle_indices[ingrediente]
    rect = bottle_rects[i]

    # Animaciones especiales: hielo y limón
    if ingrediente in ["TasaHielo", "Limones"]:

        animacion_vertido = {
            "ingrediente": ingrediente,
            "indice": i,
            "inicio": pygame.time.get_ticks(),
            "tipo": "objeto",
            "agregar_mezcla": True
        }

        return

    # Posicion inicial de la boquilla con la escala de seleccion
    alto = int(rect.height * ESCALA_SELECCION)

    boquilla_inicial = (
        rect.centerx,
        rect.centery - alto // 2
    )

    # Determinar hacia donde se inclina la botella
# Determinar hacia donde se inclina la botella
    angulo = -115

    # Desplazamiento especial para algunas botellas
    botellas_medio = [
        "Cachaza",
        "Ron",
        "Nectar",
        "CocaCola",
        "cariñoso"
    ]

    botellas_alto = [
        "SmirnoffTamarindo",
        "Poker"
    ]

    if ingrediente in botellas_medio:
        desplazamiento_x = 10
    elif ingrediente in botellas_alto:
        desplazamiento_x = 15
    else:
        desplazamiento_x = 0

    animacion_vertido = {
        "ingrediente": ingrediente,
        "indice": i,
        "inicio": pygame.time.get_ticks(),
        "boquilla_inicial": boquilla_inicial,
        "angulo": angulo,
        "desplazamiento_x": desplazamiento_x,
        "tipo": "botella",
        "agregar_mezcla": True,
        "sonido_iniciado": False
    }

def draw_buttons():
    for boton in botones.values():
        screen.blit(boton_surface, boton)

def dibujar_con_pivote(imagen, escala, angulo, pivote):

    # Escalar imagen
    width = int(imagen.get_width() * escala)
    height = int(imagen.get_height() * escala)

    imagen_escalada = pygame.transform.smoothscale(
        imagen, (width, height)
    )

    # Rotar imagen
    imagen_rotada = pygame.transform.rotate(
        imagen_escalada, angulo
    )

    # Calcular posicion del pivote despues de rotar
    radianes = math.radians(angulo)

    dx = 0
    dy = -height / 2

    pivote_x = (
        imagen_rotada.get_width() / 2
        + dx * math.cos(radianes)
        + dy * math.sin(radianes)
    )

    pivote_y = (
        imagen_rotada.get_height() / 2
        - dx * math.sin(radianes)
        + dy * math.cos(radianes)
    )

    # Ubicar la imagen manteniendo fijo el pivote
    rect = imagen_rotada.get_rect(
        topleft=(
            round(pivote[0] - pivote_x),
            round(pivote[1] - pivote_y)
        )
    )

    screen.blit(imagen_rotada, rect)

def actualizar_animacion():

    global animacion_vertido

    if animacion_vertido is None:
        return

    tiempo = pygame.time.get_ticks() - animacion_vertido["inicio"]

    if animacion_vertido["tipo"] == "objeto":
        tiempo_total = DURACION_CAIDA

    else:
        tiempo_total = (
            DURACION_INCLINACION
            + DURACION_VERTIDO
            + DURACION_REGRESO
        )

        # Iniciar sonido cuando comienza a salir el líquido
        if (
            tiempo >= DURACION_INCLINACION
            and tiempo < DURACION_INCLINACION + DURACION_VERTIDO
            and not animacion_vertido["sonido_iniciado"]
        ):
            sonido_vertido.play()
            animacion_vertido["sonido_iniciado"] = True

        # Detener sonido cuando termina el vertido
        if tiempo >= DURACION_INCLINACION + DURACION_VERTIDO:
            sonido_vertido.stop()

    if tiempo >= tiempo_total:

        ingrediente = animacion_vertido["ingrediente"]

        if animacion_vertido["agregar_mezcla"]:
            mezcla.append(ingrediente)

            print("Ingrediente agregado:", ingrediente)
            print("Mezcla actual:", mezcla)

        animacion_vertido = None

def draw_bottle_animation():

    if animacion_vertido is None:
        return

    if animacion_vertido["tipo"] != "botella":
        return

    tiempo = pygame.time.get_ticks() - animacion_vertido["inicio"]

    inicio = animacion_vertido["boquilla_inicial"]
    destino = PUNTO_VERTIDO

    angulo_final = animacion_vertido["angulo"]

    # INCLINACION
    if tiempo < DURACION_INCLINACION:

        progreso = tiempo / DURACION_INCLINACION

        angulo = angulo_final * progreso

        x = inicio[0] + (destino[0] - inicio[0]) * progreso
        y = inicio[1] + (destino[1] - inicio[1]) * progreso

        escala = ESCALA_SELECCION + (
            ESCALA_VERTIDO - ESCALA_SELECCION
        ) * progreso

    # VERTIDO
    elif tiempo < DURACION_INCLINACION + DURACION_VERTIDO:

        angulo = angulo_final
        x, y = destino
        escala = ESCALA_VERTIDO

    # REGRESO
    else:

        progreso = (
            tiempo - DURACION_INCLINACION - DURACION_VERTIDO
        ) / DURACION_REGRESO

        angulo = angulo_final * (1 - progreso)

        x = destino[0] + (inicio[0] - destino[0]) * progreso
        y = destino[1] + (inicio[1] - destino[1]) * progreso

        escala = ESCALA_VERTIDO + (
            ESCALA_SELECCION - ESCALA_VERTIDO
        ) * progreso

    # Obtener botella
    i = animacion_vertido["indice"]
    imagen = bottle_images[i]

    # Dibujar botella usando la boquilla como pivote
    desplazamiento_x = animacion_vertido["desplazamiento_x"]

    dibujar_con_pivote(
        imagen,
        escala,
        angulo,
        (x + desplazamiento_x, y)
    )

def draw_objeto_cayendo():

    if animacion_vertido is None:
        return

    if animacion_vertido["tipo"] != "objeto":
        return

    tiempo = pygame.time.get_ticks() - animacion_vertido["inicio"]

    progreso = min(tiempo / DURACION_CAIDA, 1)

    # Seleccionar imagen
    if animacion_vertido["ingrediente"] == "TasaHielo":
        imagen = hielo
    else:
        imagen = rodaja_limon

    # Trayectoria de caída
    inicio = (PUNTO_LIQUIDO[0], 220)
    final = PUNTO_LIQUIDO

    x = inicio[0] + (final[0] - inicio[0]) * progreso
    y = inicio[1] + (final[1] - inicio[1]) * progreso

    # Desaparecer gradualmente al llegar
    alpha = 255

    if progreso > 0.8:
        alpha = int(255 * (1 - progreso) / 0.2)

    objeto = imagen.copy()
    objeto.set_alpha(max(0, alpha))

    rect = objeto.get_rect(
        center=(int(x), int(y))
    )

    screen.blit(objeto, rect)

def draw_lighting():

    global current_color, next_color, light_progress

    light_progress += light_speed

    if light_progress >= 255:

        light_progress = 0
        current_color = next_color

        next_color += 1

        if next_color >= len(light_colors):
            next_color = 0

    # Interpolar colores
    color1 = light_colors[current_color]
    color2 = light_colors[next_color]

    r = color1[0] + (color2[0] - color1[0]) * light_progress / 255
    g = color1[1] + (color2[1] - color1[1]) * light_progress / 255
    b = color1[2] + (color2[2] - color1[2]) * light_progress / 255

    # Aplicar oscuridad
    light_surface.fill((darkness, darkness, darkness))

    screen.blit(
        light_surface,
        (0, 0),
        special_flags=pygame.BLEND_RGB_SUB
    )

    # Aplicar iluminación de colores
    light_surface.fill((
        int(r * light_intensity / 255),
        int(g * light_intensity / 255),
        int(b * light_intensity / 255)
    ))

    screen.blit(
        light_surface,
        (0, 0),
        special_flags=pygame.BLEND_RGB_ADD
    )

def draw_coctelera():

    # SERVICIO
    if animacion_servir is not None:
        tiempo = pygame.time.get_ticks() - animacion_servir["inicio"]

        if tiempo < DURACION_DESPLAZAMIENTO:
            progreso = tiempo / DURACION_DESPLAZAMIENTO

            x = COCTELERA_X_INICIAL + (
                COCTELERA_X_SERVIR - COCTELERA_X_INICIAL
            ) * progreso

            screen.blit(coctelera_sin_tapa, (int(x), COCTELERA_Y))

        return

    # BATIDO
    if animacion_batido is not None:

        tiempo = pygame.time.get_ticks() - animacion_batido

        desplazamiento_x = math.sin(tiempo * 0.06) * 5
        desplazamiento_y = math.sin(tiempo * 0.04) * 7
        angulo = math.sin(tiempo * 0.09) * 9

        imagen = pygame.transform.rotate(
            coctelera_cerrada,
            angulo
        )

        rect = imagen.get_rect(
            center=(
                617 + desplazamiento_x,
                357 + desplazamiento_y
            )
        )

        screen.blit(imagen, rect)
        return

    # ESTADO NORMAL O SERVICIO COMPLETADO
    screen.blit(
        coctelera_sin_tapa,
        (coctelera_x, COCTELERA_Y)
    )

def draw_bartender():

    # Por defecto, Jonathan está en su posición normal
    imagen = bartender

    if animacion_servir is not None:

        tiempo = (
            pygame.time.get_ticks()
            - animacion_servir["inicio"]
            - DURACION_DESPLAZAMIENTO
        )

        if 0 <= tiempo < DURACION_SERVICIO:

            if tiempo < 400:
                imagen = bartender_frames[0]

            elif tiempo < 900:
                imagen = bartender_frames[1]

            elif tiempo < 3100:
                imagen = bartender_frames[2]

            elif tiempo < 3600:
                imagen = bartender_frames[1]

            else:
                imagen = bartender_frames[0]

    screen.blit(imagen, bartender_rect)

def draw_bafle():

    # Tiempo transcurrido en segundos
    time = pygame.time.get_ticks() / 1000

    # =====================================
    # ANIMACIÓN DE TAMAÑO
    # =====================================

    scale = 1 + 0.04 * math.sin(time * 5)

    # =====================================
    # ANIMACIÓN DE ROTACIÓN
    # =====================================

    angle = 2.5 * math.sin(time * 7)

    # Calcular nuevas dimensiones
    width = int(BAFLE_WIDTH * scale)
    height = int(BAFLE_HEIGHT * scale)

    # Redimensionar desde la imagen original
    bafle_animation = pygame.transform.smoothscale(
        bafle_original, (width, height)
    )

    # Rotar imagen
    bafle_animation = pygame.transform.rotate(
        bafle_animation, angle
    )

    # Mantener el centro en la misma posición
    bafle_animation_rect = bafle_animation.get_rect(
        center=bafle_rect.center
    )

    screen.blit(
        bafle_animation,
        bafle_animation_rect
    )

def cargar_canciones():

    canciones = []

    for archivo in MUSIC_DIR.iterdir():

        if archivo.suffix.lower() in [".ogg", ".mp3", ".wav"]:
            canciones.append(archivo)

    canciones.sort()

    for cancion in canciones:
        cola_musica.encolar(cancion)

def reproducir_siguiente():

    # Si la cola está vacía, volver a cargar las canciones
    if cola_musica.esta_vacia():
        cargar_canciones()

    # Extraer la primera canción
    cancion = cola_musica.desencolar()

    # Reproducirla si existe
    if cancion is not None:

        pygame.mixer.music.load(str(cancion))
        pygame.mixer.music.play()

def iniciar_batido():
    global animacion_batido

    if len(mezcla) == 0:
        return

    if animacion_batido is not None or mezcla_batida:
        return

    animacion_batido = pygame.time.get_ticks()
    sonido_batido.play()

def iniciar_servir():
    global animacion_servir

    if not mezcla_batida:
        return

    if servicio_completado or animacion_servir is not None:
        return

    animacion_servir = {
        "inicio": pygame.time.get_ticks(),
        "sonido_iniciado": False
    }

def actualizar_servir():
    global animacion_servir
    global servicio_completado, coctelera_x

    if animacion_servir is None:
        return

    tiempo = pygame.time.get_ticks() - animacion_servir["inicio"]

    if (
        tiempo >= DURACION_DESPLAZAMIENTO
        and not animacion_servir["sonido_iniciado"]
    ):
        sonido_servir.play(loops=-1)
        animacion_servir["sonido_iniciado"] = True

    tiempo_total = DURACION_DESPLAZAMIENTO + DURACION_SERVICIO

    if tiempo >= tiempo_total:
        sonido_servir.stop()

        animacion_servir = None
        servicio_completado = True
        coctelera_x = COCTELERA_X_SERVIR

        print("Animacion ejecutada: Servir")

        mezcla_evaluable = [
            ingrediente
            for ingrediente in mezcla
            if ingrediente != "TasaHielo"
        ]

        if mezcla_evaluable:
            propiedades = calcular_propiedades(mezcla_evaluable)
            puntuacion = calcular_puntuacion(
                mezcla_evaluable,
                propiedades
            )

            print("Propiedades:", propiedades)
            print("Puntuacion:", round(puntuacion, 2))
        else:
            print("No hay ingredientes evaluables.")
            print("Puntuacion: 0")

def actualizar_batido():
    global animacion_batido, mezcla_batida

    if animacion_batido is None:
        return

    tiempo = pygame.time.get_ticks() - animacion_batido

    if tiempo >= DURACION_BATIDO:
        sonido_batido.stop()
        animacion_batido = None
        mezcla_batida = True



def draw_liquido():

    if animacion_vertido is None:
        return

    if animacion_vertido["tipo"] != "botella":
        return

    tiempo = pygame.time.get_ticks() - animacion_vertido["inicio"]

    # El líquido solo aparece durante el vertido
    if not (
        DURACION_INCLINACION <= tiempo <
        DURACION_INCLINACION + DURACION_VERTIDO
    ):
        return

    # Obtener el ingrediente y su color
    i = animacion_vertido["indice"]
    nombre = bottle_data[i][0]

    color = ingredientes[nombre]["Color"]

    # Punto donde sale el líquido
    inicio = PUNTO_VERTIDO

    # Punto donde llega el líquido
    final = PUNTO_LIQUIDO

    # Animación del chorro
    progreso = (
        tiempo - DURACION_INCLINACION
    ) / DURACION_VERTIDO

    grosor = int(5 + 2 * abs(math.sin(progreso * 15)))

    # Crear superficie transparente
    liquido = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    # Color con transparencia (alfa = 170)
    color_liquido = (*color, 170)

    # Dibujar chorro
    pygame.draw.line(
        liquido,
        color_liquido,
        inicio,
        final,
        grosor
    )
    screen.blit(liquido, (0, 0))



def draw_bottles():

    seleccionada = cola_bebidas.obtener_actual()

    for i in range(len(bottle_images)):

        if (
            animacion_vertido is not None
            and i == animacion_vertido["indice"]
            and animacion_vertido["tipo"] == "botella"
        ):
            continue

        if seleccionada is not None and bottle_indices[seleccionada] == i:

            imagen = bottle_images[i]
            rect = bottle_rects[i]

            width = int(rect.width * ESCALA_SELECCION)
            height = int(rect.height * ESCALA_SELECCION)

            imagen_seleccionada = pygame.transform.smoothscale(
                imagen, (width, height)
            )

            rect_seleccionado = imagen_seleccionada.get_rect(
                center=rect.center
            )

            screen.blit(imagen_seleccionada, rect_seleccionado)

        else:

            screen.blit(bottle_images[i], bottle_rects[i])


def draw_scene():

    screen.blit(background, (0, 0))

    # Objetos que caen y líquido: detrás de las imágenes
    draw_liquido()
    draw_objeto_cayendo()

    draw_bafle()
    draw_bottles()
    draw_bartender()
    draw_coctelera()
    # Botella animada: delante de Jonathan
    draw_bottle_animation()

    draw_lighting()
    draw_buttons()


# =====================================
# BUCLE PRINCIPAL
# =====================================
reproducir_siguiente()
running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == MUSIC_END:
            reproducir_siguiente()

        if event.type == pygame.KEYDOWN:

            if (
                animacion_vertido is None
                and animacion_batido is None
                and animacion_servir is None
            ):
                if event.key == pygame.K_RIGHT:
                    cola_bebidas.siguiente()

                elif event.key == pygame.K_LEFT:
                    cola_bebidas.anterior()

        if event.type == pygame.MOUSEBUTTONDOWN:

            if (
                event.button == 1
                and animacion_vertido is None
                and animacion_batido is None
                and animacion_servir is None
            ):
                for nombre, boton in botones.items():

                    if boton.collidepoint(event.pos):

                        if nombre == "echar":
                            if mezcla_batida == False:
                                echar_ingrediente()

                        elif nombre == "batir":
                            iniciar_batido()

                        elif nombre == "servir":
                            iniciar_servir()
    actualizar_animacion()
    actualizar_batido()
    actualizar_servir()
    draw_scene()

    pygame.display.flip()

    clock.tick(60)


pygame.quit()
sys.exit()
