import os
import sys
from duckduckgo_search import DDGS
from google import genai

print("==================================================")
print(" AGENTE CAZADOR DE EMPLEO - EJECUCIÓN AUTOMÁTICA ")
print("==================================================")

# 1. Verificar que la API Key de Gemini esté presente
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("\n ERROR CRÍTICO: No se encontró la variable GEMINI_API_KEY.")
    sys.exit(1)

print(" API Key detectada correctamente.")
print(" Buscando convocatorias en la web...")

# 2. Rastrear la web de forma gratuita con DuckDuckGo
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

# 3. Mandar la información recopilada a Gemini para análisis
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
Entrega una tabla Markdown con: Universidad y País, Nombre de la Vacante/Asignatura, Nivel Académico, Requisitos Clave y Enlace Directo. Si no hay convocatorias específicas activas, incluye los enlaces a las bolsas de trabajo permanentes de PDI de universidades de prestigio identificadas.
"""

try:
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt
    )

    print("\n--- RESULTADOS ENCONTRADOS HOY ---")
    print(response.text)
    print("\n Ejecución finalizada con éxito.")

except Exception as e:
    print(f"\n ERROR EN GEMINI: {e}")
    sys.exit(1)
