from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.progressbar import MDProgressBar
from kivy.uix.image import Image
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
import json
import threading
import requests
import os
import subprocess
import sys

class UpdateScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wasion_blue = get_color_from_hex("#183883")
        self.config_data = None
        self.setup_ui()

    def setup_ui(self):
        self.md_bg_color = (1, 1, 1, 1) # Fondo blanco industrial
        
        main = MDBoxLayout(orientation="vertical", padding="40dp", spacing="20dp")
        
        # Logo Wasion
        main.add_widget(Image(source="assets/wasion-ltd--600.png", size_hint=(None, None), size=("200dp", "80dp"), pos_hint={"center_x": 0.5}))
        
        self.title_label = MDLabel(text="Nueva Actualización Disponible", font_style="H5", halign="center", bold=True, theme_text_color="Primary")
        main.add_widget(self.title_label)
        
        self.version_label = MDLabel(text="Versión detectada: --", halign="center", font_style="Subtitle1", theme_text_color="Secondary")
        main.add_widget(self.version_label)
        
        self.changelog_label = MDLabel(text="Mejoras y correcciones en esta versión.", halign="center", font_style="Body2", theme_text_color="Secondary")
        main.add_widget(self.changelog_label)
        
        self.progress_bar = MDProgressBar(value=0, size_hint_x=0.8, pos_hint={"center_x": 0.5}, color=self.wasion_blue)
        self.progress_bar.opacity = 0
        main.add_widget(self.progress_bar)
        
        self.btn_layout = MDBoxLayout(orientation="horizontal", spacing="20dp", size_hint=(None, None), size=("300dp", "50dp"), pos_hint={"center_x": 0.5})
        
        self.update_btn = MDRaisedButton(text="ACTUALIZAR AHORA", md_bg_color=self.wasion_blue, on_release=self.start_download)
        self.cancel_btn = MDFlatButton(text="MÁS TARDE", on_release=self.go_login)
        
        self.btn_layout.add_widget(self.update_btn)
        self.btn_layout.add_widget(self.cancel_btn)
        main.add_widget(self.btn_layout)
        
        self.add_widget(main)

    def set_config(self, config):
        self.config_data = config
        self.version_label.text = f"Versión detectada: {config['version']}"
        if config.get('changelog'):
            self.changelog_label.text = config['changelog']
        if config.get('is_mandatory'):
            self.cancel_btn.disabled = True

    def start_download(self, *args):
        self.update_btn.disabled = True
        self.cancel_btn.disabled = True
        self.progress_bar.opacity = 1
        self.title_label.text = "Descargando Actualización..."
        
        threading.Thread(target=self.download_task).start()

    def download_task(self):
        url = self.config_data['download_url']
        filename = "reparaciones_update.exe" # O .zip dependiendo del caso
        
        try:
            response = requests.get(url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=4096):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            Clock.schedule_once(lambda dt, p=percent: setattr(self.progress_bar, 'value', p))
            
            Clock.schedule_once(lambda dt: self.finalize_update(filename))
        except Exception as e:
            Clock.schedule_once(lambda dt: self.show_error(str(e)))

    def finalize_update(self, filename):
        self.title_label.text = "¡Descarga Completa!"
        self.changelog_label.text = "La aplicación se reiniciará para aplicar los cambios."
        
        # Aquí crearíamos un script bootstrap de reemplazo
        # Por simplicidad, avisamos al usuario o lanzamos un script de instalación
        # En Windows: 'start installer.exe'
        Clock.schedule_once(lambda dt: self.execute_replacement(filename), 2)

    def execute_replacement(self, filename):
        # Lógica de reemplazo (Bootstrap)
        # Esto depende de si el usuario está usando EXE o scripts
        # Si es EXE, lanzamos el instalador y cerramos la app actual
        print(f"Reemplazando con {filename}")
        # subprocess.Popen([filename])
        # sys.exit(0)
        self.manager.current = "login"

    def go_login(self, *args):
        self.manager.current = "login"

    def show_error(self, err):
        self.title_label.text = "Error al Actualizar"
        self.changelog_label.text = err
        self.update_btn.disabled = False
        self.cancel_btn.disabled = False
