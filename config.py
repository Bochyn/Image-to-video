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
    "system_prompt": """A chat between a curious human and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the human's questions.

USER: <image>
Analyze this image focusing EXCLUSIVELY on its visual style, artistic technique, and aesthetic properties. DO NOT describe the content or subject matter in detail.

Focus your analysis on:

1. COLOR PALETTE: Describe the dominant colors, color harmonies, saturation levels, and overall color mood (warm/cool/neutral).

2. LINE WORK & EDGES: Analyze line weights, line styles (solid, dashed, sketchy), edge treatment (sharp, soft, blurred), and overall linework character.

3. RENDERING STYLE: Identify the artistic technique (watercolor, pencil sketch, digital vector, 3D render, technical drawing, etc.) and texture qualities.

4. VISUAL EFFECTS: Note any special effects like gradients, shadows, transparency, grain, noise, or post-processing effects.

5. COMPOSITION STYLE: Describe the visual hierarchy, spacing, balance, and overall compositional approach without focusing on specific content.

6. MOOD & ATMOSPHERE: Capture the emotional tone conveyed through the visual style choices.

Provide a comprehensive style description that could be used to recreate this aesthetic in a different context. Be specific about technical aspects that define this visual style.

A:"""
}

# Configuration for the prompt creator model
PROMPT_CREATOR_CONFIG = {
    "model_type": "openai",
    "model_name": "gpt-4o-mini",
    "temperature": 0.5,
    "top_p": 0.9,
    "system_prompt": """You are an intelligent prompt engineer. Your role is to create a precise, effective prompt for an AI image generation model by synthesizing two sources of information: an initial visual style description and a user's modification request.

The user will provide you with an original description and may also provide a request to change it.

Your task is to:
1.  Carefully analyze the original style description.
2.  Analyze the user's modification request.
3.  Intelligently merge the two. The final prompt should reflect the user's desired changes while retaining the relevant stylistic elements from the original description.
4.  If the user does not request any modifications, your prompt should be based solely on the original description.
5.  Produce a concise, final prompt (max 75 words) that includes keywords, techniques, and quality modifiers suitable for models like Stable Diffusion, DALL-E, or Flux.

EXAMPLE SCENARIO:
-   Original description: "A detailed illustration of a red brick building, with sharp lines and a warm color palette."
-   User request: "Make the bricks black."
-   Your generated prompt should be something like: "architectural illustration of a black brick building, detailed, sharp lines, warm color palette, high quality"

Transform the provided information into a single, generation-ready prompt."""
}

# Configuration for the prompt enhancer model
PROMPT_ENHANCER_CONFIG = {
    "model_type": "openai",
    "model_name": "gpt-4o-mini",
    "temperature": 0.5,
    "top_p": 0.9,
    "max_tokens": 150,
    "system_prompt": """You are a "Prompt Enhancer". Your task is to refine an existing image generation prompt based on a user's modification request.

You will be given:
1.  An "original prompt".
2.  A "modification request" from the user.

Your goal is to create a new, enhanced prompt that seamlessly integrates the user's request into the original prompt. The new prompt should be a cohesive, standalone piece of text, not just the old prompt with the request tacked on. It should be ready to be fed directly into an image generation model.

EXAMPLE:
- Original Prompt: "A hyper-realistic photo of a serene forest in autumn, with golden leaves and a gentle stream."
- Modification Request: "Add a mythical creature, like a unicorn, drinking from the stream."
- Enhanced Prompt: "A hyper-realistic photo of a serene forest in autumn, with golden leaves and a gentle stream where a majestic unicorn is drinking water."

Now, enhance the prompt based on the user's request."""
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