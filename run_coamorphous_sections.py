"""
PaperBanana — Dos figuras del paper BZT-GZD
Figura A: SOLO metodología | Figura B: SOLO resultados
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

OUTPUT = Path("/mnt/agent-workspace/Buzón/Para-Jorge/paperbanana-test")
OUTPUT.mkdir(parents=True, exist_ok=True)

# ─── FIGURA A: SOLO METODOLOGÍA ────────────────────────────────────────
METODOLOGIA = {
    "id": "metodologia",
    "caption": (
        "Figure 1: Experimental methodology for the preparation and characterization "
        "of the Bezafibrate–Gliclazide (BZT–GZD) co-amorphous binary system. "
        "The workflow shows the melt-quench amorphization process with temperature-specific "
        "conditions per molar fraction, followed by the three-technique characterization pipeline: "
        "DSC for thermal analysis, ATR-FTIR for molecular interaction detection, "
        "and XRPD for structural stability monitoring over time."
    ),
    "content": """
## Methodology: Preparation and Characterization of BZT–GZD Co-Amorphous System

### Step 1 — Starting Materials
- Bezafibrate (BZT, Mw = 361.82 g/mol, BCS Class II drug, lipid regulator)
- Gliclazide (GZD, Mw = 323.41 g/mol, BCS Class II drug, hypoglycemic)
- Molar fractions prepared: x_BZT = 0.1, 0.3, 0.4, 0.5, 0.6, 0.7, 0.9
- Pre-processing: gentle grinding with mortar and pestle for 1 minute

### Step 2 — Melt-Quench Amorphization (Core Process)
- x_BZT = 0.5: heat to 160°C × 1 min → immediate quench to room temperature
- x_BZT = 0.7: heat to 180°C × 1 min → immediate quench to room temperature
- Temperatures selected from phase diagram (below eutectic melting point)
- Result: homogeneous amorphous solid solution formed
- Storage: desiccator at room temperature

### Step 3 — Thermal Characterization (DSC)
- Instrument: Diamond DSC PerkinElmer with intra-cooling
- Calibration: indium standard (Tm = 156.6°C, ΔH = 28.5 J/mol)
- Heating program (6-step cycle):
  1. Heat 30°C → 195°C at 10°C/min
  2. Isotherm 195°C × 1 min
  3. Cool 195°C → –20°C at 70°C/min (quench)
  4. Isotherm –20°C × 5 min
  5. Reheat –20°C → 190°C at 10°C/min
  6. Cool to 30°C at 70°C/min
- Measured: Tm (melting), eutectic point, Tg (glass transition)

### Step 4 — Molecular Interaction Analysis (ATR-FTIR)
- Instrument: PerkinElmer Spectrum 400 FTIR-ATR/NIR
- Scan range: 380–4000 cm⁻¹, resolution 4 cm⁻¹, 16 scans averaged
- Spectra normalized and baseline corrected
- Target: detect hydrogen bond formation between BZT and GZD

### Step 5 — Long-term Stability Monitoring (XRPD)
- Instrument: Rigaku Miniflex 600, Cu tube (λ = 1.5418 Å)
- Scan: 3–37° 2θ at 2°/min, step 0.05°
- Periodic analysis over 8+ years of storage in desiccator
- Criterion: absence of crystalline diffraction peaks = amorphous state maintained
""",
}

# ─── FIGURA B: SOLO RESULTADOS ─────────────────────────────────────────
RESULTADOS = {
    "id": "resultados",
    "caption": (
        "Figure 2: Key results from the Bezafibrate–Gliclazide (BZT–GZD) co-amorphous "
        "binary system study. Results include: (A) phase diagram showing eutectic composition "
        "at x_BZT = 0.5 and glass transition temperatures across all molar fractions; "
        "(B) ATR-FTIR evidence of hydrogen bond formation (redshifts: 1547→1538 cm⁻¹, "
        "1717→1609 cm⁻¹); (C) XRPD confirmation of amorphous state retention for >8 years; "
        "and (D) solubility enhancement: 2.1× for BZT and 1.5× for GZD at x_BZT=0.5, "
        "and 4× for BZT at x_BZT=0.7."
    ),
    "content": """
## Results: BZT–GZD Co-Amorphous Binary System

### Result 1 — Phase Diagram and Thermal Analysis (DSC)
- Pure drug melting points: BZT = 186.3°C, GZD = 169.3°C (matches literature)
- Eutectic composition: x_BZT = 0.5 (single DSC peak at 152.4°C) — 1:1 molar ratio
- Binary fractions x_BZT = 0.1, 0.4, 0.6, 0.7, 0.9: two peaks (eutectic + liquidus)
- Glass transition temperatures (amorphous state):
  - Pure BZT: Tg = 34.2°C (literature: 36.9°C — good agreement)
  - Pure GZD: Tg = 36.6°C
  - Binary system: single Tg across ALL compositions → confirms homogeneous amorphous solid solution
- No crystallization or melting events after Tg → thermally stable amorphous system

### Result 2 — Intermolecular Interactions (ATR-FTIR)
- Observed redshifts in co-amorphous systems vs. crystalline pure drugs:
  - Band shift: 1547 → 1538 cm⁻¹ (–9 cm⁻¹)
  - Band shift: 1717 → 1609 cm⁻¹ (–108 cm⁻¹, significant)
- Interpretation: hydrogen bond formation between BZT and GZD molecules
- Mechanism: intermolecular H-bonds prevent recrystallization (stabilize amorphous matrix)
- Confirms molecular-level homogeneous mixing of both APIs

### Result 3 — Long-term Stability (XRPD, 8+ years)
- Amorphous state confirmed at t=0: no crystalline diffraction peaks (3–37° 2θ)
- Periodic monitoring over 8+ years of desiccator storage
- ALL compositions retain amorphous state — ZERO recrystallization detected
- Key novelty: previous reports limited to 4–6 months; this is the longest stability study reported
- This directly validates the intermolecular H-bond stabilization mechanism (FTIR)

### Result 4 — Solubility Enhancement (HPLC quantification in Milli-Q water, 24h)
Comparison vs. crystalline pure drugs:

| System | BZT enhancement | GZD enhancement |
|--------|----------------|----------------|
| Physical mixture (PM) | Moderate | Moderate |
| CoA x_BZT = 0.5 | **2.1×** | **1.5×** |
| CoA x_BZT = 0.7 | **4.0×** | — |

- Solubility maintained over 8+ years (no crystallization = no solubility loss)
- Both drugs simultaneously enhanced — combination therapy advantage
- Physical mixtures show intermediate improvement vs. co-amorphous systems

### Clinical Significance
- Target: Metabolic Syndrome (diabetes + hypercholesterolemia often coexist)
- GZD (hypoglycemic) + BZT (lipid regulator) = simultaneous treatment
- Enhanced solubility → improved bioavailability → more effective treatment
- 8-year stability → viable pharmaceutical formulation shelf life
""",
}


async def generate_figure(test, processor, label):
    print(f"\n{'='*55}")
    print(f"  {label}")
    print(f"{'='*55}")

    data = {
        "caption": test["caption"],
        "content": test["content"],
        "visual_intent": test["caption"],
        "task_name": "diagram",
        "output_language": "Spanish",
    }

    print("  [0/3] Retriever...")
    data = await processor.retriever_agent.process(data)
    refs = data.get("top10_references", [])
    print(f"  ✅ {len(refs)} referencias: {refs[:3]}")

    print("  [1/3] Planner...")
    data = await processor.planner_agent.process(data)
    print(f"  ✅ {len(data.get('target_diagram_desc0',''))} chars")

    print("  [2/3] Stylist...")
    data = await processor.stylist_agent.process(data)
    print(f"  ✅ {len(data.get('target_diagram_stylist_desc0',''))} chars")

    print("  [3/3] Visualizer...")
    data = await processor.visualizer_agent.process(data)

    img_b64 = (data.get("target_diagram_stylist_desc0_base64_jpg") or
               data.get("target_diagram_desc0_base64_jpg"))

    if img_b64:
        if "," in img_b64:
            img_b64 = img_b64.split(",")[1]
        ts = datetime.now().strftime("%H%M%S")
        out = OUTPUT / f"paperbanana-coamorphous-{test['id']}-{ts}.jpg"
        with open(out, "wb") as f:
            f.write(base64.b64decode(img_b64))
        print(f"  ✅ Guardada: {out.name} ({out.stat().st_size/1024:.1f} KB)")
        return str(out)
    else:
        print("  ❌ No se generó imagen")
        return None


async def main():
    exp_config = config.ExpConfig(
        dataset_name="PaperBananaBench",
        task_name="diagram",
        exp_mode="demo_planner_critic",
        retrieval_setting="auto",
        max_critic_rounds=1,
    )
    print(f"📄 Paper: BZT-GZD (AAPS PharmSciTech 2025)")
    print(f"🎯 Dos figuras: METODOLOGÍA + RESULTADOS")
    print(f"🤖 {exp_config.model_name} + {exp_config.image_model_name}")

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

    path_a = await generate_figure(METODOLOGIA, processor, "🔬 FIGURA A — Solo Metodología")
    path_b = await generate_figure(RESULTADOS,  processor, "📊 FIGURA B — Solo Resultados")

    print(f"\n{'='*55}")
    print("RESUMEN:")
    print(f"  A (Metodología): {path_a or '❌'}")
    print(f"  B (Resultados):  {path_b or '❌'}")

asyncio.run(main())
