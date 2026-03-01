"""
PaperBanana — Figura del paper CoAmorphous BZT-GZD de Jorge (AAPS PharmSciTech 2025)
Memito 🐹 — 01-Mar-2026
"""
import asyncio, base64, sys
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

# ─── PAPER REAL DE JORGE ────────────────────────────────────────────────
CAPTION = (
    "Figure 2: Schematic overview of the co-amorphous binary system preparation and "
    "characterization pipeline for the Bezafibrate–Gliclazide (BZT–GZD) system. "
    "The workflow illustrates the melt-quench amorphization process, multi-technique "
    "characterization (DSC phase diagram, ATR-FTIR hydrogen bonding, XRPD stability), "
    "and resulting solubility enhancement outcomes across different molar fractions (x_BZT = 0.1–0.9). "
    "Long-term stability retention of the amorphous state for more than eight years is highlighted."
)

CONTENT = """
## Co-Amorphous Binary System: Bezafibrate–Gliclazide (BZT–GZD)

### Background and Motivation
Approximately 75% of existing drugs exhibit low aqueous solubility (BCS Class II).
Gliclazide (GZD, hypoglycemic) and Bezafibrate (BZT, lipid-regulator) both treat
Metabolic Syndrome components. The co-amorphous (CoA) strategy combines two APIs to
simultaneously improve solubility and prevent recrystallization via intermolecular
hydrogen bonds, offering a superior alternative to drug-polymer systems.

### Materials
- Bezafibrate (BZT, Mw = 361.82 g/mol, Sigma-Aldrich, ≥98%)
- Gliclazide (GZD, Mw = 323.41 g/mol, Sigma-Aldrich, ≥98%)
- Molar fractions studied: x_BZT = 0.1, 0.3, 0.4, 0.5, 0.6, 0.7, 0.9

### Preparation: Melt-Quench Technique
1. Pure drugs and physical mixtures ground with mortar and pestle (1 min)
2. Placed on aluminum plate and heated in furnace:
   - x_BZT = 0.5: heated to 160°C for 1 minute until complete melting
   - x_BZT = 0.7: heated to 180°C for 1 minute until complete melting
3. Immediately quench-cooled to room temperature → amorphous solid formed
4. Stored in desiccator at room temperature

### Characterization Pipeline (multi-technique approach)

**1. Differential Scanning Calorimetry (DSC) — Phase Diagram**
- Endothermic melting peaks: BZT at 186.3°C, GZD at 169.3°C
- Eutectic composition at x_BZT = 0.5 (single peak at 152.4°C)
- Single glass transition temperature (Tg) across all compositions → confirms homogeneous amorphous solid solution
- Pure amorphous Tg: BZT = 34.2°C, GZD = 36.6°C

**2. ATR-FTIR Spectroscopy — Intermolecular Interactions**
- Redshift of IR bands: 1547 → 1538 cm⁻¹ and 1717 → 1609 cm⁻¹
- Evidence of hydrogen bond formation between BZT and GZD molecules
- Confirms molecular-level homogeneous distribution of co-formers

**3. X-Ray Powder Diffraction (XRPD) — Long-term Stability**
- Amorphous state confirmed by absence of crystalline diffraction peaks
- Periodic analysis over 8+ years of storage (unique long-term dataset)
- All compositions retain amorphous state — no recrystallization detected

### Results: Solubility Enhancement
Solubility studies in Milli-Q water (24h equilibration, HPLC quantification):
- x_BZT = 0.5: BZT solubility increased 2.1× ; GZD solubility increased 1.5×
- x_BZT = 0.7: BZT solubility increased 4× vs crystalline pure drug
- Physical mixtures show intermediate improvement vs co-amorphous systems
- Enhanced solubility maintained over 8+ years of storage

### Key Innovation
First report of a BZT-GZD co-amorphous binary system with:
- Simultaneous solubility enhancement of both drugs
- Verified amorphous stability for >8 years (longest reported for any CoA system)
- Potential combination therapy for Metabolic Syndrome (diabetes + hypercholesterolemia)
"""

async def main():
    exp_config = config.ExpConfig(
        dataset_name="PaperBananaBench",
        task_name="diagram",
        exp_mode="demo_planner_critic",
        retrieval_setting="auto",
        max_critic_rounds=1,
    )
    print(f"📄 Paper: BZT-GZD Co-Amorphous System (Jorge Cruz-Angeles, AAPS PharmSciTech 2025)")
    print(f"🤖 Modelos: {exp_config.model_name} + {exp_config.image_model_name}\n")

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
        "caption": CAPTION,
        "content": CONTENT,
        "visual_intent": CAPTION,
        "task_name": "diagram",
        "output_language": "Spanish",
    }

    print("  [0/3] Retriever — buscando papers similares de farmacia/materiales...")
    data = await processor.retriever_agent.process(data)
    refs = data.get("top10_references", [])
    print(f"  ✅ {len(refs)} referencias encontradas: {refs[:4]}")

    print("  [1/3] Planner — traduciendo métodos a descripción visual...")
    data = await processor.planner_agent.process(data)
    desc = data.get("target_diagram_desc0", "")
    print(f"  ✅ Descripción: {len(desc)} chars")

    print("  [2/3] Stylist — refinando para estética académica...")
    data = await processor.stylist_agent.process(data)
    styled = data.get("target_diagram_stylist_desc0", "")
    print(f"  ✅ Refinada: {len(styled)} chars")

    print("  [3/3] Visualizer — generando imagen con NanoBanana Pro...")
    data = await processor.visualizer_agent.process(data)

    img_b64 = (data.get("target_diagram_stylist_desc0_base64_jpg") or
               data.get("target_diagram_desc0_base64_jpg"))

    if img_b64:
        if "," in img_b64:
            img_b64 = img_b64.split(",")[1]
        ts = datetime.now().strftime("%H%M%S")
        out = OUTPUT_DIR / f"paperbanana-coamorphous-btg-gzd-{ts}.jpg"
        with open(out, "wb") as f:
            f.write(base64.b64decode(img_b64))
        size_kb = out.stat().st_size / 1024
        print(f"\n✅ Figura guardada: {out.name} ({size_kb:.1f} KB)")
    else:
        print("❌ No se generó imagen")
        print("Keys disponibles:", [k for k in data if "base64" in k or "desc" in k])

asyncio.run(main())
