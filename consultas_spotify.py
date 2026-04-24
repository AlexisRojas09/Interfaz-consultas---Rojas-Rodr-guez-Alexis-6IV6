"""
Módulo de consultas para el proyecto de interfaz gráfica
Basado en un proyecto anterior pero adaptado para usar datos de Spotify :D

Consultas disponibles:
1. Canciones más populares (barras)
2. Artistas con más seguidores (pie)
3. Duración de canciones en minutos (barras)
4. Géneros más comunes (pie)
5. Álbumes por tipo (pie)
6. Relación popularidad artista vs canción (dispersión)
7. Canciones explícitas vs no explícitas (pie)
8. Top 10 artistas por popularidad (barras)
9. Álbumes con más pistas (barras)
10. Duración promedio por género (barras)
11. Álbumes más recientes (barras)
12. Comparación álbumes vs singles (barras)

Autor: Alexis Rojas Rodríguez 6IV6
Fecha: 2026

Antes de empezar quiero aclaras que usé subplots y variables fig y ax (que no hemos visto en clase de IA)
porque las aprendimos en análisis de datos
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def cargar_datos():
    """
    Carga los datos del CSV de Spotify y hace una limpieza básica
    Returns:
        df: DataFrame completo
        canciones: DataFrame con solo las canciones
    """
    # Leemos el csv con los datos de Spotify
    df = pd.read_csv("track_data_final.csv")

    # Limpiamos datos importantes que no pueden estar vacíos
    df = df.dropna(subset=['track_name', 'artist_name', 'track_popularity'])

    # Convertimos la duración de ms a minutos para mejor lectura
    df['duration_min'] = df['track_duration_ms'] / 60000

    return df


# 1. Canciones más populares (barras)
def canciones_populares(canciones):
    """
    Muestra las 10 canciones con mayor popularidad
    Args:
        canciones: DataFrame con los datos de Spotify
    Returns:
        fig: Gráfica de matplotlib
        argumento: Descripción de la consulta
    """
    # Obtenemos las 10 canciones más populares
    top_canciones = canciones.nlargest(10, 'track_popularity')[['track_name', 'track_popularity']]
    top_canciones = top_canciones.sort_values('track_popularity', ascending=True)

    # Creamos la gráfica con tamaño más grande (Estas funciones las hicimos en análisis de datos :D, por si se ven avanzadas o algo que no vimos en clase)
    fig, ax = plt.subplots(figsize=(12, 8))
    colores = ['#ff9ff3', '#feca57', '#ff6b6b', '#48dbfb', '#1dd1a1', '#5f27cd', '#c8d6e5', '#576574', '#ff9f43', '#0abde3']
    ax.barh(top_canciones['track_name'], top_canciones['track_popularity'], color=colores)

    # Ajustamos el tamaño para que se vea bien el texto
    fig.subplots_adjust(left=0.4)
    ax.set_title("Top 10 canciones más populares")
    ax.set_xlabel("Popularidad")
    ax.set_ylabel("Canción")
    plt.close(fig)

    # Descripción de la consulta
    argumento = "Esta gráfica muestra las canciones con mayor popularidad en la plataforma, " \
    "esto para identificar qué tipo de contenido tiene mayor aceptacion entre los usuarios. " \
    "La popularidad es un valor de 0 a 100 que indica qué tan escuchada es una canción."

    return fig, argumento


# 2. Artistas con más seguidores (pie)
def artistas_seguidores(canciones):
    """
    Muestra los artistas con más seguidores en formato circular
    Args:
        canciones: DataFrame con los datos de Spotify
    Returns:
        fig: Gráfica de matplotlib
        argumento: Descripción de la consulta
    """
    # Obtenemos los artistas únicos y sus seguidores
    artistas_unicos = canciones.drop_duplicates(subset=['artist_name'])[['artist_name', 'artist_followers']]
    top_artistas = artistas_unicos.nlargest(10, 'artist_followers')

    # Creamos la gráfica de pastel con tamaño grande
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.pie(top_artistas['artist_followers'], labels=top_artistas['artist_name'], autopct='%1.1f%%')
    ax.set_title("Top 10 artistas con más seguidores")
    plt.close(fig)

    # Descripción de la consulta
    argumento = "Esta gráfica muestra los artistas con mayor cantidad de seguidores en la plataforma. " \
    "Es útil para identificar qué artistas tienen la base de fans más grande y " \
    "como se distribuye la popularidad entre diferentes músicos."

    return fig, argumento


# 3. Duración de canciones en minutos (barras)
def duracion_canciones(canciones):
    """
    Muestra la distribución de duración de las canciones
    Args:
        canciones: DataFrame con los datos de Spotify
    Returns:
        fig: Gráfica de matplotlib
        argumento: Descripción de la consulta
    """
    # Creamos categorias de duración
    menos_3 = canciones[canciones['duration_min'] < 3].shape[0]
    entre_3_5 = canciones[(canciones['duration_min'] >= 3) & (canciones['duration_min'] < 5)].shape[0]
    mas_5 = canciones[canciones['duration_min'] >= 5].shape[0]

    duraciones = np.array([menos_3, entre_3_5, mas_5])
    etiquetas = ['Menos de 3 min', '3-5 min', 'Mas de 5 min']

    # Creamos la gráfica
    fig, ax = plt.subplots(figsize=(12, 8))
    colores = ['#ff9ff3', '#feca57', '#ff6b6b']
    ax.bar(etiquetas, duraciones, color=colores)
    ax.set_title("Distribución de duración de canciones")
    ax.set_xlabel("Rango de duración")
    ax.set_ylabel("Cantidad de canciones")
    plt.close(fig)

    # Descripción de la consulta
    argumento = "Esta gráfica muestra la distribución de duración de las canciones en la base de datos. " \
    "Permite ver si predominan las canciones cortas, medianas o largas, lo cual " \
    "puede indicar las preferencias de los artistas en cuanto a la duración de sus temas."

    return fig, argumento


# 4. Géneros más comunes (pie)
def generos_comunes(canciones):
    """
    Muestra los géneros musicales más comunes
    Args:
        canciones: DataFrame con los datos de Spotify
    Returns:
        fig: Gráfica de matplotlib
        argumento: Descripción de la consulta
    """
    # Contamos los géneros (vienen en formato lista)
    géneros = []
    for g in canciones['artist_genres'].dropna():
        # Limpiamos los corchetes y comillas
        g_limpio = g.replace('[', '').replace(']', '').replace("'", "").replace('"', '')
        if g_limpio:
            géneros.append(g_limpio.strip())

    # Contamos cada género
    from collections import Counter
    conteo_generos = Counter(géneros)
    top_generos = dict(conteo_generos.most_common(10))

    # Creamos la gráfica
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.pie(list(top_generos.values()), labels=list(top_generos.keys()), autopct='%1.1f%%')
    ax.set_title("Top 10 géneros musicales")
    plt.close(fig)

    # Descripción de la consulta
    argumento = "Esta gráfica muestra los géneros musicales más comunes entre los artistas. " \
    "Es útil para entender qué tipos de música predominan en la plataforma " \
    "y como está distribuida la diversidad musical."

    return fig, argumento


# 5. Álbumes por tipo (pie)
def albums_por_tipo(canciones):
    """
    Muestra la distribución de tipos de álbumes
    Args:
        canciones: DataFrame con los datos de Spotify
    Returns:
        fig: Gráfica de matplotlib
        argumento: Descripción de la consulta
    """
    # Contamos los tipos de album
    tipos = canciones['album_type'].value_counts()

    # Creamos la gráfica
    fig, ax = plt.subplots(figsize=(12, 8))
    tipos.plot(kind='pie', ax=ax, autopct='%1.1f%%')
    ax.set_title("Distribución de álbumes por tipo")
    ax.set_ylabel("")
    plt.close(fig)

    # Descripción de la consulta
    argumento = "Esta gráfica muestra la distribución de álbumes, singles y compilations " \
    "en la base de datos. Permite ver si hay más álbumes completos, sencillos " \
    "o colecciones de exitos."

    return fig, argumento


# 6. Relación popularidad artista vs canción (dispersión)
def popularidad_relacion(canciones):
    """
    Muestra la relación entre popularidad del artista y la canción
    Args:
        canciones: DataFrame con los datos de Spotify
    Returns:
        fig: Gráfica de matplotlib
        argumento: Descripción de la consulta
    """
    # Creamos la gráfica de dispersión (scatter)
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Reducimos el tamaño de los puntos (s=15) y añadimos transparencia (alpha=0.3) 
    # para que se aprecie dónde hay mayor concentración de datos
    ax.scatter(canciones['artist_popularity'], canciones['track_popularity'], alpha=0.3, s=15, color='#8e44ad')

    ax.set_title("Relación: Popularidad del artista vs canción")
    ax.set_xlabel("Popularidad del artista")
    ax.set_ylabel("Popularidad de la canción")
    ax.grid(True, linestyle='--', alpha=0.7) # Añadir cuadricula para mejor lectura
    plt.close(fig)

    # Descripción de la consulta
    argumento = "Esta es una gráfica de dispersión pero de tipo scatter plot (La vi en la documentación y me gustó :D). Cada puntito representa una canción, " \
    "su posición horizontal indica qué tan popular es el artista, y su vertical qué tan popular es esa canción en específico. " \
    "Al poner miles de puntos juntos, las zonas más oscuras nos dicen dónde se concentra la mayoría de la música. " \
    "Sirve para ver si obligatoriamente un artista muy famoso siempre tiene canciones súper famosas."

    return fig, argumento


# 7. Canciones explícitas vs no explícitas (pie)
def canciones_explicitas(canciones):
    """
    Muestra la distribución de canciones explícitas
    Args:
        canciones: DataFrame con los datos de Spotify
    Returns:
        fig: Gráfica de matplotlib
        argumento: Descripción de la consulta
    """
    # Contamos explícitas
    explícitas = canciones[canciones['explicit'] == True].shape[0]
    no_explicitas = canciones[canciones['explicit'] == False].shape[0]

    datos = np.array([explícitas, no_explicitas])
    etiquetas = ['Explícitas', 'No explícitas']

    # Creamos la gráfica
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.pie(datos, labels=etiquetas, autopct='%1.1f%%', colors=['#ff6b6b', '#4ecdc4'])
    ax.set_title("Canciones explícitas vs no explícitas")
    plt.close(fig)

    # Descripción de la consulta
    argumento = "Esta gráfica muestra la proporción de canciones con contenido explicito " \
    "versus aquellas sin el. Es útil para entender qué tipo de contenido " \
    "predomina en la plataforma."

    return fig, argumento


# 8. Top 10 artistas por popularidad (barras)
def top_artistas_popularidad(canciones):
    """
    Muestra los artistas con mayor popularidad
    Args:
        canciones: DataFrame con los datos de Spotify
    Returns:
        fig: Gráfica de matplotlib
        argumento: Descripción de la consulta
    """
    # Obtenemos artistas únicos y su popularidad
    artistas_unicos = canciones.drop_duplicates(subset=['artist_name'])[['artist_name', 'artist_popularity']]
    top_10 = artistas_unicos.nlargest(10, 'artist_popularity')
    top_10 = top_10.sort_values('artist_popularity', ascending=True)

    # Creamos la gráfica
    fig, ax = plt.subplots(figsize=(12, 8))
    colores = ['#1abc9c', '#2ecc71', '#3498db', '#9b59b6', '#34495e', '#f1c40f', '#e67e22', '#e74c3c', '#ecf0f1', '#95a5a6']
    ax.barh(top_10['artist_name'], top_10['artist_popularity'], color=colores)

    fig.subplots_adjust(left=0.3)
    ax.set_title("Top 10 artistas por popularidad")
    ax.set_xlabel("Popularidad")
    ax.set_ylabel("Artista")
    plt.close(fig)

    # Descripción de la consulta
    argumento = "Esta gráfica muestra los 10 artistas con mayor indice de popularidad " \
    "en la plataforma. La popularidad del artista es un valor calculado por Spotify " \
    "basado en el número de reproducciones y otros factores."

    return fig, argumento


# 9. Álbumes con más pistas (barras)
def albums_mas_pistas(canciones):
    """
    Muestra los álbumes con más canciones
    Args:
        canciones: DataFrame con los datos de Spotify
    Returns:
        fig: Gráfica de matplotlib
        argumento: Descripción de la consulta
    """
    # Obtenemos álbumes únicos con su número de pistas
    albums_unicos = canciones.drop_duplicates(subset=['album_id'])[['album_name', 'album_total_tracks']]
    
    # Filtramos álbumes que tengan nombres en blanco o con puros caracteres que matplotlib no renderiza bien (como japonés/coreano) 
    # Si al pasarlo a ASCII queda vacío, lo ignoramos para la gráfica
    # Aquí la verdad si me quedé pensando un rato :/, le pedí ayuda a la IA porque de plano no pude y me ayudó a encontrar esta solución
    albums_unicos = albums_unicos[albums_unicos['album_name'].apply(lambda x: len(str(x).encode('ascii', 'ignore').strip()) > 0)]
    
    top_albums = albums_unicos.nlargest(10, 'album_total_tracks')
    top_albums = top_albums.sort_values('album_total_tracks', ascending=True)

    # Creamos la gráfica
    fig, ax = plt.subplots(figsize=(12, 8))
    colores = ['#ff7979', '#badc58', '#dff9fb', '#f6e58d', '#ffbe76', '#e056fd', '#686de0', '#30336b', '#95afc0', '#22a6b3']
    ax.barh(top_albums['album_name'], top_albums['album_total_tracks'], color=colores)

    fig.subplots_adjust(left=0.4)
    ax.set_title("Top 10 álbumes con más pistas")
    ax.set_xlabel("Numero de pistas")
    ax.set_ylabel("Album")
    plt.close(fig)

    # Descripción de la consulta
    argumento = "Esta gráfica muestra los álbumes con mayor cantidad de canciones. " \
    "Es útil para identificar que álbumes tienen más contenido " \
    "y si hay una correlacion entre el tamaño del album y su popularidad."

    return fig, argumento


# 10. Duración promedio por género (barras)
def duracion_promedio_genero(canciones):
    """
    Muestra la duración promedio de canciones por género
    Args:
        canciones: DataFrame con los datos de Spotify
    Returns:
        fig: Gráfica de matplotlib
        argumento: Descripción de la consulta
    """
    # Limpiamos los géneros
    generos_limpios = []
    duraciones = []

    for idx, row in canciones.iterrows():
        if pd.notna(row['artist_genres']):
            g = row['artist_genres'].replace('[', '').replace(']', '').replace("'", "").strip()
            if g:
                generos_limpios.append(g)
                duraciones.append(row['duration_min'])

    # Creamos un dataframe temporal
    temp_df = pd.DataFrame({'género': generos_limpios, 'duración': duraciones})
    duracion_promedio = temp_df.groupby('género')['duración'].mean().sort_values(ascending=False).head(10)

    # Creamos la gráfica
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.subplots_adjust(bottom=0.5)
    colores = ['#55efc4', '#81ecec', '#74b9ff', '#a29bfe', '#dfe6e9', '#ffeaa7', '#fab1a0', '#ff7675', '#fd79a8', '#fdcb6e']
    duracion_promedio.plot(kind='bar', ax=ax, color=colores)
    ax.set_title("Duración promedio por género (minutos)")
    ax.set_xlabel("Género")
    ax.set_ylabel("Duración promedio (min)")
    ax.tick_params(axis='x', rotation=45)
    plt.close(fig)

    # Descripción de la consulta
    argumento = "Esta gráfica muestra la duración promedio de las canciones " \
    "para cada género musical. Permite identificar si algunos géneros " \
    "tienden a tener canciones más largas que otros."

    return fig, argumento


# 11. Álbumes más recientes (barras)
def albums_recientes(canciones):
    """
    Muestra los álbumes más recientes por fecha de lanzamiento
    Args:
        canciones: DataFrame con los datos de Spotify
    Returns:
        fig: Gráfica de matplotlib
        argumento: Descripción de la consulta
    """
    # Convertimos la fecha a formato datetime
    canciones['album_release_date'] = pd.to_datetime(canciones['album_release_date'], errors='coerce')

    # Obtenemos álbumes únicos y ordenamos por fecha
    albums_unicos = canciones.drop_duplicates(subset=['album_id'])[['album_name', 'album_release_date']]
    albums_recientes = albums_unicos.dropna().nlargest(10, 'album_release_date')

    # Extraemos el año para mejor visualizacion
    albums_recientes['año'] = albums_recientes['album_release_date'].dt.year

    # Creamos la gráfica
    fig, ax = plt.subplots(figsize=(12, 8))
    colores = ['#e55039', '#4a69bd', '#60a3bc', '#78e08f', '#f8c291', '#b71540', '#0a3d62', '#079992', '#38ada9', '#e58e26']
    ax.barh(albums_recientes['album_name'], albums_recientes['año'], color=colores)
    fig.subplots_adjust(left=0.4)
    ax.set_title("Top 10 álbumes más recientes")
    ax.set_xlabel("Año de lanzamiento")
    ax.set_ylabel("Album")
    plt.close(fig)

    # Descripción de la consulta
    argumento = "Esta gráfica muestra los álbumes más recientes en la base de datos. " \
    "Permite identificar que álbumes son los últimos lanzamientos " \
    "y ver la distribución temporal del contenido."

    return fig, argumento


# 12. Comparación álbumes vs singles (barras)
def albums_vs_singles(canciones):
    """
    Compara la cantidad de álbumes completos vs singles
    Args:
        canciones: DataFrame con los datos de Spotify
    Returns:
        fig: Gráfica de matplotlib
        argumento: Descripción de la consulta
    """
    # Filtramos solo álbumes y singles
    álbumes = canciones[canciones['album_type'] == 'album'].shape[0]
    singles = canciones[canciones['album_type'] == 'single'].shape[0]
    compilations = canciones[canciones['album_type'] == 'compilation'].shape[0]

    datos = np.array([álbumes, singles, compilations])
    etiquetas = ['Álbumes', 'Singles', 'Compilations']

    # Creamos la gráfica
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.bar(etiquetas, datos, color=['#3498db', '#e74c3c', '#2ecc71'])
    ax.set_title("Comparación: Álbumes vs Singles vs Compilations")
    ax.set_xlabel("Tipo de contenido")
    ax.set_ylabel("Cantidad")
    plt.close(fig)

    # Descripción de la consulta
    argumento = "Esta gráfica compara la cantidad de álbumes completos, singles " \
    "y compilations en la base de datos. Permite ver qué tipo de contenido " \
    "es más comun entre los artistas."

    return fig, argumento


# Fin del modulo de consultas :D
