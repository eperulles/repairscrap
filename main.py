from kivymd.app import MDApp
from kivymd.uix.screenmanager import ScreenManager
from kivy.clock import Clock
from kivy.resources import resource_add_path
import json
import os
import sys

# IMPORTACIONES DE MÓDULOS
from modules.login.login_screen import LoginScreen
from modules.menu.menu_screen import MenuScreen
from modules.pcba.pcba_screen import PCBAScreen
from modules.medidor.medidor_screen import MedidorScreen
from modules.common.update_screen import UpdateScreen
from modules.common.database import get_app_config

class ReparacionesApp(MDApp):
    def build(self):
        # SOPORTE PARA RECURSOS EN PYINSTALLER (.EXE)
        if hasattr(sys, '_MEIPASS'):
            # Si estamos en el EXE, los assets están en '_internal'
            internal_path = os.path.join(sys._MEIPASS, '_internal')
            resource_add_path(internal_path)
            resource_add_path(os.path.join(internal_path, 'assets'))
            resource_add_path(sys._MEIPASS)
        
        self.user_data = None
        # MODO DE REGISTRO (Reparación o Scrap)
        self.movimiento_tipo = "Reparación"
        
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"
        self.theme_cls.accent_palette = "DeepPurple"
        
        self.sm = ScreenManager()
        self.sm.add_widget(LoginScreen(name="login"))
        self.sm.add_widget(MenuScreen(name="menu"))
        self.sm.add_widget(PCBAScreen(name="pcba"))
        self.sm.add_widget(MedidorScreen(name="medidor"))
        self.sm.add_widget(UpdateScreen(name="update"))
        
        return self.sm

    def toggle_mode(self, mode):
        """Cambia entre Reparación y Scrap"""
        self.movimiento_tipo = mode
        print(f"Modo cambiado a: {self.movimiento_tipo}")

    def on_start(self):
        # Programar el chequeo de actualización después de que la app inicie
        Clock.schedule_once(self.check_for_updates, 1)

    def check_for_updates(self, dt):
        try:
            # Leer versión local
            local_version = "1.0.0"
            if os.path.exists("version.json"):
                with open("version.json", "r") as f:
                    local_version = json.load(f).get("version", "1.0.0")
            
            # Consultar Supabase
            remote_config = get_app_config()
            
            if remote_config and remote_config.get("version") != local_version:
                print(f"Update Found: {local_version} -> {remote_config['version']}")
                update_screen = self.sm.get_screen("update")
                update_screen.set_config(remote_config)
                self.sm.current = "update"
        except Exception as e:
            print(f"Error checking for updates: {e}")

    def toggle_theme(self):
        self.theme_cls.theme_style = "Light" if self.theme_cls.theme_style == "Dark" else "Dark"
        for screen in self.sm.screens:
            if hasattr(screen, "on_theme_change"):
                screen.on_theme_change()

if __name__ == "__main__":
    ReparacionesApp().run()
