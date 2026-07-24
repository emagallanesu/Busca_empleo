import os
from google import genai
from google.genai import types

print("==================================================")
print(" AGENTE CAZADOR DE EMPLEO - EJECUCIÓN AUTOMÁTICA ")
print("==================================================")

# Configurar cliente con la API Key guardada en GitHub
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

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

print("Buscando oportunidades docentes en la web...")

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=prompt,
    config=types.GenerateContentConfig(
        tools=[types.Tool(google_search=types.GoogleSearch())]
    )
)

print("\n--- RESULTADOS ENCONTRADOS HOY ---")
print(response.text)
