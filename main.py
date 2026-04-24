"""
Alexis Rojas Rodríguez 6IV6
Interfaz gráfica para consultas de Spotify
Basado en un proyecto anterior pero adaptado para este nuevo dataset :D

Sistema de navegación entre frames para mostrar diferentes pantallas:
- Login: Inicio de sesión con validación
- Menú: Selección de consultas
- Consulta: Muestra la gráfica de cada consulta
- Justificación: Explica el propósito de cada consulta

Usuario: usuario
Contraseña: contrasena
"""

# Custom tkinter para la interfaz grafica
from CTkMessagebox import CTkMessagebox
import customtkinter as ctk

# Matplotlib para las graficas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Modulo de consultas
import consultas_spotify as cons

# OS para leer archivos del sistema
import os

# Ignorar advertencias molestas de matplotlib (como los "Glyph missing")
# Esto lo vi porque mi terminal estaba muy sucia y lo vi en internet jeje
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Tema oscuro para que se vea nice
ctk.set_appearance_mode("dark")

# Color azul para los widgets
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    """
    Clase principal de la aplicacion
    Maneja la navegacion entre diferentes frames
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Título de la ventana
        self.title("Consultas Spotify")
        # Tamaño de la ventana un poco más grande para que entren las gráficas
        self.geometry("1400x800")
        self.current_frame = None
        # Arrancamos con el login
        self.show_frame(LoginFrame)

    def show_frame(self, frame_class, *args, **kwargs):
        """
        Método para cambiar entre frames
        Destruye el frame actual y crea el nuevo
        """
        if self.current_frame is not None:
            self.current_frame.destroy()

        # Creamos el nuevo frame
        self.current_frame = frame_class(self, *args, **kwargs)
        self.current_frame.pack(fill="both", expand=True)


class LoginFrame(ctk.CTkFrame):
    """
    Frame de inicio de sesión
    Valida las credenciales contra el archivo users.txt
    """

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master

        # Título del login
        self.title_label = ctk.CTkLabel(self, text="Inicio de Sesión", font=("Arial", 24))
        self.title_label.pack(pady=30)

        # Etiqueta y campo de usuario
        self.username_label = ctk.CTkLabel(self, text="Usuario:")
        self.username_label.pack(pady=10)
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Ingrese usuario", width=250)
        self.username_entry.pack(pady=5)

        # Etiqueta y campo de contraseña
        self.password_label = ctk.CTkLabel(self, text="Contraseña:")
        self.password_label.pack(pady=10)
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Ingrese contraseña", show="*", width=250)
        self.password_entry.pack(pady=5)

        # Botón de inicio de sesión
        self.login_button = ctk.CTkButton(self, text="Iniciar Sesión", command=self.login, width=200, height=40)
        self.login_button.pack(pady=30)

    def leer_usuarios(self):
        """
        Lee el archivo de usuarios y retorna una lista con las credenciales
        """
        if not os.path.exists("users.txt"):
            return []

        datos_usuario = []
        with open("users.txt", "r") as f:
            for linea in f:
                linea = linea.strip().split(",")
                usuario, contrasena = linea[0], linea[1]
                datos_usuario.append((usuario, contrasena))
        return datos_usuario

    def login(self):
        """
        Valida las credenciales ingresadas
        """
        usuario = self.username_entry.get()
        contrasena = self.password_entry.get()
        datos = self.leer_usuarios()

        if not datos:
            self.mensaje_error("Archivo de usuarios no encontrado")
            return

        # Verificamos las credenciales
        if usuario == datos[0][0] and contrasena == datos[0][1]:
            self.master.show_frame(MenuFrame)
        else:
            self.mensaje_error("Usuario o contraseña incorrecta")

    def mensaje_error(self, mensaje):
        """
        Muestra un mensaje de error en una ventana emergente
        """
        CTkMessagebox(title="Error", message=mensaje, icon="cancel", option_1="Aceptar")


class MenuFrame(ctk.CTkFrame):
    """
    Frame del menú principal
    Muestra los botones para seleccionar cada consulta
    """

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master

        # Título del menú
        self.titulo = ctk.CTkLabel(self, text="Seleccione una consulta", font=("Arial", 22))
        self.titulo.pack(pady=20)

        # Cargamos los datos al iniciar
        self.datos = cons.cargar_datos()

        # Contenedor para los botones
        self.botones_frame = ctk.CTkFrame(self)
        self.botones_frame.pack(pady=20, padx=20, expand=True)

        # Lista de botones para las 12 consultas
        botones_consulta = [
            ("Top Populares", lambda: self.master.show_frame(ConsultaFrame, cons.canciones_populares(self.datos))),
            ("Top Seguidores", lambda: self.master.show_frame(ConsultaFrame, cons.artistas_seguidores(self.datos))),
            ("Duración Canciones", lambda: self.master.show_frame(ConsultaFrame, cons.duracion_canciones(self.datos))),
            ("Top Géneros", lambda: self.master.show_frame(ConsultaFrame, cons.generos_comunes(self.datos))),
            ("Tipos de Álbum", lambda: self.master.show_frame(ConsultaFrame, cons.albums_por_tipo(self.datos))),
            ("Pop. Artista vs Canción", lambda: self.master.show_frame(ConsultaFrame, cons.popularidad_relacion(self.datos))),
            ("Explícitas vs No", lambda: self.master.show_frame(ConsultaFrame, cons.canciones_explicitas(self.datos))),
            ("Top Artistas", lambda: self.master.show_frame(ConsultaFrame, cons.top_artistas_popularidad(self.datos))),
            ("Álbumes más Pistas", lambda: self.master.show_frame(ConsultaFrame, cons.albums_mas_pistas(self.datos))),
            ("Duración por Género", lambda: self.master.show_frame(ConsultaFrame, cons.duracion_promedio_genero(self.datos))),
            ("Álbumes Recientes", lambda: self.master.show_frame(ConsultaFrame, cons.albums_recientes(self.datos))),
            ("Álbumes vs Sencillos", lambda: self.master.show_frame(ConsultaFrame, cons.albums_vs_singles(self.datos))),
        ]

        # Creamos dos filas de 6 botones cada una
        for i, (texto, comando) in enumerate(botones_consulta):
            fila = i // 6
            columna = i % 6
            boton = ctk.CTkButton(self.botones_frame, text=texto, command=comando, width=140, height=55)
            boton.grid(row=fila, column=columna, padx=15, pady=15, sticky="nsew")

        # Botón para cerrar sesión
        self.boton_salir = ctk.CTkButton(self, text="Cerrar Sesión", command=lambda: self.master.show_frame(LoginFrame))
        self.boton_salir.pack(pady=20)


class ConsultaFrame(ctk.CTkFrame):
    """
    Frame que muestra la gráfica de cada consulta
    """

    def __init__(self, master, ref_consulta, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master

        # Título de la consulta
        self.titulo_label = ctk.CTkLabel(self, text="Consulta", font=("Arial", 20))
        self.titulo_label.pack(pady=20)

        # Obtenemos la figura y el argumento de la consulta
        fig, argumento = ref_consulta

        # Creamos un canvas para mostrar la gráfica
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=10)

        # Frame para los botones
        self.frame_botones = ctk.CTkFrame(self)

        # Botón de justificación
        self.boton_justificacion = ctk.CTkButton(self.frame_botones, text="Justificación", command=lambda: self.mostrar_justificacion(argumento))

        # Botón para volver
        self.boton_volver = ctk.CTkButton(self.frame_botones, text="Volver", command=self.volver)

        self.boton_volver.grid(row=0, column=0, padx=10)
        self.boton_justificacion.grid(row=0, column=1, padx=10)
        self.frame_botones.pack(pady=20)

    def volver(self):
        """
        Regresa al menú principal
        """
        self.master.show_frame(MenuFrame)

    def mostrar_justificacion(self, texto):
        """
        Muestra el frame de justificación con el texto correspondiente
        """
        self.master.show_frame(JustificacionFrame, texto)


class JustificacionFrame(ctk.CTkFrame):
    """
    Frame que muestra la justificación de cada consulta
    """

    def __init__(self, master, texto, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master

        # Título de la justificación
        self.titulo_label = ctk.CTkLabel(self, text="Justificación", font=("Arial", 20))
        self.titulo_label.pack(pady=20)

        # Caja de texto para mostrar la justificación
        self.caja_texto = ctk.CTkTextbox(self, activate_scrollbars=True)
        self.caja_texto.pack(pady=20, padx=20, expand=True)

        # Insertamos el texto
        self.caja_texto.insert("1.0", texto)
        self.caja_texto.configure(state="disabled")

        # Botón para volver
        self.boton_volver = ctk.CTkButton(self, text="Volver", command=lambda: self.master.show_frame(MenuFrame))
        self.boton_volver.pack(pady=20)


# Ejecucion principal de la aplicacion (naiiiis)
if __name__ == "__main__":
    app = App()
    app.mainloop()  

