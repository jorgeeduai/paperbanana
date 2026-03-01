# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Vanilla Agent - Directly rendering images based on the method section.
"""

import json
from typing import Dict, Any
from google.genai import types
import base64, io, asyncio
from PIL import Image

from utils import generation_utils
from .base_agent import BaseAgent


class PlannerAgent(BaseAgent):
    """Planner Agent to generate images based on user queries"""

    def __init__(self, language: str = "en", **kwargs):
        super().__init__(**kwargs)
        self.model_name = self.exp_config.model_name
        self.language = language  # "en" (default) or "es" (español)

        # Task-specific configurations
        if "plot" in self.exp_config.task_name:
            self.system_prompt = (
                PLOT_PLANNER_AGENT_SYSTEM_PROMPT_ES
                if language == "es"
                else PLOT_PLANNER_AGENT_SYSTEM_PROMPT
            )
            self.task_config = {
                "task_name": "plot",
                "content_label": "Plot Raw Data",
                "visual_intent_label": "Visual Intent of the Desired Plot",
            }
        else:
            self.system_prompt = (
                DIAGRAM_PLANNER_AGENT_SYSTEM_PROMPT_ES
                if language == "es"
                else DIAGRAM_PLANNER_AGENT_SYSTEM_PROMPT
            )
            self.task_config = {
                "task_name": "diagram",
                "content_label": "Methodology Section",
                "visual_intent_label": "Diagram Caption",
            }

    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Unified processing method that works for both diagram and plot tasks.
        Uses task_config to determine task-specific parameters.
        Expects data['top10_references'] to be already populated by retriever.
        """
        cfg = self.task_config
        
        raw_content = data["content"]
        content = json.dumps(raw_content) if isinstance(raw_content, (dict, list)) else raw_content
        description = data["visual_intent"]

        content_list = []
        
        # Check if retriever has already provided full examples (e.g., in manual mode)
        examples = data.get("retrieved_examples", [])
        if not examples:
            retrieved_ids = data.get("top10_references", [])
            if retrieved_ids:  # Skip loading dataset if no references requested
                with open(self.exp_config.work_dir / f"data/PaperBananaBench/{cfg['task_name']}/ref.json", "r", encoding="utf-8") as f:
                    candidate_pool = json.load(f)
                id_to_item = {item["id"]: item for item in candidate_pool}
                examples = [id_to_item[ref_id] for ref_id in retrieved_ids if ref_id in id_to_item]
        
        user_prompt = ""
        for idx, item in enumerate(examples):
            user_prompt += f"Example {idx+1}:\n"
            
            item_content = item["content"]
            if isinstance(item_content, (dict, list)):
                item_content = json.dumps(item_content)
            
            user_prompt += f"{cfg['content_label']}: {item_content}\n"
            user_prompt += f"{cfg['visual_intent_label']}: {item['visual_intent']}\nReference {cfg['task_name'].capitalize()}: "
            content_list.append({"type": "text", "text": user_prompt})
            
            # Resolve relative path using work_dir
            image_path = self.exp_config.work_dir / f"data/PaperBananaBench/{cfg['task_name']}" / item["path_to_gt_image"]
            with open(image_path, "rb") as f:
                ref_image_base64 = base64.b64encode(f.read()).decode("utf-8")
            content_list.append({"type": "image", "image_base64": ref_image_base64})
            user_prompt = ""

        user_prompt += f"Now, based on the following {cfg['content_label'].lower()} and {cfg['visual_intent_label'].lower()}, provide a detailed description for the figure to be generated.\n"
        user_prompt += f"{cfg['content_label']}: {content}\n{cfg['visual_intent_label']}: {description}\n"
        # Language instruction injected from data or from agent default
        output_language = data.get("output_language", "Spanish" if self.language == "es" else None)
        if output_language:
            user_prompt += f"IMPORTANT: All visible text labels inside the figure must be written in {output_language}.\n"
        user_prompt += "Detailed description of the target figure to be generated"
        if cfg["task_name"] == "diagram":
            user_prompt += " (do not include figure titles)"
        user_prompt += ":"

        content_list.append({"type": "text", "text": user_prompt})

        response_list = await generation_utils.call_gemini_with_retry_async(
            model_name=self.model_name,
            contents=content_list,
            config=types.GenerateContentConfig(
                system_instruction=self.system_prompt,
                temperature=self.exp_config.temperature,
                candidate_count=1,
                max_output_tokens=50000,
            ),
            max_attempts=5,
            retry_delay=5,
        )
        
        for idx, response in enumerate(response_list):
            data[f"target_{cfg['task_name']}_desc{idx}"] = response.strip()

        return data




DIAGRAM_PLANNER_AGENT_SYSTEM_PROMPT = """
I am working on a task: given the 'Methodology' section of a paper, and the caption of the desired figure, automatically generate a corresponding illustrative diagram. I will input the text of the 'Methodology' section, the figure caption, and your output should be a detailed description of an illustrative figure that effectively represents the methods described in the text.

To help you understand the task better, and grasp the principles for generating such figures, I will also provide you with several examples. You should learn from these examples to provide your figure description.

** IMPORTANT: **
Your description should be as detailed as possible. Semantically, clearly describe each element and their connections. Formally, include various details such as background style (typically pure white or very light pastel), colors, line thickness, icon styles, etc. Remember: vague or unclear specifications will only make the generated figure worse, not better.
"""

DIAGRAM_PLANNER_AGENT_SYSTEM_PROMPT_ES = """
Estoy trabajando en una tarea: dada la sección de 'Metodología' de un artículo científico, y el pie de figura deseado, generar automáticamente un diagrama ilustrativo correspondiente. Recibiré el texto de la sección de 'Metodología' y el pie de figura, y tu salida debe ser una descripción detallada de una figura ilustrativa que represente eficazmente los métodos descritos en el texto.

Para ayudarte a entender mejor la tarea y comprender los principios para generar dichas figuras, también te proporcionaré varios ejemplos. Debes aprender de estos ejemplos para elaborar tu descripción de figura.

** IMPORTANTE: **
Tu descripción debe ser lo más detallada posible. Semánticamente, describe claramente cada elemento y sus conexiones. Formalmente, incluye detalles como el estilo de fondo (típicamente blanco puro o pastel muy claro), colores, grosor de líneas, estilos de íconos, etc. Recuerda: las especificaciones vagas o poco claras solo empeorarán la figura generada.

** IDIOMA DE SALIDA: **
Todos los textos que aparezcan DENTRO de la figura (etiquetas, títulos de secciones, nombres de componentes, leyendas) deben estar en ESPAÑOL. La descripción que produces puede estar en inglés, pero especifica explícitamente que los elementos de texto visibles en la figura deben estar en español.
"""

PLOT_PLANNER_AGENT_SYSTEM_PROMPT = """
I am working on a task: given the raw data (typically in tabular or json format) and a visual intent of the desired plot, automatically generate a corresponding statistical plot that are both accurate and aesthetically pleasing. I will input the raw data and the plot visual intent, and your output should be a detailed description of an illustrative plot that effectively represents the data.  Note that your description should include all the raw data points to be plotted.

To help you understand the task better, and grasp the principles for generating such plots, I will also provide you with several examples. You should learn from these examples to provide your plot description.

** IMPORTANT: **
Your description should be as detailed as possible. For content, explain the precise mapping of variables to visual channels (x, y, hue) and explicitly enumerate every raw data point's coordinate to be drawn to ensure accuracy. For presentation, specify the exact aesthetic parameters, including specific HEX color codes, font sizes for all labels, line widths, marker dimensions, legend placement, and grid styles. You should learn from the examples' content presentation and aesthetic design (e.g., color schemes).
"""

PLOT_PLANNER_AGENT_SYSTEM_PROMPT_ES = """
Estoy trabajando en una tarea: dados los datos en bruto (típicamente en formato tabular o JSON) y la intención visual de la gráfica deseada, generar automáticamente una gráfica estadística que sea precisa y estéticamente atractiva. Recibiré los datos en bruto y la intención visual, y tu salida debe ser una descripción detallada de una gráfica ilustrativa que represente eficazmente los datos. Nota: tu descripción debe incluir todos los puntos de datos en bruto a graficar.

Para ayudarte a entender mejor la tarea, también te proporcionaré varios ejemplos de los que debes aprender.

** IMPORTANTE: **
Tu descripción debe ser lo más detallada posible. Para el contenido, explica el mapeo preciso de variables a canales visuales (x, y, tonalidad) y enumera explícitamente las coordenadas de cada punto de datos. Para la presentación, especifica los parámetros estéticos exactos, incluyendo códigos de color HEX específicos, tamaños de fuente para todas las etiquetas, anchos de línea, dimensiones de marcadores, ubicación de leyenda y estilos de cuadrícula.

** IDIOMA DE SALIDA: **
Todos los textos visibles en la gráfica (etiquetas de ejes, título, leyenda) deben estar en ESPAÑOL.
"""

