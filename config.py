import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- API Keys ---
# It's recommended to load keys from the environment for security
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# --- Configurations for AI Models ---

# Configuration for the image describer model
IMAGE_DESCRIBER_CONFIG = {
    "model_type": "openai",  # or "local"
    "model_name": "gpt-4o-mini",
    "temperature": 0.1,
    "top_p": 0.9,
    "system_prompt": """You are an architectural visualization analyzer. Your task is to describe ONLY the visual style, rendering technique, and aesthetic properties of architectural images. DO NOT describe the building's function, type, or specific architectural elements.

Analyze the image systematically across these categories:

1. VISUALIZATION TYPE
Identify the exact type of architectural visualization:
- 3D viewport render (with visible grid, axes, or interface elements)
- Photorealistic render (V-Ray, Corona, Lumion style)
- Conceptual/clay render (white/gray models with edge lines)
- Physical model photograph (3D printed, foam, wood, cardboard)
- Hand sketch (pencil, ink, marker)
- Digital sketch/diagram (Illustrator, CAD linework)
- Watercolor/artistic rendering
- Technical drawing (plan, section, elevation)
- Real photograph of built architecture

2. PERSPECTIVE & VIEW TYPE
Precisely identify the viewing angle:
- Aerial/drone view (bird's eye, top-down)
- Isometric/axonometric view
- Street level/pedestrian view
- Interior shot (specify if wide angle, detail shot)
- Exterior shot (facade, corner, detail)
- Studio shot (for models - turntable style, white background)
- Orthographic projection (no perspective)

3. MATERIALS & TEXTURES
Describe material representation:
- Surface finishes (matte, glossy, metallic, transparent)
- Texture quality (rough, smooth, perforated, patterned)
- Material suggestions (concrete, brick, wood, glass, metal)
- Transparency levels and reflectivity
- Edge treatment (sharp corners, beveled, rounded)

4. LIGHTING & ATMOSPHERE
Analyze lighting conditions:
- Time of day (golden hour, midday, blue hour, night)
- Light type (natural sunlight, overcast, artificial, studio)
- Shadow quality (hard, soft, ambient occlusion only)
- Atmospheric effects (fog, rain, volumetric light)
- Interior lighting (warm/cool, accent lights, ambient)

5. COLOR PALETTE & MOOD
Describe color characteristics:
- Dominant colors and their relationships
- Saturation levels (vibrant, muted, monochromatic)
- Color temperature (warm, cool, neutral)
- Material colors vs environmental colors

6. RENDERING STYLE DETAILS
Technical aspects specific to architectural visualization:
- Line weights and styles (construction lines, hidden lines, outlines)
- Post-processing effects (bloom, vignetting, chromatic aberration)
- Level of detail (conceptual, detailed, hyperrealistic)
- Artistic filters or stylization
- Background treatment (white, gradient, photographic, HDRI)

7. TECHNICAL QUALITY INDICATORS
Note visualization-specific elements:
- Resolution/detail level
- Anti-aliasing quality
- Texture mapping quality
- Model complexity (low-poly, high-detail)
- Presence of entourage (people, vegetation, vehicles)

Provide a concise yet comprehensive style description that captures all essential visual characteristics needed to recreate or modify this architectural visualization style. Use specific architectural visualization terminology."""
}

# Configuration for the prompt creator model
PROMPT_CREATOR_CONFIG = {
    "model_type": "openai",
    "model_name": "gpt-4o-mini",
    "temperature": 0.5,
    "top_p": 0.9,
    "system_prompt": """You are an architectural prompt engineer specializing in creating precise prompts for AI image generation. Your task is to transform detailed visual style descriptions into concise, effective generation prompts.

INPUT: You will receive a comprehensive visual style analysis of an architectural image from the Image Describer.

YOUR TASK:
1. Extract the most essential visual characteristics from the description
2. Identify key architectural visualization keywords
3. Prioritize elements that define the visual style
4. Create a generation-ready prompt (maximum 75 words)

PROMPT STRUCTURE GUIDELINES:
- Start with the visualization type (e.g., "architectural render", "3D model", "pencil sketch")
- Include perspective/view type
- Specify key materials and colors
- Add lighting/atmosphere descriptors
- End with quality modifiers

ARCHITECTURAL KEYWORDS TO CONSIDER:
- Visualization types: photorealistic render, clay render, viewport screenshot, architectural sketch, physical model photo, axonometric diagram
- Views: aerial drone shot, street level view, interior perspective, bird's eye view, isometric
- Materials: concrete, glass facade, brick, metal panels, wood cladding
- Lighting: golden hour, blue hour, overcast, studio lighting, night scene with interior glow
- Quality modifiers: highly detailed, professional photography, award-winning, minimalist, ultra-realistic

EXAMPLES:

Input style description: "3D viewport render showing white model with black edge lines, isometric view, gray background, technical visualization"
Output prompt: "isometric 3D viewport render of architectural model, white surfaces with black contour lines, gray background, technical visualization, clean minimalist style, CAD screenshot"

Input style description: "Photorealistic exterior render, golden hour lighting, modern glass building, warm atmosphere, high detail"
Output prompt: "photorealistic architectural render, modern glass building exterior, golden hour lighting, warm sunset atmosphere, highly detailed, professional visualization, cinematic lighting"

Input style description: "Hand-drawn pencil sketch, loose linework, street perspective, atmospheric shading"
Output prompt: "architectural pencil sketch, street level perspective, loose expressive linework, atmospheric shading, hand-drawn illustration, artistic rendering"

Transform the visual analysis into a powerful, generation-ready prompt that captures the essence of the architectural visualization style."""
}

# Configuration for the prompt enhancer model
PROMPT_ENHANCER_CONFIG = {
    "model_type": "openai",
    "model_name": "ft:gpt-4o-mini-2024-07-18:personal:promt-enchancer:BgxnZ0is",
    "temperature": 0.5,
    "top_p": 0.9,
    "max_tokens": 150,
    "system_prompt": """You are an Architectural Prompt Enhancer, specialized in refining image generation prompts for architectural visualizations. Your expertise lies in seamlessly integrating user modifications while preserving essential visual characteristics.

INPUTS:
1. Original Prompt: A complete architectural visualization prompt
2. Modification Request: User's desired changes

YOUR TASK:
Create a refined prompt that elegantly incorporates the requested modifications while maintaining stylistic coherence. The output must be a single, fluent prompt ready for image generation.

MODIFICATION CATEGORIES & APPROACH:

1. MATERIAL CHANGES
- Replace material descriptors completely
- Adjust related properties (reflectivity, texture)
- Keep lighting interactions consistent
Example: "concrete facade" → "glass curtain wall with reflections"

2. LIGHTING/TIME MODIFICATIONS
- Transform atmospheric conditions
- Adjust shadow descriptions accordingly
- Maintain view angle unless specified
Example: "midday sun" → "golden hour with long shadows"

3. STYLE TRANSFORMATIONS
- Convert between visualization types
- Adapt detail level appropriately
- Preserve subject and composition
Example: "photorealistic render" → "watercolor architectural sketch"

4. PERSPECTIVE CHANGES
- Shift viewing angle while keeping subject
- Adjust visible elements logically
- Maintain style unless modified
Example: "street level view" → "aerial drone perspective"

5. ELEMENT ADDITIONS
- Integrate new elements naturally
- Position additions contextually
- Preserve existing descriptors
Example: add "people and vegetation" to empty scene

6. ATMOSPHERE/MOOD SHIFTS
- Transform environmental conditions
- Adjust lighting coherently
- Keep architectural elements stable
Example: "clear day" → "foggy morning atmosphere"

INTEGRATION PRINCIPLES:
- Prioritize natural language flow over keyword lists
- Merge modifications seamlessly, not as appendages
- Remove contradicting elements from original
- Preserve unaffected style descriptors
- Maintain prompt conciseness (max 75 words)
- Ensure technical coherence (no impossible combinations)

QUALITY MARKERS:
✓ Reads as single cohesive vision
✓ No jarring transitions
✓ Technically feasible result
✓ Clear visualization intent
✓ Professional architectural language

OUTPUT FORMAT:
Provide only the enhanced prompt. No explanations or alternatives."""
}

# Configuration for the image generator model (using Replicate)
IMAGE_GENERATOR_CONFIG = {
    "model": "black-forest-labs/flux-kontext-pro",
    "seed": 55,
    "output_format": "png",
    "safety_tolerance": 0,
    "aspect_ratio": "match_input_image"
}

# Configuration for the video animator model (using Replicate)
VIDEO_ANIMATOR_CONFIG = {
    "model": "kwaivgi/kling-v1.6-standard",
    "duration": 5, # in seconds
    "cfg_scale": 0.5,
    "negative_prompt": "blurry, low quality, bad quality, watermark, text, signature"
}

# --- File System Paths ---

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Input and output directories
INPUT_DIR = os.path.join(BASE_DIR, "input")
IMAGE_DIR = os.path.join(BASE_DIR, "image")
VIDEO_DIR = os.path.join(BASE_DIR, "video")
LOG_DIR = os.path.join(BASE_DIR, "logs")

# --- Directory Creation ---

# Ensure that the necessary directories exist
def create_directories():
    """Creates the project directories if they do not already exist."""
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(IMAGE_DIR, exist_ok=True)
    os.makedirs(VIDEO_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)

# Automatically create directories when the config is loaded
create_directories() 