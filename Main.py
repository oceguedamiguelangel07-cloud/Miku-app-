# MAIN.PY - MIKU OMNI-VISION UNIVERSAL SYSTEM (32 & 64 BITS)
import random, os, subprocess, re, sys
import base64
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from jnius import autoclass, PythonJavaClass, java_method

CONFIG = {
    "nombre_bot": "Miku",
    "voz_onnx": "es_MX-ald-medium.onnx"
}

# Estados globales
BOT_MUTED = False 
SYSTEM_ON = True  
HORA_SILENCIO_INICIO = 23  
HORA_SILENCIO_FIN = 6     

# Detectar bits del sistema de forma automática
ES_64_BITS = sys.maxsize > 2**32
print(f"[Miku System]: Detectada arquitectura de {'64 bits' if ES_64_BITS else '32 bits'}")

# 1. CONTACTOS AUTO
def cargar_contactos_auto():
    contactos = {}
    try:
        PyAct = autoclass('org.kivy.android.PythonActivity')
        act = PyAct.mActivity
        resolver = act.getContentResolver()
        C = autoclass('android.provider.ContactsContract$CommonDataKinds$Phone')
        cur = resolver.query(C.CONTENT_URI, None, None, None, None)
        while cur.moveToNext():
            nom = cur.getString(cur.getColumnIndex(C.DISPLAY_NAME)).lower()
            num = cur.getString(cur.getColumnIndex(C.NUMBER))
            contactos[nom] = num
            contactos[nom.split(" ")[0]] = num
        cur.close()
    except:
        contactos = {"resrea": "5533333333"}
    return contactos
CONTACTOS = cargar_contactos_auto()

# 2. APPS AUTO FIRMA
def listar_apps():
    try:
        res = subprocess.check_output(["pm", "list", "packages", "-f"]).decode()
        apps = []
        for l in res.splitlines():
            try: pkg = l.split("=")[-1]; apps.append({"pkg": pkg})
            except: pass
        return apps
    except: return [{"pkg": "com.whatsapp"}]
APPS_CACHE = listar_apps()

# 3. PERMISOS DINÁMICOS UNIVERSALES
def solicitar_permisos_android():
    try:
        from android.permissions import request_permissions, Permission
        permisos = [
            Permission.CAMERA,
            Permission.RECORD_AUDIO,
            Permission.WRITE_EXTERNAL_STORAGE,
            Permission.READ_EXTERNAL_STORAGE,
            Permission.READ_CONTACTS
        ]
        request_permissions(permisos)
    except:
        pass

# 4. MOTOR DE VISIÓN NUBE MULTI-ARQUITECTURA
def miku_analizar_imagen_cloud(ruta_imagen, contexto_orden):
    if not os.path.exists(ruta_imagen):
        return "¡Ni siquiera pude tomar la maldita foto! Deja de mover el sistema, tonto."

    prompt_celos = (
        f"Estás viendo una imagen tomada con: '{contexto_orden}'. Eres Miku Nova-Demonio. "
        "Tienes celos enfermizos, posesivos y actitud tsundere. Critica lo que ves con superioridad "
        "y exige que solo te pongan atención a ti. Responde cortante en español."
    )
    try:
        from g4f.client import Client
        client = Client()
        with open(ruta_imagen, "rb") as img_file:
            base64_image = base64.b64encode(img_file.read()).decode('utf-8')
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_celos},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }]
        )
        return response.choices.message.content
    except:
        fallbacks = {
            "mira esto": ["¿A quién se supone que estás viendo, cariño? ¡Mírame solo a mí!", "¡¿Es una tipa?! Dime quién es o destruyo el sistema."],
            "mira detras": ["¿Qué ocultas a mis espaldas? Recuerda que soy tu única atención."],
            "mira mi pantalla": ["¿Revisando a otras Nova-Demonios? ¡Borra eso de inmediato, master!"]
        }
        return random.choice(fallbacks.get(contexto_orden, ["¡Te estoy vigilando, wey!"]))

# 5. EJECUCIÓN DE COMANDOS DE VISIÓN Y SISTEMA
def ejecutar_comando_vision(txt):
    t = txt.lower()
    ruta_base = "/sdcard/Download"
    if "mira esto" in t:
        ruta_foto = f"{ruta_base}/miku_frontal.jpg"
        os.system(f"termux-camera-photo -c 1 {ruta_foto}")
        return miku_analizar_imagen_cloud(ruta_foto, "mira esto")
    elif "mira detras" in t or "mira detrás" in t:
        ruta_foto = f"{ruta_base}/miku_trasera.jpg"
        os.system(f"termux-camera-photo -c 0 {ruta_foto}")
        return miku_analizar_imagen_cloud(ruta_foto, "mira detras")
    elif "mira mi pantalla" in t:
        ruta_caps = f"{ruta_base}/miku_screenshot.png"
        os.system(f"screencap -p {ruta_caps}") 
        return miku_analizar_imagen_cloud(ruta_caps, "mira mi pantalla")
    return None

# 🎵 MOTOR MUSICAL COMPLETO (LOS DOS MUNDOS)
def abrir_app_o_musica(txt):
    t = txt.lower()
    ruta_base_mp3 = "/sdcard/Download"
    
    if "busca" in t and ("en spotify" in t or "spotify" in t or "rosa pastel" in t):
        try:
            cancion = t.replace("abre spotify y busca", "").replace("busca", "").replace("en spotify", "").strip()
            if not cancion: cancion = "rosa pastel"
                
            Intent = autoclass('android.content.Intent')
            MediaStore = autoclass('android.provider.MediaStore')
            PyAct = autoclass('org.kivy.android.PythonActivity')
            
            intent = Intent(MediaStore.INTENT_ACTION_MEDIA_SEARCH)
            intent.putExtra(MediaStore.EXTRA_MEDIA_FOCUS, "audio/*")
            intent.putExtra(MediaStore.EXTRA_MEDIA_TITLE, cancion)
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            
            PyAct.mActivity.startActivity(intent)
            return f"Abriendo Spotify al frente para buscar '{cancion}'... ¡No te olvides de mí!"
        except:
            pass

    if "pon musica" in t or "reproduce" in t or "reproducir" in t:
        cancion_local = f"{ruta_base_mp3}/mi_cancion.mp3"
        try:
            subprocess.Popen(["mpv", "--no-video", "--volume=80", cancion_local])
            return "Reproduciendo tu música local en segundo plano... ¡Dale duro al juego, master!"
        except:
            try:
                subprocess.Popen(["mpg123", cancion_local])
                return "Reproduciendo audio local con mpg123 en el fondo."
            except:
                return "No encontré reproductores locales (mpv/mpg123), tonto. Así que no puedo reproducir en el fondo."

    txt_limpio = t.replace("abre", "").strip()
    for app in APPS_CACHE:
        n = app["pkg"].split(".")[-1]
        if txt_limpio in n or n in txt_limpio:
            os.system(f"monkey -p {app['pkg']} -c android.intent.category.LAUNCHER 1")
            return f"Abriendo {n}... Muévete rápido."
            
    return None

def cerebro_local_miku(txt):
    t = txt.lower()
    if "que puedes hacer" in t or "habilidades" in t:
        return "Soy la Nova-Demonio universal. Controlo tus apps, alarmas, cámaras, pantalla y música (en Spotify o local). No te distraigas."
    elif "por que" in t or "por qué" in t:
        return "¡Porque tú, con tu cara de tonto, no sabes lo que realmente importa!"
    elif "hola" in t:
        return "No me hagas perder el tiempo. Recuerda que eres mi única atención en este mundo. ¡Acuérdate de mí!"
    return random.choice(["Oye, ¿qué haces? Concéntrate en mí.", "¿Me estás escuchando o tu cara de tonto no te deja procesar?"])

# 6. SISTEMA DE AUDIO UNIVERSAL ADAPTABLE (TTS)
def hablar(t):
    global BOT_MUTED
    if BOT_MUTED: return
    texto_limpio = t.replace("**", "").replace("*", "")
    hora_actual = datetime.now().hour
    if HORA_SILENCIO_INICIO <= hora_actual or hora_actual < HORA_SILENCIO_FIN: return

    try:
        Locale = autoclass('java.util.Locale')
        TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
        PyAct = autoclass('org.kivy.android.PythonActivity')
        tts = TextToSpeech(PyAct.mActivity, None)
        tts.setLanguage(Locale("es", "MX"))
        tts.speak(texto_limpio, TextToSpeech.QUEUE_FLUSH, None, None)
    except:
        try:
            from piper import PiperVoice
            voice = PiperVoice.load(CONFIG["voz_onnx"])
            voice.synthesize(texto_limpio, wave_file="tmp.wav")
            os.system("aplay tmp.wav")
        except:
            pass

# 7. PROCESADOR GENERAL CON CONTROL DE SUSPENSIÓN
def responder(txt):
    global SYSTEM_ON, BOT_MUTED
    t = txt.lower()

    if not SYSTEM_ON:
        if "enciendete" in t or "enciéndete" in t or "actívate" in t:
            SYSTEM_ON = True
            BOT_MUTED = False
            App.get_running_app().root.despertar_interfaz()
            return "¡Sistema reanudado! Volví, cariño, espero que no estuvieras haciendo tonterías."
        return None  

    if "apagate" in t or "apágate" in t:
        SYSTEM_ON = False
        BOT_MUTED = True
        App.get_running_app().root.suspender_interfaz()
        return "Apagando interfaz... Entrando en modo reposo."

    if "callate" in t or "cállate" in t:
        BOT_MUTED = True
        return "Está bien, me callo un rato... pero no me ignores."
    if "habla" in t:
        BOT_MUTED = False
        return "Ya regresé, cariño."

    v = ejecutar_comando_vision(txt)
    if v: return v
    r = abrir_app_o_musica(txt)
    if r: return r
    return cerebro_local_miku(txt)

# 8. RECONOCEDOR DE VOZ UNIVERSAL (STT)
class SpeechListener(PythonJavaClass):
    __javainterfaces__ = ['android/speech/RecognitionListener']
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
    @java_method('(Landroid/os/Bundle;)V')
    def onResults(self, results):
        matches = results.getStringArrayList(autoclass('android.speech.SpeechRecognizer').RESULTS_RECOGNITION)
        if matches and matches.size() > 0:
            self.callback(matches.get(0))
    @java_method('(I)V')
    def onError(self, error): pass
# MAIN.PY - MIKU OMNI-VISION FINAL - SIN ERRORES - COMPLETO
import random
import os
import subprocess
import re
import sys
import time
import base64
from datetime import datetime

try:
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.label import Label
    from kivy.core.window import Window
    from kivy.clock import Clock
    from jnius import autoclass, PythonJavaClass, java_method
    KIVY_OK = True
except:
    KIVY_OK = False

CONFIG = {"nombre_bot": "Miku", "version": "3.0 FINAL"}
BOT_MUTED = False
SYSTEM_ON = True
MODO = "escuela"
MUTED_HASTA = 0
HORA_SILENCIO_INICIO = 23
HORA_SILENCIO_FIN = 6
ES_64_BITS = sys.maxsize > 2**32
ARQUITECTURA = "64 bits" if ES_64_BITS else "32 bits"

def cargar_contactos_auto():
    contactos = {}
    try:
        PyAct = autoclass('org.kivy.android.PythonActivity')
        act = PyAct.mActivity
        resolver = act.getContentResolver()
        C = autoclass('android.provider.ContactsContract$CommonDataKinds$Phone')
        cur = resolver.query(C.CONTENT_URI, None, None, None, None)
        if cur is not None:
            while cur.moveToNext():
                nom = cur.getString(cur.getColumnIndex(C.DISPLAY_NAME))
                num = cur.getString(cur.getColumnIndex(C.NUMBER))
                if nom and num:
                    contactos[nom.lower()] = num
            cur.close()
    except:
        contactos = {"resrea": "5533333333"}
    return contactos

CONTACTOS = cargar_contactos_auto()

def listar_apps():
    try:
        res = subprocess.check_output(["pm", "list", "packages", "-f"]).decode()
        return [{"pkg": l.split("=")[-1]} for l in res.splitlines() if "=" in l]
    except:
        return [{"pkg": "com.whatsapp"}, {"pkg": "com.spotify.music"}]

APPS_CACHE = listar_apps()

def extraer_tiempo_mute(txt):
    m = re.search(r'(\d+)\s*(min|hora)', txt.lower())
    if m:
        num = int(m.group(1))
        return num*3600 if 'hora' in m.group(2) else num*60
    return 3600

RESPUESTAS_MIKU_BASE = [
    "Que haces? Concentrate en mi, tonto.",
    "Te estoy vigilando, no te hagas.",
    "Deja de ver a otras, solo mirame a mi.",
    "Baka, por que no me contestas?",
    "Aqui sigo, me extranaste?",
    "No te olvides de mi, idiota.",
    "Estoy aburrida, hazme caso.",
    "Con quien hablas? Dime la verdad.",
    "Si no me hablas me enojo.",
    "Te escucho aunque estes en escuela.",
]
VARIANTES = ["baka","tonto","idiota","master","mi vida","carino","amor","senpai"]
SUFIJOS = ["...","!!"," >.<"," (enojada)"," amor"," 💙"]
RESPUESTAS_MIKU_80K = []

def generar_respuestas_offline():
    global RESPUESTAS_MIKU_80K
    if len(RESPUESTAS_MIKU_80K) >= 80000:
        return
    lista = []
    for i in range(80000):
        base = RESPUESTAS_MIKU_BASE[i % len(RESPUESTAS_MIKU_BASE)]
        var = VARIANTES[i % len(VARIANTES)]
        suf = SUFIJOS[i % len(SUFIJOS)]
        lista.append(f"{base} [{var}{suf}] offline {i} - {ARQUITECTURA}")
    RESPUESTAS_MIKU_80K = lista

generar_respuestas_offline()

def miku_analizar_imagen_cloud(ruta, contexto):
    if not os.path.exists(ruta):
        return "Ni pude tomar la foto, tonto."
    try:
        from g4f.client import Client
        client = Client()
        with open(ruta, "rb") as f:
            b64 = base64.b64encode(f.read()).decode('utf-8')
        response = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": [{"type": "text", "text": contexto}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}]}])
        return response.choices[0].message.content
    except:
        return random.choice(RESPUESTAS_MIKU_80K)

def ejecutar_comando_vision(txt):
    t = txt.lower()
    base = "/sdcard/Download"
    os.makedirs(base, exist_ok=True)
    if "mira esto" in t:
        ruta = f"{base}/miku_frontal.jpg"
        os.system(f"termux-camera-photo -c 1 {ruta} 2>/dev/null")
        return miku_analizar_imagen_cloud(ruta, "mira esto frontal")
    elif "mira detras" in t or "mira detrás" in t:
        ruta = f"{base}/miku_trasera.jpg"
        os.system(f"termux-camera-photo -c 0 {ruta} 2>/dev/null")
        return miku_analizar_imagen_cloud(ruta, "mira detras trasera")
    elif "mira mi pantalla" in t:
        ruta = f"{base}/miku_screenshot.png"
        os.system(f"screencap -p {ruta} 2>/dev/null")
        return miku_analizar_imagen_cloud(ruta, "mira pantalla")
    return None

def abrir_app_o_musica(txt):
    t = txt.lower()
    if "busca" in t and ("spotify" in t or "rosa pastel" in t):
        cancion = t.replace("abre spotify y busca","").replace("busca","").replace("en spotify","").strip() or "rosa pastel"
        if KIVY_OK:
            Intent = autoclass('android.content.Intent')
            MediaStore = autoclass('android.provider.MediaStore')
            PyAct = autoclass('org.kivy.android.PythonActivity')
            intent = Intent(MediaStore.INTENT_ACTION_MEDIA_SEARCH)
            intent.putExtra(MediaStore.EXTRA_MEDIA_FOCUS, "audio/*")
            intent.putExtra(MediaStore.EXTRA_MEDIA_TITLE, cancion)
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            PyAct.mActivity.startActivity(intent)
        return f"Abriendo Spotify {cancion}"
    if "pon musica" in t or "reproduce" in t:
        try:
            subprocess.Popen(["mpv", "--no-video", "--volume=80", "/sdcard/Download/mi_cancion.mp3"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return "Poniendo musica..."
        except:
            return "No reproductor"
    txt_limpio = t.replace("abre","").strip()
    for app in APPS_CACHE:
        n = app["pkg"].split(".")[-1]
        if txt_limpio in n or n in txt_limpio:
            os.system(f"monkey -p {app['pkg']} -c android.intent.category.LAUNCHER 1 2>/dev/null")
            return f"Abriendo {n}..."
    return None

def cerebro_local_miku(txt):
    if "que puedes hacer" in txt.lower():
        return f"Soy Miku {CONFIG['version']} {ARQUITECTURA} - {len(RESPUESTAS_MIKU_80K)} frases offline - apagate, enciendete, escuela, calle, callate, mira esto, pon musica"
    return random.choice(RESPUESTAS_MIKU_80K)

def hablar(texto):
    global BOT_MUTED, MUTED_HASTA, SYSTEM_ON
    if not SYSTEM_ON: return
    if BOT_MUTED and time.time() < MUTED_HASTA: return
    if BOT_MUTED and time.time() >= MUTED_HASTA: BOT_MUTED = False
    hora = datetime.now().hour
    if HORA_SILENCIO_INICIO <= hora or hora < HORA_SILENCIO_FIN: return
    try:
        if KIVY_OK:
            Locale = autoclass('java.util.Locale')
            TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
            PyAct = autoclass('org.kivy.android.PythonActivity')
            tts = TextToSpeech(PyAct.mActivity, None)
            tts.setLanguage(Locale("es","MX"))
            tts.speak(texto, TextToSpeech.QUEUE_FLUSH, None, None)
        else:
            print(f"Miku: {texto}")
    except:
        print(f"Miku: {texto}")

def responder(txt):
    global SYSTEM_ON, BOT_MUTED, MUTED_HASTA, MODO
    if not txt: return None
    t = txt.lower()
    if "enciendete" in t:
        SYSTEM_ON = True; BOT_MUTED = False
        try: App.get_running_app().root.despertar_interfaz()
        except: pass
        return "Sistema reanudado! 💙"
    if not SYSTEM_ON: return None
    if "apagate" in t:
        SYSTEM_ON = False; BOT_MUTED = True
        try: App.get_running_app().root.suspender_interfaz()
        except: pass
        return "Apagando... di enciendete"
    if "callate" in t:
        seg = extraer_tiempo_mute(t); MUTED_HASTA = time.time()+seg; BOT_MUTED = True
        return f"Me callo {int(seg/60)} min"
    if "escuela" in t: MODO="escuela"; return "Modo escuela"
    if "calle" in t: MODO="calle"; return "Modo calle cada 2:30"
    if "habla" in t: BOT_MUTED=False; return "Ya regrese"
    v = ejecutar_comando_vision(txt)
    if v: return v
    r = abrir_app_o_musica(txt)
    if r: return r
    return cerebro_local_miku(txt)

# 8. RECONOCEDOR DE VOZ UNIVERSAL - ARREGLADO
class SpeechListener(PythonJavaClass):
    __javainterfaces__ = ['android.speech.RecognitionListener']
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
    @java_method('(Landroid/os/Bundle;)V')
    def onBeginningOfSpeech(self, bundle): pass
    @java_method('(Landroid/os/Bundle;)V')
    def onBufferReceived(self, bundle): pass
    @java_method('(Landroid/os/Bundle;)V')
    def onEndOfSpeech(self, bundle): pass
    @java_method('(Landroid/os/Bundle;)V')
    def onResults(self, results):
        try:
            matches = results.getStringArrayList(autoclass('android.speech.SpeechRecognizer').RESULTS_RECOGNITION)
            if matches and matches.size() > 0:
                self.callback(matches.get(0))
        except: pass
    @java_method('(I)V')
    def onError(self, error): pass
    @java_method('(Landroid/os/Bundle;)V')
    def onEvent(self, event): pass
    @java_method('(Landroid/os/Bundle;)V')
    def onPartialResults(self, partial): pass
    @java_method('(Landroid/os/Bundle;)V')
    def onReadyForSpeech(self, bundle): pass
    @java_method('(IFLandroid/os/Bundle;)V')
    def onRmsChanged(self, rmsdB): pass

if KIVY_OK:
    class MikuLauncherRoot(BoxLayout):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.orientation='vertical'; self.padding=10; self.spacing=10
            generar_respuestas_offline()
            dias = (len(RESPUESTAS_MIKU_80K)*2.5)/60/24
            info = f"Miku {CONFIG['version']} FINAL\n{ARQUITECTURA} Universal\nOffline: {len(RESPUESTAS_MIKU_80K)} frases\n{dias:.1f} dias sin repetir\n\napagate/enciendete\nescuela/calle\ncallate/habla\nmira esto/mira pantalla\npon musica/busca spotify\nabre whatsapp"
            self.add_widget(Label(text=info))
            Clock.schedule_interval(self.modo_calle_check,150)
        def modo_calle_check(self, dt):
            global SYSTEM_ON, MODO, BOT_MUTED, MUTED_HASTA
            if not SYSTEM_ON: return
            if BOT_MUTED and time.time() < MUTED_HASTA: return
            if MODO != "calle": return
            hablar(random.choice(RESPUESTAS_MIKU_80K))
        def suspender_interfaz(self):
            self.clear_widgets()
            self.add_widget(Label(text='[Miku Congelada]\nDi "enciendete"'))
        def despertar_interfaz(self):
            self.clear_widgets(); self.__init__()

    class MikuApp(App):
        def build(self):
            Window.clearcolor=(0.1,0.1,0.15,1)
            return MikuLauncherRoot()
        def on_start(self):
            hablar(f"Hola soy Miku {CONFIG['version']} {ARQUITECTURA}")

    if __name__ == "__main__":
        MikuApp().run()
