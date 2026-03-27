from supabase import create_client, Client
from config.settings import SUPABASE_URL, SUPABASE_KEY

_client: Client = None

def get_client() -> Client:
    global _client
    if _client is None:
        _client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _client

def login(usuario: str, contrasena: str) -> dict | None:
    client = get_client()
    response = client.table("usuarios").select("*").eq("usuario", usuario).eq("contrasena", contrasena).eq("activo", True).execute()
    if response.data:
        return response.data[0]
    return None

def get_areas() -> list:
    client = get_client()
    response = client.table("areas").select("*").eq("activo", True).execute()
    return response.data

def get_lineas(area_id: int = None) -> list:
    client = get_client()
    query = client.table("lineas").select("*, areas(nombre)").eq("activo", True)
    if area_id:
        query = query.eq("area_id", area_id)
    response = query.execute()
    return response.data

def get_defectos(area_id: int = None) -> list:
    client = get_client()
    query = client.table("defectos").select("*").eq("activo", True)
    if area_id:
        query = query.eq("area_id", area_id)
    response = query.execute()
    return response.data

def get_usuarios() -> list:
    client = get_client()
    response = client.table("usuarios").select("id, nombre_completo").eq("activo", True).execute()
    return response.data

def insert_reparacion(data: dict) -> dict | None:
    client = get_client()
    try:
        response = client.table("reparaciones").insert(data).execute()
        if hasattr(response, 'data') and response.data:
            return response.data[0]
        else:
            print(f"Insert Error: No data returned. Response: {response}")
    except Exception as e:
        print(f"Database Insert Exception: {e}")
    return None

def get_supervisores() -> list:
    client = get_client()
    response = client.table("supervisores").select("*").eq("activo", True).execute()
    return response.data

def get_modelos() -> list:
    client = get_client()
    response = client.table("modelos").select("*").eq("activo", True).execute()
    return response.data

def get_app_config() -> dict | None:
    """Obtiene la configuración de la versión más reciente en Supabase."""
    client = get_client()
    try:
        response = client.table("config_app").select("*").order("created_at", desc=True).limit(1).execute()
        if response.data:
            return response.data[0]
    except Exception as e:
        print(f"Update Check Error: {e}")
    return None
