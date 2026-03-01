"""
PaperBanana — Script en ESPAÑOL (default)
Jorge Cruz-Angeles & Memito 🐹 — 01-Mar-2026

Este es el script principal para uso cotidiano. Genera figuras con
textos internos en ESPAÑOL por default.

Uso:
  .venv/bin/python run_es.py              # ejecuta los 3 test cases en español
  .venv/bin/python run_es.py --lang en    # override a inglés
"""

import argparse
import asyncio
import base64
import sys
import os
import json
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from utils import config
from utils.paperviz_processor import PaperVizProcessor
from agents.planner_agent import PlannerAgent
from agents.visualizer_agent import VisualizerAgent
from agents.stylist_agent import StylistAgent
from agents.critic_agent import CriticAgent
from agents.retriever_agent import RetrieverAgent
from agents.vanilla_agent import VanillaAgent
from agents.polish_agent import PolishAgent

OUTPUT_DIR = Path("/mnt/agent-workspace/Buzón/Para-Jorge/paperbanana-test")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ─────────────────────────────────────────────────────────────
# TEST CASES EN ESPAÑOL
# ─────────────────────────────────────────────────────────────

TESTS = [
    {
        "id": "paperbanana-meta",
        "label": "PaperBanana explicando PaperBanana 🍌 (meta-figura)",
        "caption": (
            "Figura 1: Visión general del framework multi-agente PaperBanana para la generación "
            "automatizada de ilustraciones académicas. Dado el texto de metodología y el pie de "
            "figura como entrada, cinco agentes especializados colaboran en secuencia: el Retriever "
            "identifica diagramas de referencia relevantes, el Planificador sintetiza una descripción "
            "visual detallada mediante aprendizaje en contexto, el Estilista la refina según estándares "
            "estéticos académicos, el Visualizador genera la imagen usando un modelo de generación de "
            "imágenes de última generación, y el Crítico cierra el ciclo mediante refinamiento iterativo "
            "multi-ronda hasta producir una ilustración lista para publicación."
        ),
        "content": """
## PaperBanana: Framework Multi-Agente Guiado por Referencias para Ilustración Académica

PaperBanana automatiza la generación de diagramas científicos y gráficas de calidad de publicación
a partir del texto de la sección de métodos y pies de figura. El framework orquesta cinco agentes
especializados en un pipeline estructurado inspirado en la colaboración de equipos creativos:

**Entrada:**
- Contenido de la sección de métodos (texto Markdown describiendo el enfoque científico)
- Pie de figura (intención comunicativa y descripción de la ilustración deseada)

**Pipeline de Agentes:**

1. **Agente Retriever (Recuperador)**
   - Busca en un conjunto de referencias curado (dataset PaperBananaBench) los diagramas más relevantes
   - Usa similitud semántica para identificar los top-k ejemplos de referencia
   - Proporciona ejemplos few-shot a los agentes posteriores para aprendizaje en contexto

2. **Agente Planner (Planificador)**
   - Recibe: contenido de métodos + intención visual + ejemplos de referencia con imágenes
   - Traduce el contenido científico en una descripción textual comprensiva de la figura a generar
   - Usa aprendizaje en contexto de los diagramas de referencia para guiar la estructura visual
   - Salida: descripción detallada de la figura (~3500-4000 caracteres)

3. **Agente Stylist (Estilista)**
   - Recibe: descripción del planificador + guías de estilo sintetizadas automáticamente
   - Refina la descripción para adherirse a los estándares estéticos académicos
   - Agrega especificaciones de paleta de colores, diseño, tipografía y jerarquía visual
   - Salida: descripción estéticamente refinada (~4500-5000 caracteres)

4. **Agente Visualizer (Visualizador)**
   - Recibe: descripción refinada por el estilista
   - Transforma la descripción textual en salida visual usando el modelo de generación de imágenes Gemini
   - Genera múltiples imágenes candidatas en paralelo para comparación
   - Salida: imagen JPG codificada en base64

5. **Agente Critic (Crítico)**
   - Recibe: imagen generada + descripción original + pie de figura
   - Evalúa la imagen contra precisión científica y estándares estéticos
   - Proporciona retroalimentación estructurada y sugerencias de mejora
   - Forma un ciclo cerrado con el Visualizador para refinamiento iterativo multi-ronda
   - Se detiene cuando se alcanza el umbral de calidad o se agotan las rondas máximas

**Salida:** Ilustración lista para publicación en formato JPG, adecuada para papers académicos en conferencias y revistas de IA/ML.
""",
    },
    {
        "id": "cholula",
        "label": "Nanopartículas Cholula — ML Antitumoral (Ma et al. 2025)",
        "caption": (
            "Figura 1: Visión general del pipeline de aprendizaje automático interpretable para predecir "
            "los efectos antitumorales de nanopartículas metálicas y de óxido metálico. "
            "El framework integra descriptores de química cuántica con datos de toxicidad "
            "de 152 artículos (2765 instancias), aplica modelos LightGBM, CNN y MLP, "
            "y usa SHAP para la interpretabilidad."
        ),
        "content": """
## Pipeline de Aprendizaje Automático para Predicción de Toxicidad Antitumoral de Nanopartículas

Combinamos cálculos de química cuántica con datos de toxicidad publicados para desarrollar un
framework de aprendizaje automático interpretable que logra más del 90% de precisión en validación cruzada.

**Dataset**: 39 descriptores extraídos de 152 artículos, con 2765 instancias que cubren
varios tipos de nanopartículas, métodos de detección y tipos celulares.

**Ingeniería de Características**:
- Coeficiente de similitud de Jaccard para representación mejorada de datos
- Características clave: concentración, tiempo de exposición, potencial zeta, diámetro, área COSMO (CA),
  recubrimiento, métodos de ensayo, tipos celulares, electronegatividad del metal, energía HOMO, peso molecular

**Modelos Evaluados**:
1. **LightGBM**: Gradient boosting eficiente con aprendizaje basado en histogramas; búsqueda de cuadrícula
   para tasa de aprendizaje, profundidad del árbol y número de hojas; optimizado mediante validación cruzada.
2. **CNN**: Dos capas convolucionales (32 y 64 filtros, tamaño de kernel 3) con max pooling,
   capas completamente conectadas y activación sigmoide para clasificación binaria.
3. **MLP**: Tres capas completamente conectadas que aprenden relaciones no lineales entre características.

**Interpretabilidad**:
- Análisis de Importancia de Características para clasificar descriptores
- SHAP (Shapley Additive Explanations) para explicar predicciones individuales

**Validación**: Se sintetizaron nuevas nanopartículas de óxido metálico y se evaluaron sus propiedades
fisicoquímicas y toxicidad antitumoral experimentalmente para validar la generalización del modelo.
""",
    },
    {
        "id": "jorge",
        "label": "MetaChem — IA Disciplinar NOVUS 2026 (Jorge Q1027/Q1028)",
        "caption": (
            "Figura 1: Framework MetaChem — sistema pedagógico impulsado por IA que integra "
            "un chatbot LLM experto en química, podcasts generados con IA (NotebookLM), "
            "y evaluación formativa adaptativa para cursos de química de licenciatura "
            "(Q1027 Bioquímica y Q1028 Química General) en el Tecnológico de Monterrey."
        ),
        "content": """
## MetaChem: IA Disciplinar Especializada para Educación en Química

MetaChem es un framework educativo impulsado por IA para cursos de química de licenciatura
(Q1027 Bioquímica, Q1028 Química General) diseñado para mejorar la comprensión conceptual,
reducir la carga cognitiva y promover el aprendizaje activo mediante tres componentes integrados:

**Componente 1 — Chatbot GPTeach Experto en Química**:
- LLM ajustado con contenido específico de la disciplina (biomoléculas, termodinámica, mezclas)
- Diálogo socrático: guía a los estudiantes a través de la resolución de problemas sin dar respuestas directas
- Retroalimentación adaptativa basada en las respuestas de los estudiantes
- Desplegado en Canvas LMS; accesible 24/7

**Componente 2 — Pipeline de Podcasts con IA (NotebookLM)**:
- Material fuente: notas de clase, capítulos de libro, protocolos de laboratorio
- NotebookLM genera diálogos de audio contextualizando cada tema
- Episodios de podcast semanales distribuidos vía Spotify
- Resultados previos: 97% de preferencia estudiantil sobre la lectura tradicional (n=76)

**Componente 3 — Evaluador Formativo con IA**:
- Escenarios inmersivos basados en roles (estudiante como científico, investigador o ingeniero)
- Retroalimentación automatizada alineada con rúbricas y con citas del material del curso
- Datos recolectados: precisión, tiempo en tarea, indicadores de aprendizaje autorregulado

**Diseño Experimental**:
- Cuasi-experimental: grupo de tratamiento (MetaChem) vs grupo control (tradicional)
- Pruebas conceptuales pre/post (instrumentos validados)
- 3 periodos, ~400 estudiantes en total
- Métricas de resultado: ganancias conceptuales (d de Cohen), calificaciones de exámenes, engagement
""",
    },
]


async def run_test(test: dict, exp_config, processor, language: str = "es") -> dict:
    """Run a single PaperBanana test."""
    print(f"\n{'='*60}")
    print(f"🍌 Procesando: {test['label']}")
    print(f"{'='*60}")

    data = {
        "caption": test["caption"],
        "content": test["content"],
        "visual_intent": test["caption"],
        "task_name": "diagram",
        "output_language": "Spanish" if language == "es" else None,
    }

    result = {
        "id": test["id"],
        "label": test["label"],
        "stages": {},
        "final_image_path": None,
        "error": None,
    }

    try:
        # Stage 0: Retriever (busca ejemplos similares en el dataset)
        print("  [0/3] Retriever Agent (buscando referencias similares)...")
        data = await processor.retriever_agent.process(data)
        refs = data.get("top10_references", [])
        print(f"  ✅ Retriever: {len(refs)} referencias encontradas → {refs[:3]}...")

        # Stage 1: Planner
        print("  [1/3] Planner Agent...")
        data = await processor.planner_agent.process(data)
        desc_key = "target_diagram_desc0"
        if desc_key in data:
            result["stages"]["planner_desc"] = data[desc_key][:300] + "..."
            print(f"  ✅ Planner: descripción generada ({len(data.get(desc_key,''))} chars)")

        # Stage 2: Stylist
        print("  [2/3] Stylist Agent...")
        data = await processor.stylist_agent.process(data)
        stylist_desc_key = "target_diagram_stylist_desc0"
        if stylist_desc_key in data:
            result["stages"]["stylist_desc"] = data[stylist_desc_key][:300] + "..."
            print(f"  ✅ Stylist: descripción refinada ({len(data.get(stylist_desc_key,''))} chars)")

        # Stage 3: Visualizer (generates the image)
        print("  [3/3] Visualizer Agent (generando imagen)...")
        data = await processor.visualizer_agent.process(data)

        # Find the image
        img_keys = [k for k in data if "base64_jpg" in k or "base64" in k]
        print(f"  Claves de imagen encontradas: {img_keys}")

        img_b64 = None
        for key in ["target_diagram_stylist_desc0_base64_jpg", "target_diagram_desc0_base64_jpg"]:
            if key in data and data[key]:
                img_b64 = data[key]
                print(f"  ✅ Visualizer: imagen encontrada en '{key}'")
                break

        if img_b64:
            # Save image
            ts = datetime.now().strftime("%H%M%S")
            lang_suffix = f"-{language}"
            out_path = OUTPUT_DIR / f"paperbanana-{test['id']}{lang_suffix}-{ts}.jpg"
            if "," in img_b64:
                img_b64 = img_b64.split(",")[1]
            img_bytes = base64.b64decode(img_b64)
            with open(out_path, "wb") as f:
                f.write(img_bytes)
            result["final_image_path"] = str(out_path)
            print(f"  ✅ Imagen guardada: {out_path} ({len(img_bytes)/1024:.1f} KB)")
        else:
            result["error"] = "No se encontró imagen en el output"
            print(f"  ❌ {result['error']}")
            print(f"  Keys disponibles: {list(data.keys())[:20]}")

    except Exception as e:
        import traceback
        result["error"] = str(e)
        result["traceback"] = traceback.format_exc()
        print(f"  ❌ Error: {e}")
        traceback.print_exc()

    return result


async def main(language: str = "es"):
    print("🍌 PaperBanana — Script en Español (run_es.py)")
    print(f"Idioma de salida: {'🇪🇸 Español' if language == 'es' else '🇺🇸 English'}")
    print(f"Output dir: {OUTPUT_DIR}")
    print()

    # Init config
    exp_config = config.ExpConfig(
        dataset_name="PaperBananaBench",
        task_name="diagram",
        exp_mode="demo_planner_critic",
        retrieval_setting="auto",  # dataset descargado ✅
        max_critic_rounds=1,
    )
    print(f"Modelo texto: {exp_config.model_name}")
    print(f"Modelo imagen: {exp_config.image_model_name}")

    # Init agents (language="es" activa prompts en español y labels en español)
    processor = PaperVizProcessor(
        exp_config=exp_config,
        vanilla_agent=VanillaAgent(exp_config=exp_config),
        planner_agent=PlannerAgent(exp_config=exp_config, language=language),
        visualizer_agent=VisualizerAgent(exp_config=exp_config),
        stylist_agent=StylistAgent(exp_config=exp_config, language=language),
        critic_agent=CriticAgent(exp_config=exp_config),
        retriever_agent=RetrieverAgent(exp_config=exp_config),
        polish_agent=PolishAgent(exp_config=exp_config),
    )

    results = []
    for test in TESTS:  # Los 3: meta + Cholula + Jorge
        result = await run_test(test, exp_config, processor, language=language)
        results.append(result)

    # Summary
    print(f"\n{'='*60}")
    print("📊 RESUMEN")
    print(f"{'='*60}")
    for r in results:
        status = "✅" if r["final_image_path"] else "❌"
        print(f"{status} {r['label']}")
        if r["final_image_path"]:
            print(f"   → {r['final_image_path']}")
        if r["error"]:
            print(f"   Error: {r['error'][:200]}")

    # Save results JSON
    report_path = OUTPUT_DIR / f"results-es-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    print(f"\n📝 Reporte guardado: {report_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PaperBanana — Generador de figuras en Español")
    parser.add_argument(
        "--lang",
        choices=["en", "es"],
        default="es",  # ← ESPAÑOL por default (diferente a run_custom.py)
        help="Idioma de salida para los textos de la figura (default: es / español)",
    )
    parser.add_argument(
        "--caption",
        type=str,
        default=None,
        help="Descripción de la figura a generar (modo single). Si se omite, ejecuta los 3 test cases.",
    )
    parser.add_argument(
        "--content",
        type=str,
        default="",
        help="Contexto adicional del paper (opcional, mejora la calidad)",
    )
    parser.add_argument(
        "--type",
        choices=["diagram", "plot"],
        default="diagram",
        help="Tipo de figura: diagram (diagramas) o plot (gráficas estadísticas)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Carpeta de salida (default: output/ o la configurada en OUTPUT_DIR)",
    )
    args = parser.parse_args()

    if args.caption:
        # Modo single: generar una sola figura a partir de --caption
        import uuid
        single_test = {
            "id": f"custom-{uuid.uuid4().hex[:6]}",
            "label": args.caption[:60],
            "caption": args.caption,
            "content": args.content,
        }
        if args.output:
            OUTPUT_DIR = Path(args.output)
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        async def run_single():
            print("🍌 PaperBanana — Modo Single (una figura)")
            print(f"Idioma: {'🇪🇸 Español' if args.lang == 'es' else '🇺🇸 English'}")
            print(f"Caption: {args.caption[:80]}...")
            print(f"Output: {OUTPUT_DIR}\n")

            exp_config = config.ExpConfig(
                dataset_name="PaperBananaBench",
                task_name=args.type,
                exp_mode="demo_planner_critic",
                retrieval_setting="auto",
                max_critic_rounds=1,
            )
            processor = PaperVizProcessor(
                exp_config=exp_config,
                vanilla_agent=VanillaAgent(exp_config=exp_config),
                planner_agent=PlannerAgent(exp_config=exp_config, language=args.lang),
                visualizer_agent=VisualizerAgent(exp_config=exp_config),
                stylist_agent=StylistAgent(exp_config=exp_config, language=args.lang),
                critic_agent=CriticAgent(exp_config=exp_config),
                retriever_agent=RetrieverAgent(exp_config=exp_config),
                polish_agent=PolishAgent(exp_config=exp_config),
            )
            result = await run_test(single_test, exp_config, processor, language=args.lang)
            if result["final_image_path"]:
                print(f"\n✅ Figura generada: {result['final_image_path']}")
            else:
                print(f"\n❌ Error: {result.get('error', 'Unknown')}")

        asyncio.run(run_single())
    else:
        asyncio.run(main(language=args.lang))
