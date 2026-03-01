"""
PaperBanana — Prueba custom sin Streamlit
Jorge Cruz-Angeles & Memito 🐹 — 28-Feb-2026

Uso:
  .venv/bin/python run_custom.py              # inglés (default)
  .venv/bin/python run_custom.py --lang es    # español

Para español por default usa run_es.py.
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
# TEST CASES
# ─────────────────────────────────────────────────────────────

TESTS = [
    {
        "id": "paperbanana-meta",
        "label": "PaperBanana explicando PaperBanana 🍌 (meta-figura)",
        "caption": (
            "Figure 1: Overview of the PaperBanana multi-agent framework for automated academic illustration. "
            "Given a method section and figure caption as input, five specialized agents collaborate in sequence: "
            "the Retriever identifies relevant reference diagrams, the Planner synthesizes a detailed visual description "
            "via in-context learning, the Stylist refines it to academic aesthetic standards, the Visualizer generates "
            "the image using a state-of-the-art image generation model, and the Critic closes the loop through "
            "iterative multi-round refinement until a publication-ready illustration is produced."
        ),
        "content": """
## PaperBanana: A Reference-Driven Multi-Agent Framework for Academic Illustration

PaperBanana automates the generation of publication-quality scientific diagrams and plots from raw
method section text and figure captions. The framework orchestrates five specialized agents in a
structured pipeline inspired by creative team collaboration:

**Input:**
- Method section content (Markdown text describing the scientific approach)
- Figure caption (communicative intent and description of the desired illustration)

**Agent Pipeline:**

1. **Retriever Agent**
   - Searches a curated reference pool (PaperBananaBench dataset) for the most relevant existing diagrams
   - Uses semantic similarity to identify top-k reference examples
   - Provides few-shot examples to downstream agents for in-context learning

2. **Planner Agent**
   - Receives: method content + visual intent + reference examples with images
   - Translates scientific content into a comprehensive textual description of the figure to generate
   - Uses in-context learning from reference diagrams to guide visual structure
   - Output: detailed figure description (~3500-4000 characters)

3. **Stylist Agent**
   - Receives: planner description + automatically synthesized style guidelines
   - Refines the description to adhere to academic aesthetic standards
   - Adds specifications for color palette, layout, typography, and visual hierarchy
   - Output: aesthetically refined description (~4500-5000 characters)

4. **Visualizer Agent**
   - Receives: stylist-refined description
   - Transforms textual description into visual output using Gemini image generation model
   - Generates multiple candidate images in parallel for comparison
   - Output: base64-encoded JPG image

5. **Critic Agent**
   - Receives: generated image + original description + caption
   - Evaluates the image against scientific accuracy and aesthetic standards
   - Provides structured feedback and improvement suggestions
   - Forms a closed-loop with the Visualizer for multi-round iterative refinement
   - Stops when quality threshold is reached or max_rounds is exhausted

**Output:** Publication-ready illustration in JPG format, suitable for academic papers in AI/ML conferences and journals.
""",
    },
    {
        "id": "cholula",
        "label": "Cholula NPs — ML Antitumor (Ma et al. 2025)",
        "caption": (
            "Figure 1: Overview of the interpretable machine learning pipeline for predicting "
            "antitumor effects of metal and metal oxide nanoparticles. "
            "The framework integrates quantum chemistry descriptors with toxicity data "
            "from 152 articles (2765 instances), applies LightGBM, CNN, and MLP models, "
            "and uses SHAP for interpretability."
        ),
        "content": """
## Machine Learning Pipeline for Antitumor Nanoparticle Toxicity Prediction

We combined quantum chemistry calculations with published toxicity data to develop an
interpretable machine learning framework achieving over 90% accuracy in cross-validation.

**Dataset**: 39 descriptors extracted from 152 articles, comprising 2765 instances
covering various nanoparticle types, detection methods, and cell types.

**Feature Engineering**:
- Jaccard similarity coefficient for enhanced data representation
- Key features: concentration, exposure time, zeta potential, diameter, COSMO area (CA),
  coating, testing methods, cell types, metal electronegativity, HOMO energy, molecular weight

**Models Evaluated**:
1. **LightGBM**: Efficient gradient boosting with histogram-based learning; grid search
   for learning rate, tree depth, and number of leaves; optimized via cross-validation.
2. **CNN**: Two convolutional layers (32 and 64 filters, kernel size 3) with max pooling,
   fully connected layers, and sigmoid activation for binary classification.
3. **MLP**: Three fully connected layers learning nonlinear relationships between features.

**Interpretability**:
- Feature Importance analysis to rank descriptors
- SHAP (Shapley Additive Explanations) to explain individual predictions

**Validation**: Synthesized novel metal oxide nanoparticles and assessed physicochemical
properties and antitumor toxicity experimentally to validate model generalizability.
""",
    },
    {
        "id": "jorge",
        "label": "Jorge — MetaChem NOVUS 2026 (IA Disciplinar Q1027/Q1028)",
        "caption": (
            "Figure 1: Framework of MetaChem — a specialized AI-driven pedagogical system "
            "integrating a chemistry-expert LLM chatbot, AI-generated podcasts (NotebookLM), "
            "and adaptive formative evaluation for undergraduate chemistry courses "
            "(Q1027 Biochemistry and Q1028 General Chemistry) at Tecnológico de Monterrey."
        ),
        "content": """
## MetaChem: Specialized Disciplinary AI for Chemistry Education

MetaChem is an AI-powered educational framework for undergraduate chemistry courses
(Q1027 Biochemistry, Q1028 General Chemistry) designed to improve conceptual understanding,
reduce cognitive load, and promote active learning through three integrated components:

**Component 1 — GPTeach Chemistry Expert Chatbot**:
- LLM fine-tuned on discipline-specific content (biomolecules, thermodynamics, mixtures)
- Socratic dialogue: guides students through problem-solving without giving direct answers
- Adaptive feedback based on student responses
- Deployed on Canvas LMS; accessible 24/7

**Component 2 — AI-Generated Podcast Pipeline (NotebookLM)**:
- Source material: lecture notes, textbook chapters, lab protocols
- NotebookLM generates audio dialogues contextualizing each topic
- Weekly podcast episodes distributed via Spotify
- Previous results: 97% student preference over traditional reading (n=76)

**Component 3 — Formative AI Evaluator**:
- Immersive role-based scenarios (student as scientist, researcher, or engineer)
- Rubric-aligned automated feedback with citations from course materials
- Data collected: accuracy, time-on-task, self-regulated learning indicators

**Experimental Design**:
- Quasi-experimental: treatment group (MetaChem) vs control group (traditional)
- Pre/post conceptual tests (validated instruments)
- 3 periods, ~400 students total
- Outcome metrics: conceptual gains (Cohen's d), exam scores, engagement
""",
    },
]


async def run_test(test: dict, exp_config, processor, language: str = "en") -> dict:
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
            out_path = OUTPUT_DIR / f"paperbanana-{test['id']}-{ts}.jpg"
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


async def main(language: str = "en"):
    print("🍌 PaperBanana — Prueba custom de Memito & Jorge")
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

    # Init agents (language="es" activa prompts en español)
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
    report_path = OUTPUT_DIR / f"results-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    print(f"\n📝 Reporte guardado: {report_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PaperBanana — Generador de figuras académicas")
    parser.add_argument(
        "--lang",
        choices=["en", "es"],
        default="en",
        help="Idioma de salida para los textos de la figura (default: en / inglés)",
    )
    args = parser.parse_args()
    asyncio.run(main(language=args.lang))
