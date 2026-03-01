# PaperBanana — Documentación Completa
**Última actualización:** 01-Mar-2026  
**Responsable:** Memito 🐹 & Jorge Cruz-Angeles

---

## ¿Qué es PaperBanana?

Pipeline multi-agente open-source para generar figuras académicas de calidad de publicación.
- **Paper:** arXiv 2601.23265 (Dawei Zhu et al., Google Research)
- **Repo original:** https://github.com/google-research/papervizagent  
- **Fork mantenido:** https://github.com/dwzhu-pku/PaperBanana (4.4k ⭐)
- **Input:** sección de métodos (texto Markdown) + caption de la figura
- **Output:** imagen JPG lista para publicación

---

## Pipeline de 5 Agentes

| Agente | Qué hace |
|--------|----------|
| **Retriever** | Busca diagramas de referencia similares en el dataset |
| **Planner** | Traduce el contenido científico a descripción detallada de figura |
| **Stylist** | Refina la descripción para estándares estéticos académicos |
| **Visualizer** | Genera la imagen con modelo Gemini (image generation) |
| **Critic** | Loop iterativo de mejora sobre la imagen generada |

---

## Setup en la VM de Memito

### Ubicación
```
~/.openclaw/workspace/projects/paperbanana/
```

### Instalación (ya hecho)
```bash
cd ~/.openclaw/workspace/projects/paperbanana
uv venv --python 3.12
source .venv/bin/activate
uv pip install -r requirements.txt
```

### Configuración (configs/model_config.yaml)
```yaml
defaults:
  model_name: "gemini-3-pro-preview"              # Texto (Planner, Stylist, Critic)
  image_model_name: "gemini-3-pro-image-preview"  # Imagen (Visualizer = NanoBanana Pro)

api_keys:
  google_api_key: "<ver ~/.openclaw/secrets/google_gemini_api_key.txt>"
  openai_api_key: ""
  anthropic_api_key: ""
```

---

## 🐛 Bugs Corregidos

### Bug 1 — Planner requiere ref.json aunque no haya referencias
- **Archivo:** `agents/planner_agent.py` (línea ~69)
- **Síntoma:** `FileNotFoundError` si el dataset PaperBananaBench no está descargado
- **Fix:** Agregar `if retrieved_ids:` antes del `open()` para saltar la carga del dataset si no hay referencias solicitadas
- **Estado:** ✅ Corregido (28-Feb-2026)

### Bug 2 — VisualizerAgent.process() no acepta kwarg `source`
- **Archivo:** `run_custom.py`
- **Síntoma:** `TypeError: process() got an unexpected keyword argument 'source'`
- **Fix:** Llamar como `processor.visualizer_agent.process(data)` sin `source=`
- **Estado:** ✅ Corregido (28-Feb-2026)

### Bug 3 — PaperVizProcessor en modo `demo_planner_critic` ejecuta stages incorrectos
- **Archivo:** `utils/paperviz_processor.py`
- **Síntoma:** En modo `demo_planner_critic`, el pipeline omitía el Stylist Agent, por lo que la clave `target_diagram_stylist_desc0` no se generaba y el Visualizer usaba la descripción sin refinar
- **Fix:** En `run_custom.py` se llaman los agentes manualmente (Retriever → Planner → Stylist → Visualizer) en lugar de usar `process_single_query()`
- **Estado:** ✅ Workaround aplicado (28-Feb-2026)

---

## 🇪🇸 Español por Default

### ¿Cómo funciona?

El soporte de idioma se implementa en dos niveles:

#### Nivel 1: System Prompts bilingües en los agentes
- `PlannerAgent` tiene `DIAGRAM_PLANNER_AGENT_SYSTEM_PROMPT_ES` y `PLOT_PLANNER_AGENT_SYSTEM_PROMPT_ES`
- `StylistAgent` tiene `DIAGRAM_STYLIST_AGENT_SYSTEM_PROMPT_ES` y `PLOT_STYLIST_AGENT_SYSTEM_PROMPT_ES`
- Al instanciar con `language="es"`, se activan los prompts en español

#### Nivel 2: Instrucción de idioma en el user prompt
- En cada llamada a `process()`, si `data["output_language"]` == `"Spanish"`, se agrega automáticamente:
  ```
  IMPORTANT: All visible text labels inside the figure must be written in Spanish.
  ```
- Esto asegura que el idioma se refuerce tanto en el system prompt como en el user prompt

### Activar español (método 1: agentes con language="es")
```python
planner_agent = PlannerAgent(exp_config=exp_config, language="es")
stylist_agent = StylistAgent(exp_config=exp_config, language="es")
```

### Activar español (método 2: data dict)
```python
data = {
    "caption": "Figura 1: ...",
    "content": "## Metodología ...",
    "visual_intent": "Figura 1: ...",
    "task_name": "diagram",
    "output_language": "Spanish",  # ← agrega esta clave
}
```

### Combinación recomendada (máxima efectividad)
```python
# Instanciar con language="es" (activa system prompts en español)
planner_agent = PlannerAgent(exp_config=exp_config, language="es")
stylist_agent = StylistAgent(exp_config=exp_config, language="es")

# Y en el data dict (refuerza en user prompt)
data = {
    ...
    "output_language": "Spanish",
}
```

### Scripts disponibles

| Script | Idioma default | Uso |
|--------|---------------|-----|
| `run_es.py` | 🇪🇸 Español | **Script principal** — usar este de ahora en adelante |
| `run_custom.py` | 🇺🇸 Inglés | Script original — soporta `--lang es` para español |

```bash
# Forma recomendada (español por default):
.venv/bin/python run_es.py

# Override a inglés:
.venv/bin/python run_es.py --lang en

# Script original con español:
.venv/bin/python run_custom.py --lang es

# Script original en inglés (default):
.venv/bin/python run_custom.py
```

### ¿Dónde se inyecta el idioma en los agentes?

| Archivo | Dónde | Mecanismo |
|---------|-------|-----------|
| `agents/planner_agent.py` | `__init__()` | Selección de system prompt según `language` |
| `agents/planner_agent.py` | `process()` al construir `user_prompt` | Agrega línea `IMPORTANT: All visible text...` si `output_language` está en `data` |
| `agents/stylist_agent.py` | `__init__()` | Selección de system prompt según `language` |
| `agents/stylist_agent.py` | `process()` al construir `user_prompt` | Agrega línea `IMPORTANT: All visible text...` si `output_language` está en `data` |

---

## 🔌 Cómo Usar desde un Skill Externo (API Interna del Pipeline)

Para usar PaperBanana desde otro script o skill de Memito, sin depender de `run_es.py`:

### Setup mínimo
```python
import sys, asyncio, base64
from pathlib import Path

# Añadir el directorio del proyecto al path
PROJECT_DIR = Path("~/.openclaw/workspace/projects/paperbanana").expanduser()
sys.path.insert(0, str(PROJECT_DIR))

from utils import config
from utils.paperviz_processor import PaperVizProcessor
from agents.planner_agent import PlannerAgent
from agents.visualizer_agent import VisualizerAgent
from agents.stylist_agent import StylistAgent
from agents.critic_agent import CriticAgent
from agents.retriever_agent import RetrieverAgent
from agents.vanilla_agent import VanillaAgent
from agents.polish_agent import PolishAgent
```

### Inicializar config y agentes
```python
exp_config = config.ExpConfig(
    dataset_name="PaperBananaBench",
    task_name="diagram",           # "diagram" o "plot"
    exp_mode="demo_planner_critic",
    retrieval_setting="auto",
    max_critic_rounds=1,
)

# language="es" activa prompts en español
processor = PaperVizProcessor(
    exp_config=exp_config,
    vanilla_agent=VanillaAgent(exp_config=exp_config),
    planner_agent=PlannerAgent(exp_config=exp_config, language="es"),
    visualizer_agent=VisualizerAgent(exp_config=exp_config),
    stylist_agent=StylistAgent(exp_config=exp_config, language="es"),
    critic_agent=CriticAgent(exp_config=exp_config),
    retriever_agent=RetrieverAgent(exp_config=exp_config),
    polish_agent=PolishAgent(exp_config=exp_config),
)
```

### Ejecutar el pipeline completo (función async)
```python
async def generate_figure(caption: str, content: str, output_path: str, language: str = "es") -> str:
    """
    Genera una figura académica con PaperBanana.
    
    Args:
        caption: Pie de figura (describe lo que debe mostrar la imagen)
        content: Sección de métodos del paper (texto Markdown)
        output_path: Ruta donde guardar la imagen JPG resultante
        language: "es" para español (default) o "en" para inglés
    
    Returns:
        Ruta al archivo de imagen guardado, o None si falla
    """
    data = {
        "caption": caption,
        "content": content,
        "visual_intent": caption,
        "task_name": "diagram",
        "output_language": "Spanish" if language == "es" else None,
    }
    
    # Pipeline manual: Retriever → Planner → Stylist → Visualizer
    data = await processor.retriever_agent.process(data)
    data = await processor.planner_agent.process(data)
    data = await processor.stylist_agent.process(data)
    data = await processor.visualizer_agent.process(data)
    
    # Extraer imagen
    img_b64 = data.get("target_diagram_stylist_desc0_base64_jpg") or \
              data.get("target_diagram_desc0_base64_jpg")
    
    if img_b64:
        if "," in img_b64:
            img_b64 = img_b64.split(",")[1]
        img_bytes = base64.b64decode(img_b64)
        with open(output_path, "wb") as f:
            f.write(img_bytes)
        return output_path
    return None

# Uso:
# result = asyncio.run(generate_figure(caption, content, "figura.jpg"))
```

### Claves importantes del data dict

| Clave (input) | Tipo | Descripción |
|--------------|------|-------------|
| `caption` | str | Pie de figura (define el scope visual) |
| `content` | str | Sección de métodos en Markdown |
| `visual_intent` | str | Igual que `caption` en la mayoría de casos |
| `task_name` | str | `"diagram"` o `"plot"` |
| `output_language` | str\|None | `"Spanish"` para español, `None` para inglés |

| Clave (output) | Tipo | Descripción |
|---------------|------|-------------|
| `target_diagram_desc0` | str | Descripción del Planner (~3700 chars) |
| `target_diagram_stylist_desc0` | str | Descripción refinada del Stylist (~4600 chars) |
| `target_diagram_stylist_desc0_base64_jpg` | str | Imagen final en base64 |
| `top10_references` | list | IDs de referencias encontradas por Retriever |

### Nota sobre modo async

PaperBanana es completamente async. Si lo llamas desde un script síncrono:
```python
# Python puro
result = asyncio.run(generate_figure(...))

# Desde dentro de un context async existente (e.g., OpenClaw)
result = await generate_figure(...)
```

---

## Cómo Usar sin Dataset (Modo Custom)

El dataset oficial (PaperBananaBench) tiene miles de ejemplos de referencia para el Retriever.
Sin él, el Retriever y los few-shot examples se saltan, pero el pipeline sigue funcionando bien.

### Flujo del script
```python
# 1. Planner → genera descripción detallada de la figura
data = await processor.planner_agent.process(data)
# → data["target_diagram_desc0"] = "~3700 chars de descripción"

# 2. Stylist → refina para estética académica
data = await processor.stylist_agent.process(data)
# → data["target_diagram_stylist_desc0"] = "~4600 chars refinados"

# 3. Visualizer → genera imagen con Gemini
data = await processor.visualizer_agent.process(data)
# → data["target_diagram_stylist_desc0_base64_jpg"] = "<base64>"
```

### Guardar la imagen
```python
img_b64 = data.get("target_diagram_stylist_desc0_base64_jpg")
img_bytes = base64.b64decode(img_b64)
with open("figura.jpg", "wb") as f:
    f.write(img_bytes)
```

---

## Resultados de Prueba (28-Feb-2026)

### Test 1 — Cholula NPs (Ma et al. 2025)
- **Paper:** "Interpretable ML for predicting antitumor effects of M/MOx NPs"
- **Caption:** Pipeline ML con LightGBM + CNN + MLP + SHAP
- **Planner desc:** 3707 chars
- **Stylist desc:** 4665 chars
- **Imagen:** 246.2 KB
- **Archivo:** `paperbanana-cholula-155738.jpg`
- **Resultado:** ✅ Figura generada exitosamente

### Test 2 — Jorge MetaChem NOVUS 2026
- **Paper:** Propuesta NOVUS "IA Disciplinar Q1027/Q1028"
- **Caption:** Framework MetaChem: GPTeach + NotebookLM + evaluador formativo
- **Planner desc:** 3656 chars
- **Stylist desc:** 4592 chars
- **Imagen:** 194.4 KB
- **Archivo:** `paperbanana-jorge-155922.jpg`
- **Resultado:** ✅ Figura generada exitosamente

---

## Modelos y Tiempo

| Agente | Modelo | Costo aprox |
|--------|--------|-------------|
| Planner | gemini-3-pro-preview | bajo (texto) |
| Stylist | gemini-3-pro-preview | bajo (texto) |
| Visualizer | gemini-3-pro-image-preview | medio (imagen) |

- **Tiempo total por figura:** ~2-3 minutos
- **Tiempo total prueba (2 figuras):** ~4 minutos

---

## Posibles Mejoras

1. **Descargar PaperBananaBench** para activar el Retriever y mejorar calidad con few-shot examples
2. **Agregar ronda de Critic** (max_critic_rounds=1) para refinamiento iterativo
3. **Ajustar aspect ratio** en el Visualizer (actualmente default 1:1, papers prefieren 16:9)
4. **Batch processing** de todas las figuras de un paper automáticamente
5. **Integrar con NanoBanana** para control fino de resolución (2K/4K)

---

## Próximos Pasos Sugeridos

- [ ] Probar con el dataset oficial para ver diferencia de calidad (few-shot activo)
- [ ] Generar figuras para los papers de Cholula que van a publicar
- [ ] Crear flujo integrado: PDF → extraer sección → PaperBanana → figura lista
- [ ] Crear skill `paperbanana-memito` para llamar desde heartbeat/otros skills
- [ ] Evaluar si reemplaza proceso manual de figuras en papers de investigación

---

## Archivos del Proyecto

```
projects/paperbanana/
├── run_es.py              ← ⭐ Script PRINCIPAL en español (Memito 01-Mar-2026)
├── run_custom.py          ← Script original con soporte --lang es/en
├── DOCUMENTACION.md       ← Este archivo
├── configs/
│   └── model_config.yaml  ← Config con modelos y API key
├── agents/
│   ├── planner_agent.py   ← [ACTUALIZADO] soporte language="es", prompts bilingües
│   ├── stylist_agent.py   ← [ACTUALIZADO] soporte language="es", prompts bilingües
│   ├── visualizer_agent.py
│   ├── critic_agent.py
│   ├── retriever_agent.py
│   └── ...
├── utils/
│   ├── config.py
│   ├── paperviz_processor.py
│   └── ...
└── .venv/                 ← Python 3.12 + dependencias
```

---

## 📋 Changelog

### 01-Mar-2026 (Memito)
- ✅ **Soporte de idioma en agentes:** Agregado parámetro `language="es"` a `PlannerAgent` y `StylistAgent`
- ✅ **System prompts en español:** Creados `DIAGRAM_PLANNER_AGENT_SYSTEM_PROMPT_ES`, `PLOT_PLANNER_AGENT_SYSTEM_PROMPT_ES`, `DIAGRAM_STYLIST_AGENT_SYSTEM_PROMPT_ES`, `PLOT_STYLIST_AGENT_SYSTEM_PROMPT_ES`
- ✅ **Inyección de idioma en user prompt:** Ambos agentes detectan `data["output_language"]` y añaden instrucción de idioma al user prompt dinámicamente
- ✅ **`run_es.py` creado:** Script principal con test cases en español, `language="es"` por default
- ✅ **`run_custom.py` actualizado:** Soporte para `--lang es/en` via argparse, caption/content en inglés por default
- ✅ **Documentación completa:** Esta sección, sección "Español por default", "Cómo usar desde un skill externo", Changelog
- ✅ **Verificación de nombre:** Confirmado "PaperBanana" consistente en todos los archivos del proyecto

### 28-Feb-2026 (Memito)
- ✅ **Setup inicial:** Instalación del proyecto, configuración de modelos Gemini
- ✅ **Bug 1 corregido:** `planner_agent.py` — FileNotFoundError cuando no hay dataset
- ✅ **Bug 2 corregido:** `run_custom.py` — TypeError en `process()` con kwarg `source`
- ✅ **Primera prueba exitosa:** Figuras de Cholula NPs y MetaChem generadas correctamente
- ✅ **`run_custom.py` creado:** Script de prueba sin dependencia del dataset oficial
- ✅ **Documentación inicial:** Setup, bugs, resultados de prueba

---

*Documentado por Memito 🐹 — PaperBanana ahora genera figuras en español por default con `run_es.py`*

---

## Changelog

### 01-Mar-2026 — Español, Skill, Replit

#### Soporte de idioma (español por default)
- **`run_es.py`** — nuevo script principal. Pasa `language="es"` a todos los agentes.
- **`agents/planner_agent.py`** — acepta `language` en `__init__`, inyecta instrucción de idioma al prompt: `"IMPORTANT: All visible text labels inside the figure must be written in Spanish."`
- **`agents/stylist_agent.py`** — mismo patrón. El Stylist preserva el idioma en el refinamiento.
- **`run_custom.py`** — acepta `--lang es|en` via argparse. Default: `en` (para compatibilidad). Usar `run_es.py` para español directo.
- Para override puntual en inglés: `.venv/bin/python run_es.py --lang en`

#### Dos configs (Pro vs Estudiantes)
- **`configs/model_config.yaml`** — uso de Memito/Jorge. Modelos Pro (gemini-3-pro-preview + gemini-3-pro-image-preview). **Contiene la API key real — NO subir a Git.**
- **`configs/model_config_students.yaml`** — uso en Replit para alumnos Q2003B. Modelos Flash gratuitos. API key = placeholder.

#### Skill creado
- **`~/.openclaw/workspace/skills/academic-figures-paperbanana/`**
  - `SKILL.md` — instrucciones para que Memito lo invoque correctamente
  - `run_single.sh` — genera una figura con: `bash run_single.sh "caption" "contenido" es diagram pro`

#### Plan Replit Q2003B
- Documento: `PLAN-Q2003B-REPLIT.md` (452 líneas)
- Tamaño del proyecto sin dataset: **504 KB** (cabe en Replit gratuito)
- Dataset: NO va en el repo Git. Se descarga con `setup.sh` al iniciar (HuggingFace, ~30 seg).
- Costo por alumno con Flash gratuito: **$0.00**
- Fix técnico pendiente: `generation_utils.py` necesita 1 línea para reconocer `gemini-2.5-flash-image`

#### Fix config restaurado
- El subagente de Replit había pisado `model_config.yaml` (cambió a Flash y borró API key). **Restaurado a Pro + API key.**
- **Regla:** `model_config.yaml` NUNCA modificar con subagentes. Solo la sesión principal.
