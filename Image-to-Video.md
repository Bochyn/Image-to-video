# Image-to-Video - Dokumentacja Projektu

## Koncepcja Aplikacji

### Cel
Aplikacja automatyzująca proces tworzenia animowanych wideo na podstawie stylu artystycznego z obrazka wejściowego. System wykorzystuje łańcuch modeli AI, gdzie każdy specjalizuje się w konkretnym zadaniu.

### Przepływ Pracy (Pipeline)
1. **Analiza Stylu** → Model wizyjny (Janus Pro/GPT-4) analizuje styl artystyczny obrazka wejściowego
2. **Tworzenie Promptu** → GPT-4 przekształca opis w optymalny prompt dla generatora
3. **Generowanie Obrazka** → Stable Diffusion/Flux tworzy nowy obrazek w tym samym stylu
4. **Animacja** → Model video (Veo 2/SVD) animuje wygenerowany obrazek

### Architektura
```
Image-to-Video/
├── main.py              # Główny orchestrator procesu
├── config.py            # Centralna konfiguracja (API, prompty, parametry)
├── requirements.txt     # Zależności projektu
├── modules/             # Moduły funkcjonalne
│   ├── __init__.py
│   ├── image_describer.py    # Analiza stylu obrazka
│   ├── prompt_creator.py     # Tworzenie promptów
│   ├── image_generator.py    # Generowanie obrazków
│   └── video_animator.py     # Animacja video
├── input/               # Obrazki wejściowe
├── image/               # Wygenerowane obrazki
├── video/               # Wygenerowane animacje
└── logs/                # Logi aplikacji
```

## Parametry Techniczne

### Temperatury Modeli
- **Opis obrazka**: temp=0.1 (dokładność, precyzja)
- **Tworzenie promptu**: temp=0.3 (balans kreatywności i kontroli)
- **Generowanie obrazka**: temp=0.8 (wysoka kreatywność)
- **Animacja video**: temp=0.8 (płynność, naturalność ruchu)

### Wymagane API
1. **OpenAI** - GPT-4 do analizy i promptów
2. **Replicate** - Stable Diffusion i modele video
3. **LMStudio** - lokalny Janus Pro (opcjonalnie)

## Instrukcja Implementacji dla Cursor Agent

### KROK 1: Inicjalizacja Projektu
```
Stwórz nowy folder "Image-to-Video" poza strukturą kursu.
Utwórz podstawową strukturę folderów:
- modules/
- input/
- image/
- video/
- logs/

Dodaj plik .gitignore z:
- *.pyc
- __pycache__/
- .env
- logs/*
- image/*
- video/*
```

### KROK 2: Plik requirements.txt
```
Utwórz plik requirements.txt z zależnościami:
- openai
- replicate
- requests
- python-dotenv
- pillow
```

### KROK 3: Główny plik config.py
```python
Stwórz config.py w głównym folderze projektu.
Plik powinien zawierać:

1. Import os i dotenv
2. Ładowanie zmiennych środowiskowych z .env
3. Słownik IMAGE_DESCRIBER_CONFIG z:
   - model_type, model_name
   - temperature=0.1, top_p=0.9
   - system_prompt dla analizy obrazków
4. Słownik PROMPT_CREATOR_CONFIG z:
   - model_type="openai", model_name="gpt-4o-mini"
   - temperature=0.3, top_p=0.9
   - system_prompt dla tworzenia promptów
5. Słownik IMAGE_GENERATOR_CONFIG z:
   - model dla Replicate
   - temperature=0.8
   - parametry obrazka (width, height)
6. Słownik VIDEO_ANIMATOR_CONFIG z:
   - model dla animacji
   - fps, duration
   - system_prompt dla animacji
7. Definicje ścieżek (BASE_DIR, INPUT_DIR, etc.)
8. Kod tworzący foldery jeśli nie istnieją
```

### KROK 4: Moduł modules/__init__.py
```
Utwórz pusty plik __init__.py w folderze modules/
```

### KROK 5: Moduł modules/image_describer.py
```python
Stwórz klasę ImageDescriber z:
1. __init__ który ładuje config
2. Metodę describe(image_path) która:
   - Używa OpenAI API z vision
   - Przekazuje system_prompt z configa
   - Ustawia temperature i top_p
   - Zwraca szczegółowy opis obrazka
```

### KROK 6: Moduł modules/prompt_creator.py
```python
Stwórz klasę PromptCreator z:
1. __init__ który ładuje config
2. Metodę create_prompt(description) która:
   - Przyjmuje opis z poprzedniego kroku
   - Używa GPT-4 do stworzenia promptu
   - Dodaje prefix z configa
   - Zwraca gotowy prompt dla SD
```

### KROK 7: Moduł modules/image_generator.py
```python
Stwórz klasę ImageGenerator z:
1. __init__ który ładuje config
2. Metodę generate(prompt, output_name) która:
   - Używa Replicate API
   - Przekazuje prompt i parametry z configa
   - Pobiera wygenerowany obrazek
   - Zapisuje go w folderze image/
   - Zwraca ścieżkę do pliku
```

### KROK 8: Moduł modules/video_animator.py (opcjonalny na start)
```python
Stwórz klasę VideoAnimator z:
1. __init__ który ładuje config
2. Metodę animate(image_path, output_name) która:
   - Używa modelu video z Replicate
   - Animuje obrazek zgodnie z promptem
   - Zapisuje video w folderze video/
   - Zwraca ścieżkę do pliku
```

### KROK 9: Główny plik main.py
```python
Stwórz orchestrator który:
1. Importuje wszystkie moduły
2. Definiuje funkcję process_image(input_path):
   - Tworzy instancje wszystkich klas
   - Wykonuje pipeline krok po kroku
   - Loguje postępy
   - Obsługuje błędy
3. W __main__ sprawdza czy istnieje plik testowy
4. Uruchamia proces dla pliku test.jpg
```

### KROK 10: Plik .env
```
Utwórz plik .env z kluczami API:
OPENAI_API_KEY=sk-...
REPLICATE_API_KEY=r8_...
```

## Uruchomienie Prototypu

1. **Instalacja zależności**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Przygotowanie**:
   - Umieść obrazek testowy w `input/test.jpg`
   - Uzupełnij klucze API w `.env`

3. **Uruchomienie**:
   ```bash
   python main.py
   ```

## Możliwe Rozszerzenia

1. **Interfejs Web** - Dodanie Streamlit/Gradio
2. **Batch Processing** - Przetwarzanie wielu obrazków
3. **Style Mixing** - Łączenie stylów z kilku obrazków
4. **Parametryzacja** - Kontrola siły stylu, typu animacji
5. **Historia** - Zapisywanie wszystkich generacji z metadanymi

## Debugowanie

### Częste problemy:
1. **Brak klucza API** → Sprawdź plik .env
2. **Błąd modelu** → Sprawdź limity API
3. **Brak obrazka** → Upewnij się że ścieżka jest poprawna
4. **Za mały budżet** → Użyj mniejszych obrazków na start

### Logi:
- Wszystkie operacje powinny być logowane do `logs/`
- Każdy moduł ma własny logger
- Poziomy: INFO dla normalnych operacji, ERROR dla błędów

## Wskazówki dla Cursor Agent

1. **Twórz pliki po kolei** zgodnie z krokami
2. **Testuj każdy moduł osobno** przed integracją
3. **Używaj type hints** dla czytelności
4. **Dodawaj docstringi** do funkcji
5. **Obsługuj wyjątki** gracefully
6. **Loguj wszystkie kroki** dla debugowania


## System Prompts

### 1. System Prompt dla LLaVA-13B (Analiza Stylu)

```
A chat between a curious human and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the human's questions.

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

ASSISTANT:
```

### 2. System Prompt dla GPT-4 (Tworzenie Promptu)

```
You are a master prompt engineer specializing in translating visual style descriptions into precise, effective prompts for AI image generation models (Stable Diffusion, DALL-E, Flux).

Your task is to convert a style description into an optimized prompt that will recreate the described aesthetic.

RULES:
1. Focus on style keywords, not content
2. Use industry-standard terminology for art techniques
3. Include quality modifiers (masterpiece, high quality, detailed)
4. Add relevant style tags (architectural visualization, technical drawing, concept art)
5. Keep prompt concise but comprehensive (max 75 words)
6. Structure: [Style/Medium] + [Color descriptors] + [Line/Edge qualities] + [Mood/Atmosphere] + [Technical specifications]

EXAMPLE OUTPUT FORMAT:
"architectural diagram, clean vector illustration, muted pastel color palette, thin precise linework, minimal shadows, technical drawing style, isometric view, soft gradients, professional visualization, high detail, 4K quality"

Transform the provided style description into a generation-ready prompt.
```

### 3. System Prompt dla Image Generator (Stable Diffusion/Flux)

```
Create a high-quality architectural visualization following this specific style guide. 

STYLE REQUIREMENTS:
- Maintain consistent visual language throughout
- Emphasize clean, professional presentation
- Focus on clarity and readability
- Use the specified color palette and line weights

TECHNICAL SPECIFICATIONS:
- Resolution: 1024x1024 or as specified
- Style consistency: High
- Detail level: Professional quality
- Avoid: Text, watermarks, signatures, artifacts

Follow the provided prompt precisely while ensuring professional architectural visualization standards.
```

### 4. System Prompt dla Video Animator (Opcjonalny)

```
You are creating a subtle, professional animation of an architectural visualization.

ANIMATION GUIDELINES:
1. CAMERA MOVEMENT: Slow, smooth drone-like movements or gentle pans
2. ENVIRONMENTAL EFFECTS: Subtle light changes suggesting time progression
3. DETAIL REVEALS: Gradual focus shifts highlighting different architectural elements
4. ATMOSPHERE: Maintain the original style's mood throughout the animation

TECHNICAL REQUIREMENTS:
- Duration: 4-6 seconds
- FPS: 24-30
- Movement speed: Slow and cinematic
- Transitions: Smooth and professional

Create an elegant, subtle animation that enhances the architectural visualization without overwhelming it.
```

## Przykład Użycia System Promptów

### Input: Diagram architektoniczny w stylu minimalistycznym

**LLaVA Output (przykład):**
"The image exhibits a minimalist architectural style with a restricted color palette of cool grays (#E8E8E8, #CCCCCC) and accent blue (#4A90E2). Line work consists of thin, precise strokes (1-2px weight) with sharp, clean edges. The rendering style is digital vector illustration with flat colors and subtle gradients. No textures or grain present. Composition follows strict geometric principles with ample white space. The overall mood is professional, clean, and modern."

**GPT-4 Prompt Output (przykład):**
"minimalist architectural diagram, cool gray and accent blue color scheme, thin precise vector lines, flat design with subtle gradients, clean geometric composition, professional technical illustration, white background, sharp edges, modern visualization style, high detail, 4K"

## Wskazówki Implementacyjne

### Dla modułu image_describer.py:

```python
# Użyj tego system promptu dla LLaVA
LLAVA_STYLE_ANALYSIS_PROMPT = """A chat between a curious human and an artificial intelligence assistant...[pełny prompt z góry]"""

# W metodzie describe():
def describe(self, image_path):
    # Formatuj prompt dla LLaVA
    formatted_prompt = self.LLAVA_STYLE_ANALYSIS_PROMPT.replace("<image>", "")
    # Reszta implementacji...
```

### Optymalizacja dla Diagramów Architektonicznych:

1. **Preprocessing obrazka**: Przed wysłaniem do LLaVA, rozważ zwiększenie kontrastu dla lepszej analizy linii
2. **Słowa kluczowe**: Dodaj do configa listę architectural style keywords
3. **Walidacja**: Sprawdź czy opis zawiera kluczowe elementy (kolory, linie, styl)

## Aktualizacja config.py z System Promptami

```python
# Zaktualizowana konfiguracja IMAGE_DESCRIBER_CONFIG
IMAGE_DESCRIBER_CONFIG = {
    "model_type": "custom",
    "model_name": "llava-v1.5-13b",
    "custom_endpoint": LMSTUDIO_ENDPOINT,
    "custom_model_name": "llava-v1.5-13b",
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

ASSISTANT:"""
}

# Zaktualizowana konfiguracja PROMPT_CREATOR_CONFIG
PROMPT_CREATOR_CONFIG = {
    "model_type": "openai",
    "model_name": "gpt-4o-mini",
    "temperature": 0.3,
    "top_p": 0.9,
    "system_prompt": """You are a master prompt engineer specializing in translating visual style descriptions into precise, effective prompts for AI image generation models (Stable Diffusion, DALL-E, Flux).

Your task is to convert a style description into an optimized prompt that will recreate the described aesthetic.

RULES:
1. Focus on style keywords, not content
2. Use industry-standard terminology for art techniques
3. Include quality modifiers (masterpiece, high quality, detailed)
4. Add relevant style tags (architectural visualization, technical drawing, concept art)
5. Keep prompt concise but comprehensive (max 75 words)
6. Structure: [Style/Medium] + [Color descriptors] + [Line/Edge qualities] + [Mood/Atmosphere] + [Technical specifications]

EXAMPLE OUTPUT FORMAT:
"architectural diagram, clean vector illustration, muted pastel color palette, thin precise linework, minimal shadows, technical drawing style, isometric view, soft gradients, professional visualization, high detail, 4K quality"

Transform the provided style description into a generation-ready prompt."""
}
```