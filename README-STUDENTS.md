# 🍌 PaperBanana — Generador de Figuras Académicas con IA

## ¿Qué es PaperBanana?

PaperBanana genera figuras científicas de alta calidad para papers y reportes académicos usando un pipeline multi-agente con Gemini:

1. **Planner Agent** — Analiza tu descripción y planifica la figura
2. **Stylist Agent** — Refina el estilo visual (colores, tipografía, layout)
3. **Visualizer Agent** — Genera la imagen final con Gemini

## 🚀 Setup Rápido (Replit)

### Paso 1: Configurar API Key
1. Ve a [Google AI Studio](https://aistudio.google.com/apikey) y crea una API key
2. En Replit, ve a **Secrets** (🔒 candado en sidebar)
3. Agrega: `GOOGLE_API_KEY` = tu API key

### Paso 2: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 3: Descargar dataset (solo la primera vez)
```bash
bash setup.sh
```
Esto descarga ~254MB de figuras de referencia desde HuggingFace.

### Paso 4: ¡Generar una figura!
```bash
# Figura en español (default)
python run_es.py --caption "Diagrama de flujo del proceso de cristalización"

# Figura en inglés
python run_es.py --lang en --caption "Flowchart of the crystallization process"
```

## 📝 Parámetros

| Parámetro | Descripción | Default |
|-----------|-------------|---------|
| `--caption` | Descripción de la figura | (requerido) |
| `--content` | Contexto adicional del paper | "" |
| `--lang` | Idioma: `es` o `en` | `es` |
| `--type` | Tipo: `diagram` o `plot` | `diagram` |
| `--output` | Carpeta de salida | `output/` |

## 💡 Tips para mejores resultados

1. **Sé específico** — "Diagrama de flujo con 5 pasos del proceso de extracción sólido-líquido" > "diagrama de extracción"
2. **Incluye contexto** — Usa `--content` para dar contexto del paper
3. **Tipo correcto** — Usa `diagram` para diagramas de flujo, ciclos, esquemas. Usa `plot` para gráficas estadísticas.

## 📊 Ejemplos

```bash
# Diagrama de proceso
python run_es.py --caption "Diagrama de flujo del diseño de experimentos factorial 2^3 para optimización de síntesis"

# Figura tipo gráfica
python run_es.py --type plot --caption "Gráfica de barras comparando rendimiento de 4 catalizadores a 3 temperaturas"

# Con contexto del paper
python run_es.py \
  --caption "Esquema del mecanismo de formación de sistemas coamorfos" \
  --content "Paper sobre sistemas coamorfos de indometacina-sacarosa preparados por ball milling"
```

## ⚠️ Notas

- **Modelo gratuito:** Usa Gemini 2.5 Flash (tier gratuito de Google)
- **Dataset:** ~296MB — necesario para que el Retriever encuentre figuras de referencia
- **Tiempo por figura:** ~30-60 segundos
- Las figuras generadas se guardan en la carpeta `output/`

## 🔧 Troubleshooting

| Error | Solución |
|-------|----------|
| `GOOGLE_API_KEY not set` | Agrega tu API key en Secrets de Replit |
| `Dataset not found` | Corre `bash setup.sh` |
| `Rate limit exceeded` | Espera 1 minuto y reintenta |
| `Model not found` | Verifica que tu API key tenga acceso a Gemini |

---
*Basado en [PaperBanana](https://github.com/google/PaperBanana) (Google, Apache 2.0)*
