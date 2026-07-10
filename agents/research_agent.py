"""
Agente de Investigación.
Busca noticias/tendencias recientes de IA, singularidad, sci-fi, etc.
para que el agente de copywriting tenga "gancho" de actualidad.
"""
from .llm_client import ask_claude

SYSTEM_PROMPT = """Eres un agente de investigación de tendencias para marketing editorial.
Tu trabajo es encontrar 3 a 5 temas o noticias ACTUALES (últimos 7 días) relacionados con
inteligencia artificial, singularidad tecnológica, transhumanismo o ciencia ficción especulativa,
que puedan usarse como gancho para promocionar libros del género.
Devuelve una lista breve en viñetas: tema + por qué conecta con el libro. Sé concreto, nada de relleno."""


def run(book: dict) -> str:
    user_prompt = f"""
Libro: {book['title']}
Temas del libro: {', '.join(book.get('themes', []))}
Público objetivo: {book.get('target_audience', 'lectores de ciencia ficción')}

Busca 3-5 tendencias o noticias actuales que conecten con este libro.
"""
    return ask_claude(SYSTEM_PROMPT, user_prompt, use_web_search=True, max_tokens=1000)
