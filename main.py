import os
import sys
from google import genai
from google.genai import types

print("==================================================")
print(" AGENTE CAZADOR DE EMPLEO - EJECUCIÓN AUTOMÁTICA ")
print("==================================================")

# 1. Verificar si la API Key existe en los Secrets de GitHub
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("\n ERROR CRÍTICO: No se encontró la variable GEMINI_API_KEY.")
    print("Asegúrate de haberla creado en Settings > Secrets and variables > Actions.")
    sys.exit(1)

print(" API Key detectada correctamente.")
print(" Buscando oportunidades docentes en la web...")

# 2. Ejecutar la búsqueda
try:
    client = genai.Client(api_key=api_key)

    prompt = """
    Actúa como un Headhunter de Talento Académico Superior. Realiza una búsqueda web en tiempo real de convocatorias docentes 100% remotas/en línea activas en universidades públicas o de alto prestigio de México, Costa Rica, España, Colombia y Chile.

    Perfil del candidato:
    - Doctor en Tecnologías del Aprendizaje y el Conocimiento.
    - Candidato a Investigador del SNI (México).
    - Amplia experiencia en docencia virtual de posgrado (Maestría/Doctorado) y dirección de tesis.

    Filtros estrictos:
    - Excluir universidades comerciales de baja exigencia ("patito") o venta de cursos grabados.
    - Excluir puestos de diseñador instruccional puro.
    - Idioma: Español.

    Formato de salida:
    Entrega una tabla Markdown con: Universidad y País, Nombre de la Vacante/Asignatura, Nivel Académico, Requisitos Clave y Enlace Directo a la Convocatoria/Bolsa PDI.
    """

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())]
        )
    )

    print("\n--- RESULTADOS ENCONTRADOS HOY ---")
    print(response.text)
    print("\n Ejecucción finalizada con éxito.")

except Exception as e:
    print(f"\n ERROR AL CONSULTAR LA API DE GEMINI: {e}")
    sys.exit(1)
