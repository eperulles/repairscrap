from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.segmentedcontrol import MDSegmentedControl, MDSegmentedControlItem
from kivy.uix.image import Image
from kivy.utils import get_color_from_hex

class MenuScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wasion_blue = get_color_from_hex("#183883")

    def on_enter(self):
        self.setup_ui()
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        user_name = app.user_name if hasattr(app, 'user_name') else "Administrador"
        if app.user_data: user_name = app.user_data.get("nombre_completo", user_name)
        self.user_name_label.text = user_name

    def on_theme_change(self):
        self.setup_ui()

    def on_segmented_control_active(self, instance_segmented_control, instance_segmented_item):
        """Cambia el modo de registro global de la aplicación."""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        new_mode = instance_segmented_item.text.capitalize()
        if hasattr(app, 'movimiento_tipo') and app.movimiento_tipo != new_mode:
            app.toggle_mode(new_mode)

    def setup_ui(self):
        self.clear_widgets()
        is_dark = self.theme_cls.theme_style == "Dark"
        self.md_bg_color = self.theme_cls.bg_dark if is_dark else self.theme_cls.bg_normal

        main_layout = MDBoxLayout(orientation="vertical")
        header = MDBoxLayout(orientation="horizontal", size_hint_y=None, height="70dp", padding=["20dp", "5dp"], spacing="15dp", md_bg_color=self.wasion_blue)
        header.add_widget(Image(source="assets/wasion_white.png", size_hint=(None, None), size=("150dp", "45dp"), pos_hint={"center_y": 0.5}, allow_stretch=True, keep_ratio=True))
        header.add_widget(MDLabel(text="REPARACIONES", font_style="H6", bold=True, valign="center", theme_text_color="Custom", text_color=(1, 1, 1, 1)))
        header.add_widget(MDBoxLayout())
        self.user_name_label = MDLabel(text="", halign="right", valign="center", theme_text_color="Custom", text_color=(1, 1, 1, 1), font_style="Subtitle2")
        header.add_widget(self.user_name_label)
        header.add_widget(MDIconButton(icon="weather-sunny" if is_dark else "weather-night", pos_hint={"center_y": 0.5}, theme_text_color="Custom", text_color=(1, 1, 1, 1), on_release=lambda x: self.toggle_app_theme()))
        header.add_widget(MDIconButton(icon="logout", pos_hint={"center_y": 0.5}, theme_text_color="Custom", text_color=(1, 1, 1, 1), on_release=lambda x: self.logout()))

        scroll = MDScrollView(do_scroll_x=False)
        content = MDBoxLayout(orientation="vertical", padding="24dp", spacing="20dp", size_hint_y=None); content.bind(minimum_height=content.setter('height'))
        
        greeting = MDBoxLayout(orientation="vertical", size_hint_y=None, height="80dp", spacing="4dp")
        greeting.add_widget(MDLabel(text="Menú de Selección", font_style="H4", bold=True, theme_text_color="Primary"))
        greeting.add_widget(MDLabel(text="Elige el tipo de registro", font_style="Subtitle1", theme_text_color="Secondary"))
        content.add_widget(greeting)

        # CONTROL DE TAB (REPARACIÓN vs SCRAP)
        from kivymd.app import MDApp
        current_mode = MDApp.get_running_app().movimiento_tipo
        
        segmented_control = MDSegmentedControl(
            pos_hint={"center_x": 0.5},
            md_bg_color= (1, 1, 1, 0.1) if is_dark else (0.9, 0.9, 0.9, 1),
            segment_color=self.wasion_blue,
            separator_color=(0, 0, 0, 0)
        )
        rep_item = MDSegmentedControlItem(text="Reparación")
        scrap_item = MDSegmentedControlItem(text="Scrap")
        
        segmented_control.add_widget(rep_item)
        segmented_control.add_widget(scrap_item)
        
        # Seleccionar el activo según el estado global
        if current_mode == "Scrap":
            segmented_control.active_item = scrap_item
        else:
            segmented_control.active_item = rep_item
            
        # Asignar evento DESPUÉS de establecer el estado inicial
        segmented_control.bind(on_active=self.on_segmented_control_active)
        
        content.add_widget(segmented_control)

        grid = MDGridLayout(cols=1, spacing="24dp", size_hint_y=None); grid.bind(minimum_height=grid.setter('height'))
        grid.add_widget(self.create_module_card("PCBA", "assets/pcba_v6.png", "pcba", self.wasion_blue))
        grid.add_widget(self.create_module_card("MEDIDORES", "assets/medidor_v6.png", "medidor", self.wasion_blue))

        content.add_widget(grid)
        scroll.add_widget(content); main_layout.add_widget(header); main_layout.add_widget(scroll); self.add_widget(main_layout)

    def create_module_card(self, title, img, screen, color):
        is_dark = self.theme_cls.theme_style == "Dark"
        bg = (0.04, 0.08, 0.22, 0.8) if is_dark else (1, 1, 1, 1)
        card = MDCard(orientation="horizontal", padding="15dp", spacing="20dp", radius=[20, 20, 20, 20], md_bg_color=bg, elevation=2, size_hint_y=None, height="200dp", on_release=lambda x: self.go_to(screen), ripple_behavior=True)
        img_box = MDBoxLayout(size_hint=(0.4, 1), padding="5dp")
        img_box.add_widget(Image(source=img, allow_stretch=True, keep_ratio=True, size_hint=(1, 1)))
        card.add_widget(img_box)
        txt = MDBoxLayout(orientation="vertical", size_hint=(0.6, 1), padding=["0dp", "20dp"])
        txt.add_widget(MDLabel(text=title, font_style="H4", bold=True, theme_text_color="Custom", text_color=color))
        txt.add_widget(MDLabel(text="Registro de entrada industrial", font_style="Body1", theme_text_color="Secondary"))
        card.add_widget(txt)
        return card

    def toggle_app_theme(self): 
        from kivymd.app import MDApp; MDApp.get_running_app().toggle_theme()
    def go_to(self, screen): self.manager.current = screen
    def logout(self): 
        from kivymd.app import MDApp; MDApp.get_running_app().user_data = None
        self.manager.current = "login"
