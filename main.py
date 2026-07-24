import os
import sys

# Importación blindada a prueba de fallos
try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS

from openai import OpenAI

print("==================================================")
print(" AGENTE CAZADOR DE EMPLEO (MOTOR OPENROUTER) ")
print("==================================================")

# 1. Verificar API Key de OpenRouter
api_key = os.environ.get("OPENROUTER_API_KEY")
if not api_key:
    print("\n ERROR CRÍTICO: No se encontró la variable OPENROUTER_API_KEY en GitHub Secrets.")
    sys.exit(1)

print(" API Key detectada correctamente.")
print(" Buscando convocatorias docentes en la web...")

# 2. Rastrear la web gratis con DuckDuckGo
busquedas = [
    "convocatoria docente virtual universidad posgrado maestria doctorado 2026",
    "vacante profesor en linea universidad publica mexico costa rica espana colombia chile",
    "bolsa de trabajo docente investigador remoto universidad"
]

resultados_web = ""
ddgs = DDGS()

for query in busquedas:
    print(f" Rastreando: {query}")
    try:
        results = ddgs.text(query, max_results=5)
        for r in results:
            resultados_web += f"- Título: {r['title']}\n  Enlace: {r['href']}\n  Resumen: {r['body']}\n\n"
    except Exception as e:
        print(f" Advertencia en búsqueda '{query}': {e}")

print("\n Analizando y filtrando hallazgos con la IA...")

# 3. Analizar información vía OpenRouter
prompt = f"""
Actúa como un Headhunter de Talento Académico Superior. Analiza la siguiente información obtenida de la web sobre vacantes y convocatorias universitarias:

{resultados_web}

Perfil del candidato:
- Doctor en Tecnologías del Aprendizaje y el Conocimiento.
- Candidato a Investigador del SNI (México).
- Amplia experiencia en docencia virtual de posgrado (Maestría/Doctorado) y dirección de tesis.

Filtros estrictos:
- Excluir universidades comerciales de baja exigencia ("patito") o venta de cursos grabados.
- Excluir puestos de diseñador instruccional puro.
- Idioma: Español.

Formato de salida:
Entrega una tabla Markdown con: Universidad y País, Nombre de la Vacante/Asignatura, Nivel Académico, Requisitos Clave y Enlace Directo. Si no hay convocatorias específicas activas en los extractos, resume las bolsas de trabajo permanentes o portales de empleo de las universidades públicas/de prestigio encontradas.
"""

# Lista de respaldos con modelos 100% gratuitos
modelos_gratuitos = [
    "google/gemini-2.0-flash-exp:free",
    "deepseek/deepseek-r1:free",
    "qwen/qwen-2.5-72b-instruct:free",
    "mistralai/mistral-small-24b-instruct-2501:free"
]

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

exito = False

for modelo in modelos_gratuitos:
    try:
        print(f" Probando modelo: {modelo}...")
        response = client.chat.completions.create(
            model=modelo,
            messages=[{"role": "user", "content": prompt}]
        )
        print("\n--- RESULTADOS ENCONTRADOS HOY ---")
        print(response.choices[0].message.content)
        print("\n Ejecución finalizada con éxito.")
        exito = True
        break
    except Exception as e:
        print(f" El modelo {modelo} no estuvo disponible. Intentando con el siguiente...")

if not exito:
    print("\n ERROR CRÍTICO: Ninguno de los modelos gratuitos de la lista respondió.")
    sys.exit(1)
