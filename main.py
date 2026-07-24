import os
import sys
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
    "convocatoria docente virtual universidad posgrado maestria doctorado",
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

# 3. Analizar información vía OpenRouter usando un modelo 100% GRATUITO
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

try:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    # Usamos Llama 3.1 8B Instruct que es totalmente gratuito en OpenRouter
    response = client.chat.completions.create(
        model="meta-llama/llama-3.1-8b-instruct:free",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    print("\n--- RESULTADOS ENCONTRADOS HOY ---")
    print(response.choices[0].message.content)
    print("\n Ejecución finalizada con éxito.")

except Exception as e:
    print(f"\n ERROR EN OPENROUTER: {e}")
    sys.exit(1)
