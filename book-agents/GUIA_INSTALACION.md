# Guía de instalación — Equipo de agentes de marketing para tus libros

Este kit crea un equipo de 3 agentes (investigación → copywriting → SEO/README)
que corren automáticamente cada día vía GitHub Actions, y publican de verdad
en Bluesky y Mastodon. Para X, LinkedIn y Amazon te deja los textos listos
para copiar y pegar (esos 3 no permiten automatización 100% gratuita).

## Paso 1 — Copia estos archivos a tu repo

Copia toda la carpeta `book-agents/` dentro de tu repo
`mahtrigpa/post-singularity-books` (puedes fusionar las carpetas o ponerlo
en la raíz, como prefieras). Haz commit y push normal con git, o arrastrando
los archivos desde la web de GitHub.

## Paso 2 — Consigue tu API key de Gemini (Google)

1. Ve a https://aistudio.google.com/apikey e inicia sesión con tu cuenta de Google.
2. Click en **"Create API key"**.
3. Copia la key generada.
4. Gemini tiene un **nivel gratuito** (con límites de uso por minuto/día) —
   para empezar a probar no necesitas agregar tarjeta. Revisa los límites
   actuales en https://ai.google.dev/gemini-api/docs/rate-limits
5. Si más adelante quieres más calidad o volumen, puedes cambiar a la API
   de Anthropic (Claude) editando `agents/llm_client.py` por el cliente de
   Claude — dilo y te ayudo a hacer el cambio.

## Paso 3 — Crea cuentas gratis para publicar automáticamente

### Bluesky (recomendado, 100% automático y gratis)
1. Crea una cuenta en https://bsky.app si no tienes.
2. Ve a **Settings > App Passwords** y genera una nueva.
3. Guarda tu handle (ej: `tuusuario.bsky.social`) y esa contraseña de app.

### Mastodon (recomendado, 100% automático y gratis)
1. Crea una cuenta en cualquier instancia, ej. https://mastodon.social
2. Ve a **Preferencias > Desarrollo > Nueva aplicación**.
3. Dale permiso `write:statuses` y copia el "Access Token".

### YouTube (opcional — solo lectura + generación de ideas, gratis)
1. Ve a https://console.cloud.google.com, crea un proyecto (o usa uno existente).
2. Habilita la **YouTube Data API v3** en "APIs y servicios".
3. Crea una **API Key** en "Credenciales" — esta es la que ya tienes.
4. Consigue el **Channel ID** de tu canal (NO es el @handle):
   entra a tu canal logueado y ve a Configuración avanzada, o visita
   https://www.youtube.com/account_advanced
5. Esto solo te deja **leer** tus videos recientes y generar ideas de guion,
   NO publicar. Para publicar community posts o subir videos automáticamente
   se necesita un flujo OAuth2 aparte (client_id + client_secret +
   refresh_token) — dilo si quieres que lo agreguemos más adelante.

### Reddit (opcional — usar con cuidado, riesgo de baneo por spam)
1. Ve a https://www.reddit.com/prefs/apps y crea una app tipo "script".
2. Guarda el client_id, client_secret, tu usuario y contraseña.
3. **Importante:** revisa las reglas de cada subreddit antes de automatizar
   posts ahí. Muchos prohíben auto-promoción.

## Paso 4 — Configura los Secrets en GitHub

En tu repo: **Settings > Secrets and variables > Actions > New repository secret**.
Crea estos (los que no uses, simplemente no los crees y ese canal se saltará solo):

| Nombre | Valor |
|---|---|
| `GEMINI_API_KEY` | tu key de Gemini (Google AI Studio) |
| `BLUESKY_HANDLE` | tu handle de Bluesky |
| `BLUESKY_APP_PASSWORD` | tu app password de Bluesky |
| `MASTODON_API_BASE_URL` | ej. `https://mastodon.social` |
| `MASTODON_ACCESS_TOKEN` | tu token de Mastodon |
| `REDDIT_CLIENT_ID` | (opcional) |
| `REDDIT_CLIENT_SECRET` | (opcional) |
| `REDDIT_USERNAME` | (opcional) |
| `REDDIT_PASSWORD` | (opcional) |
| `YOUTUBE_API_KEY` | (opcional) tu API key de Google Cloud |

## Paso 5 — Llena tus datos reales de libros

Edita `config/books.yaml` con los títulos reales, links de Amazon,
pitch y temas de cada libro. Ya dejé precargados tus links de X y YouTube;
solo falta que agregues tu `youtube_channel_id` si vas a usar ese agente.
Esto es lo que los agentes usan para escribir contenido específico (no genérico).

## Sobre el costo real de probarlo

Con Gemini, el **nivel gratuito** normalmente alcanza para probar el flujo
completo varias veces al día sin pagar nada — solo tiene límites de
solicitudes por minuto/día que puedes revisar en la documentación oficial.
Si en el futuro quieres más calidad de escritura o mayor volumen, puedes
migrar a la API de Anthropic (Claude) — solo dime y actualizamos
`agents/llm_client.py`.

## Paso 6 — Pruébalo manualmente primero

1. Ve a la pestaña **Actions** de tu repo en GitHub.
2. Selecciona el workflow **"Marketing automático de libros"**.
3. Click en **Run workflow** para probarlo ahora mismo (sin esperar al cron).
4. Revisa los logs: te dirá qué canales publicó y cuáles se saltó por
   falta de secrets.

## Paso 7 — Déjalo corriendo solo

Una vez que veas que funciona bien, no tienes que hacer nada más: el
workflow corre automáticamente todos los días a las 8am hora CDMX
(puedes cambiar el horario editando el `cron` en
`.github/workflows/daily-marketing.yml`).

Cada día:
- Investiga tendencias reales (con web search).
- Escribe contenido nuevo y distinto para cada libro.
- Publica solo de verdad en Bluesky y Mastodon.
- Actualiza tu `README.md` como landing page de ventas.
- Deja en `drafts/manual_review.md` los textos para X, LinkedIn y Amazon
  listos para copiar/pegar cuando tengas 2 minutos.

## Notas de seguridad y buen uso

- No compartas tus API keys en el código, siempre usa Secrets de GitHub.
- Revisa cada semana el `drafts/manual_review.md` — no dejes que se acumule.
- Si usas Reddit, empieza con solo 1 subreddit y observa la reacción antes
  de añadir más.
- Puedes correr esto localmente antes de automatizarlo: instala
  `pip install -r requirements.txt`, exporta las variables de entorno
  y corre `python orchestrator.py`.
