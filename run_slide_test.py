"""
PaperBanana — Prueba con diapositiva de clase (Q2003B)
Comparar output de PaperBanana vs NanoBanana para slides
Memito 🐹 — 01-Mar-2026
"""
import asyncio, base64, sys, json
from pathlib import Path
from datetime import datetime

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

SLIDE_TEST = {
    "id": "slide-doe-factorial",
    "caption": (
        "Figura 1: Portada de la Sesión 5 de Q2003B — Diseño Factorial Completo. "
        "Visualización técnica tipo presentación universitaria con cubo 3D del diseño 2³, "
        "nodos en las esquinas representando combinaciones de factores, fondo oscuro tecnológico "
        "con gradiente azul-teal y acentos cian brillantes. Texto en español. Formato 16:9."
    ),
    "content": """
## Diseño Factorial Completo — Sesión 5 de Diseño de Experimentos (Q2003B)

Esta diapositiva de portada introduce el tema de diseño factorial completo para un curso universitario
de ingeniería. El diseño es una presentación técnica de alto impacto visual con fondo oscuro.

**Contenido de la diapositiva:**

Panel izquierdo (40% del ancho):
- Título principal en texto grande y bold: "Diseño Factorial Completo"
- Subtítulo: "Del mono-factor al multi-factor"
- Metadatos del curso: "Q2003B · Sesión 5"
- Nombre del instructor: "Dr. Jorge Cruz-Angeles"
- Tipografía blanca sobre fondo oscuro

Panel derecho (60% del ancho):
- Visualización 3D de un cubo factorial 2³ (2 niveles × 3 factores)
- 8 nodos en las esquinas del cubo, cada uno etiquetado con la combinación de factores (−, +)
- Líneas de conexión que muestran las rutas experimentales entre tratamientos
- Capas semitransparentes que muestran los planos factoriales (Factor A, Factor B, Factor C)
- Flechas de flujo de datos apuntando hacia mini-gráficas con resultados
- Gradiente de color cian-azul en las aristas del cubo

**Estilo visual:**
- Fondo: gradiente azul marino oscuro a teal profundo (#0a192f → #0d3d56)
- Patrón de fondo: circuitos impresos sutiles o cuadrícula hexagonal
- Líneas de acento: cian brillante (#00d4ff) y teal (#00b4d8)
- Estilo: infográfico técnico de alta tecnología, estética de ciencia de datos
- Formato: presentación universitaria 16:9, alta resolución
""",
}


async def main():
    exp_config = config.ExpConfig(
        dataset_name="PaperBananaBench",
        task_name="diagram",
        exp_mode="demo_planner_critic",
        retrieval_setting="auto",
        max_critic_rounds=1,
    )
    print(f"Modelo texto: {exp_config.model_name}")
    print(f"Modelo imagen: {exp_config.image_model_name}")

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

    data = {
        "caption": SLIDE_TEST["caption"],
        "content": SLIDE_TEST["content"],
        "visual_intent": SLIDE_TEST["caption"],
        "task_name": "diagram",
        "output_language": "Spanish",
    }

    print("\n🖼️ Generando diapositiva con PaperBanana...")

    # Retriever
    print("  [0/3] Retriever...")
    data = await processor.retriever_agent.process(data)
    refs = data.get("top10_references", [])
    print(f"  ✅ {len(refs)} referencias: {refs[:3]}")

    # Planner
    print("  [1/3] Planner...")
    data = await processor.planner_agent.process(data)
    print(f"  ✅ Desc: {len(data.get('target_diagram_desc0',''))} chars")

    # Stylist
    print("  [2/3] Stylist...")
    data = await processor.stylist_agent.process(data)
    print(f"  ✅ Refined: {len(data.get('target_diagram_stylist_desc0',''))} chars")

    # Visualizer
    print("  [3/3] Visualizer...")
    data = await processor.visualizer_agent.process(data)

    img_b64 = data.get("target_diagram_stylist_desc0_base64_jpg") or data.get("target_diagram_desc0_base64_jpg")
    if img_b64:
        ts = datetime.now().strftime("%H%M%S")
        out = OUTPUT_DIR / f"paperbanana-slide-doe-{ts}.jpg"
        if "," in img_b64:
            img_b64 = img_b64.split(",")[1]
        with open(out, "wb") as f:
            f.write(base64.b64decode(img_b64))
        print(f"\n✅ Slide guardada: {out} ({out.stat().st_size/1024:.1f} KB)")
    else:
        print("❌ No se generó imagen")

asyncio.run(main())
