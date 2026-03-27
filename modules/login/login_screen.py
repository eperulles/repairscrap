from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
import threading

from modules.common.database import login

class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Color Wasion Oficial Extraído: #183883
        self.wasion_blue = get_color_from_hex("#183883")
        self.setup_ui()

    def on_enter(self):
        Window.bind(on_key_down=self._on_keyboard_down)

    def on_leave(self):
        Window.unbind(on_key_down=self._on_keyboard_down)

    def _on_keyboard_down(self, window, key, scancode, codepoint, modifier):
        if key == 9: # TAB
            if self.user_input.focus: self.pass_input.focus = True
            else: self.user_input.focus = True
            return True
        elif key == 13: # ENTER
            self.do_login()
            return True
        return False

    def setup_ui(self):
        self.clear_widgets()
        is_dark = self.theme_cls.theme_style == "Dark"
        self.md_bg_color = self.theme_cls.bg_dark if is_dark else self.theme_cls.bg_normal

        layout = MDBoxLayout(orientation="vertical")
        
        # Fondo superior con el Azul Oficial
        header_bg = MDBoxLayout(size_hint_y=0.4, md_bg_color=self.wasion_blue)
        
        # Card de Login
        card_bg = (0.04, 0.08, 0.22, 1) if is_dark else (1, 1, 1, 1)
        login_card = MDCard(
            orientation="vertical",
            padding="30dp",
            spacing="15dp",
            size_hint=(None, None),
            size=("380dp", "540dp"),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            md_bg_color=card_bg,
            radius=[24, 24, 24, 24],
            elevation=4
        )

        # Logo Blanco Transparente sobre fondo azul de la card o el header
        logo_box = MDBoxLayout(size_hint_y=None, height="120dp", padding="10dp")
        logo = Image(source="assets/wasion_white.png", allow_stretch=True, keep_ratio=True)
        logo_box.add_widget(logo)

        login_card.add_widget(logo_box)
        login_card.add_widget(MDLabel(text="REPARACIONES", halign="center", font_style="H5", bold=True, theme_text_color="Custom", text_color=self.wasion_blue if not is_dark else (1, 1, 1, 1)))
        login_card.add_widget(MDLabel(text="Control de Calidad y Retrabajo", halign="center", font_style="Caption", theme_text_color="Secondary"))

        input_fill = (0.05, 0.1, 0.3, 1) if is_dark else (0.95, 0.95, 0.95, 1)
        self.user_input = MDTextField(hint_text="Usuario", icon_left="account", mode="fill", fill_color_normal=input_fill, write_tab=False)
        self.pass_input = MDTextField(hint_text="Contraseña", icon_left="lock", password=True, mode="fill", fill_color_normal=input_fill, write_tab=False)
        
        # Boton con AZUL OFICIAL
        self.login_btn = MDRaisedButton(text="INICIAR SESIÓN", size_hint_x=1, height="50dp", md_bg_color=self.wasion_blue, elevation=4, on_release=lambda x: self.do_login())
        self.status_label = MDLabel(text="", halign="center", theme_text_color="Error", font_style="Caption")

        login_card.add_widget(self.user_input); login_card.add_widget(self.pass_input); login_card.add_widget(MDBoxLayout(size_hint_y=None, height="10dp")); login_card.add_widget(self.login_btn); login_card.add_widget(self.status_label)
        
        # Superposición
        from kivy.uix.floatlayout import FloatLayout
        root = FloatLayout()
        root.add_widget(MDBoxLayout(orientation="vertical", children=[header_bg, MDBoxLayout(size_hint_y=0.6)]))
        root.add_widget(login_card)
        self.add_widget(root)

    def do_login(self):
        usuario = self.user_input.text.strip(); password = self.pass_input.text.strip()
        if not usuario or not password: self.status_label.text = "Ingresa credenciales"; return
        self.login_btn.disabled = True; self.status_label.text = "Autenticando..."
        threading.Thread(target=self._auth_thread, args=(usuario, password)).start()

    def _auth_thread(self, usuario, password):
        user_data = login(usuario, password)
        def on_auth_result():
            if user_data:
                from kivymd.app import MDApp; MDApp.get_running_app().user_data = user_data
                self.manager.current = "menu"
            else: self.status_label.text = "Error de credenciales"; self.login_btn.disabled = False
        from kivy.clock import Clock; Clock.schedule_once(lambda dt: on_auth_result(), 0)
