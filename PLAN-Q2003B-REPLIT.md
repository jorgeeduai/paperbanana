# Plan de Deploy: PaperBanana para Q2003B — Diseño de Experimentos
**Dr. Jorge Cruz-Angeles — Tec de Monterrey**  
*Preparado por Memito · 1-Mar-2026*

---

## 📋 Resumen Ejecutivo

PaperBanana se puede adaptar para Q2003B con mínimas modificaciones:
- Los alumnos usarán **Gemini 2.5 Flash** (texto) + **Gemini 2.5 Flash imagen** (diagramas)
- El deploy en **Replit es directo** — Streamlit funciona nativamente
- El dataset de 296 MB **NO va en Replit** — se usa `retrieval_setting="none"` (funcional)
- Tamaño mínimo del proyecto para Replit: **~664 KB** (sin dataset, sin assets web)

---

## 1. Compatibilidad con Gemini 2.5 Flash

### 1.1 Modelos recomendados para versión estudiante

| Rol | Modelo | Notas |
|-----|--------|-------|
| **Texto (razonamiento)** | `gemini-2.5-flash` | ✅ Funciona directo. Nivel gratuito disponible. |
| **Imágenes (diagramas)** | `gemini-2.5-flash-preview-04-17` | ✅ Soporta generación nativa de imágenes con `response_modalities=["IMAGE"]`. |

> **¿Por qué dos modelos?**  
> PaperBanana usa el `model_name` (texto) para Planner, Critic, Stylist, Retriever y Vanilla agents.  
> El `image_model_name` lo usa **únicamente el VisualizerAgent para diagramas** (modo `use_image_generation=True`).  
> Para plots estadísticos, el VisualizerAgent genera código Python/Matplotlib — solo necesita el modelo de texto.

### 1.2 Config actualizada (`configs/model_config.yaml`)

```yaml
defaults:
  model_name: "gemini-2.5-flash"
  image_model_name: "gemini-2.5-flash-preview-04-17"

api_keys:
  google_api_key: ""      # Poner vacío — se carga desde Replit Secrets
  openai_api_key: ""
  anthropic_api_key: ""
```

> **IMPORTANTE:** En el deploy de Replit, los API Keys van en **Secrets**, NO en este archivo.  
> La app ya soporta leerlos desde variables de entorno (`GOOGLE_API_KEY`).

### 1.3 Restricciones de código detectadas

**Ninguna restricción hardcodeada** impide usar Flash. El código en `utils/generation_utils.py` detecta el proveedor por el nombre del modelo:
- `"gemini" in model_name` → usa Gemini client ✅
- `"gpt-image" in model_name` → usa OpenAI ✅  
- `"image" in model_name` → activa modo de generación de imagen (el `image_model_name` siempre contiene "image" en el nombre recomendado)

**⚠️ Nota crítica sobre el modelo de imagen:**  
El código en `generation_utils.py` (líneas 132-133) activa el modo de imagen cuando `"nanoviz" in model_name or "image" in model_name`. Por eso el modelo de imagen DEBE tener "image" en su nombre.  
`gemini-2.5-flash-preview-04-17` NO contiene "image" → **el VisualizerAgent no activará el modo imagen correctamente**.

**Solución:** Usar `gemini-2.5-flash-image` (si Google lo libera) O hacer un pequeño ajuste al código (ver Sección 4).

### 1.4 Compatibilidad con retrieval_setting="none"

El `RetrieverAgent` tiene fallback automático:
```python
if retrieval_setting in ["auto", "random"] and not ref_file.exists():
    print(f"Warning: Reference file not found. Falling back to retrieval_setting='none'.")
    retrieval_setting = "none"
```
Esto significa que **aunque el alumno seleccione "auto", si no hay dataset, la app cae a "none" sin romperse**. ✅

---

## 2. Archivos Mínimos para Replit

### 2.1 Lista de archivos necesarios

```
paperbanana-q2003b/
├── demo.py                    # App Streamlit principal (40 KB)
├── requirements.txt           # Dependencias (4 KB)
├── configs/
│   └── model_config.yaml      # Config del modelo (estudiante)
├── agents/
│   ├── __init__.py
│   ├── base_agent.py
│   ├── critic_agent.py
│   ├── planner_agent.py
│   ├── polish_agent.py
│   ├── retriever_agent.py
│   ├── stylist_agent.py
│   ├── vanilla_agent.py
│   └── visualizer_agent.py
├── utils/
│   ├── __init__.py
│   ├── config.py
│   ├── generation_utils.py
│   ├── image_utils.py
│   └── paperviz_processor.py
├── prompts/
│   ├── __init__.py
│   ├── diagram_eval_prompts.py
│   └── plot_eval_prompts.py
└── style_guides/
    ├── neurips2025_diagram_style_guide.md
    └── neurips2025_plot_style_guide.md
```

**NO incluir:**
- `data/` — 296 MB del dataset (no cabe en Replit)
- `.venv/` — Replit instala sus propias dependencias
- `.git/` — no es necesario para la app
- `results/` — se genera en tiempo de ejecución
- `assets/` y `static/` — son para la landing page HTML, no para Streamlit
- `main.py`, `run_custom.py` — son para ejecución por CLI, no para demo Streamlit
- `scripts/`, `visualize/` — herramientas de análisis, no necesarias

### 2.2 Tamaño total estimado

| Carpeta/Archivo | Tamaño |
|----------------|--------|
| `demo.py` | 40 KB |
| `requirements.txt` | 4 KB |
| `agents/` | 200 KB |
| `utils/` | 124 KB |
| `configs/` | 12 KB |
| `prompts/` | 88 KB |
| `style_guides/` | 36 KB |
| **TOTAL** | **~504 KB** |

✅ Muy por debajo del límite de Replit (512 MB en plan gratuito).

---

## 3. Pasos para Deploy en Replit

### Opción recomendada: Fork en GitHub → Deploy en Replit

**¿Por qué esta opción?**
- Jorge mantiene control del código fuente en GitHub
- Los alumnos hacen Fork del repo del profe → aprenden git workflow
- Actualizaciones fáciles: Jorge pushea → alumnos hacen pull
- Replit puede conectarse directo al repo de GitHub (Import from GitHub)
- Si Replit cae, el código sigue en GitHub

**vs. Template de Replit:**
- Template es más fácil de iniciar pero menos flexible
- No enseña git a los alumnos
- Más difícil de actualizar para todos

### 3.1 Preparación del repositorio GitHub

1. **Crear repositorio limpio** (solo los archivos de Replit):
   ```bash
   # Crear un repo nuevo o branch "student" en el repo existente
   mkdir paperbanana-q2003b
   cd paperbanana-q2003b
   git init
   # Copiar solo los archivos necesarios (ver lista 2.1)
   ```

2. **Crear el archivo `.replit`** (en la raíz):
   ```toml
   run = "streamlit run demo.py --server.port 8501 --server.address 0.0.0.0"
   
   [nix]
   channel = "stable-24_05"
   
   [unitTest]
   language = "python3"
   
   [deployment]
   run = ["sh", "-c", "streamlit run demo.py --server.port 8501 --server.address 0.0.0.0"]
   deploymentTarget = "cloudrun"
   ```

3. **Crear `.streamlit/config.toml`**:
   ```toml
   [server]
   headless = true
   address = "0.0.0.0"
   port = 8501
   
   [theme]
   primaryColor = "#FFCE00"
   backgroundColor = "#1a1a1a"
   secondaryBackgroundColor = "#2d2d2d"
   textColor = "#FFFFFF"
   ```

4. **Simplificar `requirements.txt`** para Replit (sin dependencias innecesarias):
   ```
   google-genai>=1.0.0
   streamlit>=1.30.0
   pillow>=10.0.0
   numpy>=1.24.0
   tqdm>=4.65.0
   json_repair>=0.1.0
   matplotlib>=3.7.0
   python-dotenv>=1.0.0
   pyyaml>=6.0.0
   aiofiles>=23.0.0
   ```
   > Quitar: `anthropic`, `openai`, `google-auth` (los alumnos solo usan Gemini)

5. Hacer push al repo de GitHub (privado o público según prefiera Jorge)

### 3.2 Import en Replit (pasos para cada alumno)

```
1. Ir a replit.com → "Create Repl"
2. Seleccionar "Import from GitHub"
3. Pegar la URL del repo de Jorge
4. Replit detecta automáticamente que es Python + Streamlit
5. Agregar el Secret GOOGLE_API_KEY (ver sección 3.3)
6. Click "Run" → Streamlit arranca en segundos
```

### 3.3 Configuración de API Keys en Replit Secrets

Los alumnos necesitan **1 sola API Key**:

| Secret | Valor | Dónde obtenerla |
|--------|-------|----------------|
| `GOOGLE_API_KEY` | `AIzaSy...` | [aistudio.google.com](https://aistudio.google.com) → "Get API Key" |

**Pasos para configurar en Replit:**
1. En el Repl, click en el ícono 🔒 "Secrets" (panel izquierdo)
2. Click "New Secret"
3. Key: `GOOGLE_API_KEY`
4. Value: pegar su API Key de Google AI Studio
5. Click "Add Secret"

La app ya lee `GOOGLE_API_KEY` del entorno automáticamente gracias a:
```python
api_key = get_config_val("api_keys", "google_api_key", "GOOGLE_API_KEY", "")
```

> **NOTA:** El API Key del profesor NO debe compartirse. Cada alumno obtiene el suyo gratis en Google AI Studio (plan gratuito de Gemini).

---

## 4. Simplificación de la Interfaz Streamlit para Estudiantes

### 4.1 Features a quitar/simplificar

| Feature actual | Recomendación | Razón |
|---------------|---------------|-------|
| Selector "Retrieval Setting" | **Fijar a `"none"`** y ocultar | Sin dataset, las opciones auto/manual/random no funcionan |
| Selector "Model Name" | **Fijar desde config** y ocultar | Los alumnos no necesitan cambiar el modelo |
| Pestaña "Batch Processing" (Tab 2) | **Quitar** | Es para investigadores, confunde a estudiantes |
| Pestaña "Evaluate" (si existe) | **Quitar** | No relevante para Q2003B |
| Número de candidatos (default 10) | **Reducir a 3-5** | 10 llama a la API 10 veces → agota cuota rápido |
| Max Critic Rounds (default 3) | **Reducir a 1-2** | Ahorra tokens; 1 ronda es suficiente para aprendizaje |
| Nanoviz image editing | **Quitar** | Requiere Vertex AI, no disponible con API Key simple |
| Selector de Aspect Ratio | **Mantener** — es pedagógico | Los alumnos pueden explorar 16:9, 21:9 |
| Pipeline Mode | **Simplificar a 2 opciones claras** | `"Rápido (sin referencias)"` y `"Completo"` |

### 4.2 Modificaciones sugeridas al demo.py

```python
# CAMBIOS MÍNIMOS PARA VERSIÓN ESTUDIANTE:

# 1. Fijar retrieval_setting = "none" (sin dataset)
retrieval_setting = "none"  # Hardcoded, no mostrar selectbox

# 2. Fijar modelo desde config (no mostrar selector)
model_name = ""  # Usa el de model_config.yaml automáticamente

# 3. Reducir candidatos default
num_candidates = st.number_input(
    "Número de diagramas a generar",
    min_value=1,
    max_value=5,      # Máximo 5 para alumnos (ahorra tokens)
    value=3,          # Default 3 (buen balance calidad/costo)
    ...
)

# 4. Simplificar pipeline modes
exp_mode = st.selectbox(
    "Modo de generación",
    {
        "⚡ Rápido (Planner + Critic)": "demo_planner_critic",
        "✨ Completo (con Estilista)": "demo_full"
    },
    ...
)

# 5. Reducir max_critic_rounds
max_critic_rounds = st.slider("Rondas de refinamiento", 1, 3, value=2)
```

### 4.3 Agregar contexto pedagógico Q2003B

Agregar en el sidebar de Streamlit:
```python
st.sidebar.markdown("""
## 🍌 PaperBanana — Q2003B
**Diseño de Experimentos**
Dr. Jorge Cruz-Angeles

Esta herramienta usa IA (Gemini) para generar
figuras científicas a partir de descripciones
metodológicas.

**¿Cómo usarla?**
1. Describe tu metodología en el cuadro de texto
2. Escribe una leyenda para tu figura
3. Selecciona cuántas variantes generar
4. ¡Genera!
""")
```

---

## 5. Costo Estimado por Alumno — Gemini 2.5 Flash

### 5.1 Precios de Gemini 2.5 Flash (API)

| Tier | Tokens de entrada | Tokens de salida |
|------|------------------|-----------------|
| **Gratis (Free Tier)** | 1M tokens/día gratis | Incluido |
| **Pago** | $0.075/M tokens | $0.30/M tokens |

> *Fuente: Google AI Studio pricing (Feb 2026). Verificar en aistudio.google.com/pricing*

### 5.2 Estimado por sesión de uso típica en Q2003B

**Escenario:** 1 alumno genera 3 diagramas para su proyecto DOE

| Operación | Tokens aprox. | Llamadas |
|-----------|---------------|---------|
| Planner (analizar metodología) | ~4,000 tokens entrada + 2,000 salida | 3 |
| Visualizer (generar imagen) | ~1,500 tokens de prompt | 3 |
| Critic (revisar + refinar) | ~3,000 entrada + 2,000 salida | 3 |
| **Total por sesión** | **~30,000 tokens** | **~9 llamadas** |

### 5.3 Conclusión de costos

| Uso | Costo |
|-----|-------|
| **Sesión típica (3 diagramas)** | **$0.00** — dentro del free tier |
| Free tier diario | 1,000,000 tokens → ~33 sesiones típicas/día |
| Costo si excede free tier | ~$0.004 por sesión (muy bajo) |

**✅ Para uso académico ocasional (proyecto DOE), el plan gratuito de Google AI Studio es completamente suficiente.**

Los alumnos solo necesitan:
1. Cuenta de Google
2. Entrar a [aistudio.google.com](https://aistudio.google.com)
3. Crear API Key gratuita

**Rate limits del plan gratuito:**
- 10 requests/minuto (RPM)
- 1,000 requests/día (RPD)  
- 1M tokens/día

Para un grupo de ~30 alumnos trabajando de forma asíncrona (no todos al mismo tiempo), no habrá problemas de rate limiting.

---

## 6. Nota sobre el Dataset

### 6.1 Qué es el dataset

El dataset `data/PaperBananaBench/` (296 MB) contiene:
- Colección de diagramas académicos de referencia (imágenes + metadatos)
- Se usa por el **RetrieverAgent** para buscar ejemplos similares
- Permite que el Planner se inspire en diagramas reales de papers

### 6.2 Sin dataset: funcionamiento reducido pero útil

**Sin retrieval (`retrieval_setting="none"`):**
- ✅ El Planner genera la descripción del diagrama directamente del texto del alumno
- ✅ El Visualizer genera la imagen normalmente
- ✅ El Critic refina la imagen iterativamente
- ❌ No hay ejemplos de referencia para inspirar el estilo visual
- ❌ La diversidad y calidad pueden ser ligeramente menores

**Diferencia práctica para Q2003B:**
> Para diagramas de metodología DOE (bloques, factores, interacciones), la calidad sin dataset es perfectamente aceptable para uso educativo. El dataset marca diferencia principalmente en papers de IA/ML donde hay convenciones visuales muy específicas.

### 6.3 Opciones para mejorar calidad sin dataset completo

1. **Opción A — Sin dataset (recomendada para Replit):** Usar `retrieval_setting="none"`. Simple, cero fricción.

2. **Opción B — Dataset pequeño personalizado:** Jorge puede crear un mini-dataset de 5-10 diagramas de DOE que los alumnos compartan en el repo. Esto mejora la calidad sin los 296 MB.

3. **Opción C — Dataset en la nube:** Subir el dataset a Google Drive y montarlo en Replit vía script de setup. Más complejo, no recomendado para primera implementación.

---

## 7. Fix Técnico Pendiente: Modelo de Imagen

**Problema detectado:**  
El código en `utils/generation_utils.py` activa el modo de generación nativa de imágenes cuando `"image" in model_name`. El modelo `gemini-2.5-flash-preview-04-17` NO tiene "image" en su nombre.

**Fix mínimo** (1 línea en `utils/generation_utils.py`):
```python
# ANTES (línea 132-133):
if (
    "nanoviz" in model_name
    or "image" in model_name
):

# DESPUÉS:
if (
    "nanoviz" in model_name
    or "image" in model_name
    or "flash-preview" in model_name  # gemini-2.5-flash-preview supports image gen
):
```

**O alternativamente**, usar el nombre de modelo que contenga "image":
- Esperar a que Google lance `gemini-2.5-flash-image` (probablemente pronto)
- O usar `gemini-2.5-flash-image-generation` si está disponible

**Acción recomendada:** Probar primero con `gemini-2.5-flash-preview-04-17` en Google AI Studio. Si la generación de imágenes no funciona, aplicar el fix de 1 línea.

---

## 8. Checklist de Deploy

```
□ Crear repo GitHub con archivos mínimos (ver lista 2.1)
□ Actualizar configs/model_config.yaml (gemini-2.5-flash)
□ Crear .replit con comando de Streamlit
□ Crear .streamlit/config.toml
□ Simplificar requirements.txt (quitar anthropic, openai)
□ Aplicar modificaciones a demo.py (ver sección 4.2)
□ Agregar contexto pedagógico Q2003B en sidebar
□ Probar localmente que funciona con gemini-2.5-flash
□ Push a GitHub
□ Compartir URL del repo con alumnos
□ Los alumnos importan en Replit + configuran GOOGLE_API_KEY en Secrets
□ ¡Listo! 🍌
```

---

## 9. Resumen de Decisiones

| Decisión | Elección | Razón |
|----------|----------|-------|
| Modelo texto | `gemini-2.5-flash` | Gratuito, capaz, API Key de alumnos |
| Modelo imagen | `gemini-2.5-flash-preview-04-17` | Misma API Key, soporta imagen nativa |
| Deploy method | GitHub → Replit import | Pedagógico, mantenible, actualizable |
| Dataset | Sin dataset (`none`) | 296 MB no cabe en Replit; calidad suficiente |
| Candidatos default | 3 | Balance calidad/tokens/velocidad |
| Critic rounds | 2 | Suficiente para aprendizaje, ahorra cuota |

---

*Generado por Memito 🐹 · 1-Mar-2026*
