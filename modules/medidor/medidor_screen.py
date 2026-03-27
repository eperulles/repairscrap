from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.card import MDCard
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from datetime import datetime
import threading

from modules.common.database import (
    get_areas, get_lineas, get_defectos, get_modelos,
    get_supervisores, insert_reparacion
)

class MedidorScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.areas_cache = []
        self.lineas_cache = []
        self.defectos_cache = []
        self.modelos_cache = []
        self.supervisores_cache = []
        self.selected_area_id = None
        self.selected_linea_id = None
        self.selected_defecto_id = None
        self.selected_modelo_id = None
        self.selected_supervisor_id = None
        self.active_menu = None
        self.wasion_blue = get_color_from_hex("#183883")
        self.setup_ui()

    def on_enter(self):
        self.load_data()
        self.setup_ui() # Refrescar UI para ver el modo actual
        Window.bind(on_key_down=self._on_keyboard_down)

    def on_theme_change(self):
        self.setup_ui()

    def on_leave(self):
        Window.unbind(on_key_down=self._on_keyboard_down)
        self.dismiss_menu()

    def _on_keyboard_down(self, window, key, scancode, codepoint, modifier):
        if key == 9: self.focus_next_field_in_list(); return True
        return False

    def focus_next_field_in_list(self):
        self.dismiss_menu()
        fields = [self.transfer_field, self.modelo_field, self.area_field, self.linea_field, self.supervisor_field, self.defecto_field, self.reparacion_field, self.ubicacion_field]
        idx = next((i for i, f in enumerate(fields) if f.focus), None)
        if idx is None: fields[0].focus = True
        else: fields[(idx + 1) % len(fields)].focus = True

    def setup_ui(self):
        self.clear_widgets()
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        current_mode = app.movimiento_tipo
        
        is_dark = self.theme_cls.theme_style == "Dark"
        self.md_bg_color = self.theme_cls.bg_dark if is_dark else self.theme_cls.bg_normal
        main = MDBoxLayout(orientation="vertical")
        header = MDBoxLayout(orientation="horizontal", size_hint_y=None, height="65dp", padding=["15dp", "5dp"], spacing="15dp", md_bg_color=self.wasion_blue)
        header.add_widget(MDIconButton(icon="arrow-left", theme_text_color="Custom", text_color=(1, 1, 1, 1), on_release=lambda x: (setattr(self.manager, 'current', 'menu'))))
        header.add_widget(Image(source="assets/wasion_white.png", size_hint=(None, None), size=("150dp", "45dp"), pos_hint={"center_y": 0.5}, allow_stretch=True, keep_ratio=True))
        
        header_text = f"REGISTRO MEDIDOR ({current_mode.upper()})"
        header.add_widget(MDLabel(text=header_text, font_style="H6", theme_text_color="Custom", text_color=(1, 1, 1, 1), bold=True))
        
        from kivy.uix.scrollview import ScrollView
        scroll = ScrollView(do_scroll_x=False)
        content = MDBoxLayout(orientation="vertical", padding="16dp", spacing="16dp", size_hint_y=None); content.bind(minimum_height=content.setter('height'))
        
        card_bg = (0.05, 0.1, 0.3, 0.8) if is_dark else (0.92, 0.94, 0.96, 1)
        form_card = MDCard(orientation="vertical", padding="24dp", spacing="12dp", radius=[20, 20, 20, 20], md_bg_color=card_bg, elevation=2, size_hint_y=None)
        form_card.bind(minimum_height=form_card.setter('height'))
        
        fill = (0.04, 0.08, 0.22, 1) if is_dark else (1, 1, 1, 1)
        self.transfer_field = self.create_field("Número de Transfer", "barcode-scan", fill)
        form_card.add_widget(self.transfer_field)
        
        grid = MDGridLayout(cols=2, spacing="10dp", size_hint_y=None); grid.bind(minimum_height=grid.setter('height'))
        self.modelo_field = self.create_selectable_field("Modelo", "pencil", fill)
        self.modelo_field.bind(focus=lambda i, v: self.on_select_focus(i, v, self.modelos_cache, "codigo", lambda x: setattr(self, 'selected_modelo_id', x['id'])))
        self.area_field = self.create_selectable_field("Area", "office-building", fill)
        self.area_field.bind(focus=lambda i, v: self.on_select_focus(i, v, self.areas_cache, "nombre", lambda x: setattr(self, 'selected_area_id', x['id'])))
        self.linea_field = self.create_selectable_field("Linea", "access-point", fill)
        self.linea_field.bind(focus=lambda i, v: self.on_select_focus(i, v, self.lineas_cache, "numero", lambda x: setattr(self, 'selected_linea_id', x['id']), num=True))
        self.supervisor_field = self.create_selectable_field("Supervisor", "account-tie", fill)
        self.supervisor_field.bind(focus=lambda i, v: self.on_select_focus(i, v, self.supervisores_cache, "nombre", lambda x: setattr(self, 'selected_supervisor_id', x['id'])))
        grid.add_widget(self.modelo_field); grid.add_widget(self.area_field); grid.add_widget(self.linea_field); grid.add_widget(self.supervisor_field)
        form_card.add_widget(grid)
        
        self.defecto_field = self.create_selectable_field("Tipo de Defecto", "alert", fill)
        self.defecto_field.bind(focus=lambda i,v: self.on_select_focus(i,v, self.defectos_cache, "descripcion", lambda x: setattr(self, 'selected_defecto_id', x['id']), w=4))
        self.reparacion_field = self.create_field("Falla / Reparación", "tools", fill)
        self.ubicacion_field = self.create_field("Ubicación de Falla", "map-marker", fill)
        form_card.add_widget(self.defecto_field); form_card.add_widget(self.reparacion_field); form_card.add_widget(self.ubicacion_field)
        
        btn_text = f"REGISTRAR {current_mode.upper()}"
        self.submit_btn = MDRaisedButton(text=btn_text, size_hint_x=1, height="50dp", md_bg_color=self.wasion_blue, elevation=4)
        self.submit_btn.bind(on_release=self.submit_form)
        self.status_label = MDLabel(text="", theme_text_color="Secondary", font_style="Caption", halign="center")
        
        content.add_widget(form_card); content.add_widget(self.submit_btn); content.add_widget(self.status_label)
        scroll.add_widget(content); main.add_widget(header); main.add_widget(scroll); self.add_widget(main)

    def create_field(self, h, i, f):
        res = MDTextField(hint_text=h, mode="fill", fill_color_normal=f, icon_left=i, write_tab=False)
        res.bind(focus=lambda i, v: self.dismiss_menu() if v else None)
        return res
    def create_selectable_field(self, h, i, f):
        res = MDTextField(hint_text=h, mode="fill", fill_color_normal=f, icon_left=i, readonly=True, write_tab=False)
        return res
    def on_select_focus(self, i, v, data, key, cb, w=3, num=False):
        if v: self.dismiss_menu(); self.show_menu(i, data, key, cb, w, num)
    def show_menu(self, caller, data, key, cb, w, num):
        if not data: return
        items = [{"text": f"Linea {d['numero']}" if num else str(d[key]), "viewclass": "OneLineListItem", "on_release": lambda x=d, c=caller: (cb(x), setattr(c, 'text', str(x['numero'] if num else x[key])), self.dismiss_menu())} for d in data]
        self.active_menu = MDDropdownMenu(items=items, caller=caller, width_mult=w); self.active_menu.open()
    def dismiss_menu(self, *a):
        if self.active_menu: self.active_menu.dismiss(); self.active_menu = None
    def load_data(self):
        def t():
            try:
                self.areas_cache = get_areas(); self.lineas_cache = get_lineas(); self.defectos_cache = get_defectos(); self.modelos_cache = get_modelos(); self.supervisores_cache = get_supervisores()
            except: pass
        threading.Thread(target=t).start()
    def submit_form(self, *a):
        tf = self.transfer_field.text.strip(); from kivymd.app import MDApp; app = MDApp.get_running_app()
        if not tf: self.status_label.text = "Transfer requerido"; return
        u_id = app.user_data.get("id") if app.user_data else None; now = datetime.now()
        hour = now.hour; turno = 1
        if 6 <= hour < 14: turno = 1
        elif 14 <= hour < 22: turno = 2
        else: turno = 3

        data = {
            "tipo_registro": "MEDIDOR", 
            "transfer": tf, 
            "modelo": self.modelo_field.text or None, 
            "fecha": now.strftime("%Y-%m-%d"), 
            "hora": now.strftime("%H:%M:%S"), 
            "turno": turno,
            "area_id": self.selected_area_id, 
            "linea_id": self.selected_linea_id, 
            "defecto_id": self.selected_defecto_id, 
            "reparacion": self.reparacion_field.text.strip() or None, 
            "ubicacion": self.ubicacion_field.text.strip() or None, 
            "supervisor": self.supervisor_field.text or None, 
            "quien_repara_id": u_id,
            "movimiento_tipo": app.movimiento_tipo
        }
        self.submit_btn.disabled = True; threading.Thread(target=self._sub, args=(data,)).start()
    def _sub(self, d):
        r = insert_reparacion(d); from kivy.clock import Clock; Clock.schedule_once(lambda dt: self._res(r), 0)
    def _res(self, r):
        self.status_label.text = "Guardado!" if r else "Error"; self.submit_btn.disabled = False
        if r:
            for f in [self.transfer_field, self.modelo_field, self.area_field, self.linea_field, self.supervisor_field, self.defecto_field, self.reparacion_field, self.ubicacion_field]: f.text = ""
    def go_menu(self): self.manager.current = "menu"
