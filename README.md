# Image-to-Video

An application that analyzes the artistic style of an architectural visualization image, then uses that analysis to generate a new image and an optional short video animation in a similar aesthetic.

## How It Works

The process is orchestrated by the `main.py` script. It takes an input image, analyzes its visual characteristics, and enters a loop where the user can generate images and refine the AI-generated prompts until satisfied.

```mermaid
graph TD;
    %% === STYLES ===
    classDef setup fill:#E9E6E9,stroke:#686764,stroke-width:2px,color:#333;
    classDef analysis fill:#DDD7DA,stroke:#686764,stroke-width:2px,color:#333;
    classDef generation fill:#D0C9CA,stroke:#686764,stroke-width:2px,color:#333;
    classDef io fill:#B6B0B0,stroke:#686764,stroke-width:2px,color:#333;
    classDef decision fill:#EFEDF0,stroke:#82807D,stroke-width:2px,color:#333,font-weight:bold;
    classDef endNode fill:#F5F4F6,stroke:#82807D,stroke-width:1px,color:#333;

    %% === SETUP ===
    A[Place image in input folder]:::setup

    %% === ANALYSIS & PROMPT ===
    B[Run main.py]:::io
    C[Analyze Image Style with GPT-4o-mini]:::analysis
    D[Create Initial Prompt with GPT-4o-mini]:::analysis

    %% === GENERATION LOOP ===
    E[Generate Image via Replicate API]:::generation
    F[Save Image to image folder]:::io
    G{User Review}:::decision
    I[User Modifies Prompt]:::setup

    %% === VIDEO GENERATION ===
    H{Generate Video?}:::decision
    J[Animate Video via Replicate API]:::generation
    K[Save Video to video folder]:::io

    %% === END ===
    L((Process End)):::endNode

    %% === CONNECTIONS ===
    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    G -->|Accept & Continue| H
    G -->|Tweak & Regenerate| I
    I --> E
    H -->|Yes| J
    H -->|No| L
    J --> K
    K --> L
```

## Features

- **Architectural Style Analysis**: Automatically identifies key visual elements like rendering type, perspective, materials, lighting, and color palette using an AI model.
- **Prompt Generation**: Creates a concise and effective prompt for AI image generators based on the style analysis.
- **Interactive Refinement Loop**: After an image is generated, you can tweak the prompt and regenerate the image until you are satisfied with the result.
- **Image Generation**: Uses Replicate to generate a new, high-quality image based on the prompt.
- **Video Animation**: Optionally creates a short video animation from the generated image.
- **Detailed Logging**: Saves a detailed JSON log for each run, including the style description, all generated prompts, and paths to the output files.

## Project Structure

- `input/`: Place your input image here. The script looks for `test.jpg` by default.
- `image/`: Stores the images generated by the AI.
- `video/`: Stores the video animations.
- `logs/`: Contains `app.log` for general logging and detailed `*_log.json` files for each process.
- `modules/`: Contains the Python source code for each step of the pipeline.
- `main.py`: The main script to run the application.
- `config.py`: Configuration file for models, prompts, and parameters.
- `requirements.txt`: A list of the Python packages required to run the project.
- `.env`: A file (that you create) to store your API keys securely.
- `envexample.md`: An example file for your `.env` configuration.

## Requirements

### System Requirements
- Python 3.8+
- Git

### API Keys Required
- **OpenAI API Key**: Required for GPT-4o-mini model used for style analysis and prompt generation
- **Replicate API Key**: Required for image generation and video animation models

### Python Dependencies

The project requires the following Python packages (automatically installed via `requirements.txt`):

- **openai**: OpenAI API client for GPT-4o-mini interactions
- **replicate**: Replicate API client for AI image and video generation
- **requests**: HTTP library for API communications
- **python-dotenv**: Environment variable management for secure API key storage
- **pillow**: Python Imaging Library for image processing operations

## Installation and Configuration

### Prerequisites
- Python 3.8+
- Git

### 1. Clone the Repository

```bash
git clone <repository-address>
cd Image-to-Video
```

### 2. Create a Virtual Environment and Install Dependencies

Using a virtual environment is highly recommended.

```bash
# Create a virtual environment
python -m venv venv

# Activate the environment
# On Windows:
venv\Scripts\activate
# On macOS / Linux:
source venv/bin/activate

# Install the required packages
pip install -r requirements.txt
```

### 3. Configure API Keys

The application requires API keys for OpenAI and Replicate.

1.  Create a new file named `.env` in the root directory of the project.
2.  Copy the contents from `envexample.md` into your new `.env` file.
3.  Add your secret API keys to the `.env` file:

    ```.env
    # This file stores your secret keys.
    # Rename envexample.md to .env and fill in your keys.

    # OpenAI API Key for GPT-4 (style analysis and prompt creation)
    OPENAI_API_KEY="sk-..."

    # Replicate API Key for image and video generation
    REPLICATE_API_KEY="r8_..."
    ```

## Usage

1.  **Place your image** in the `input` folder. By default, the script uses `test.jpg`, but you can change the filename in `main.py`.

2.  **Run the main script** from your terminal:

    ```bash
    python main.py
    ```

3.  **Choose an option** when prompted:
    - Enter `1` to generate an image only.
    - Enter `2` to generate an image and then a video.

    ```
    What would you like to do?
    [1] Generate Image only
    [2] Generate Image and Video
    Enter choice (1 or 2):
    ```
4. **Tweak the prompt** if needed. After the first image is generated, you will be asked if you want to continue or modify the prompt.
    ```
    Image saved to image/test_generated_1.png
    What would you like to do? [1] Continue, [2] Tweak prompt and regenerate:
    ```
    If you choose to tweak, you can enter a new prompt to regenerate the image.

The final output files will be saved in the `image` and `video` folders.

## Advanced Configuration

The `config.py` file allows you to customize the application's behavior. You can modify:
- **AI Models**: Swap out the models used for image description, prompt creation, image generation, and video animation. The configuration supports both OpenAI-compatible APIs and Replicate models.
- **Model Parameters**: Adjust parameters like `temperature`, `top_p`, `seed`, video duration, and more to influence the creative output.
- **System Prompts**: Edit the master instructions given to the language models to change how they analyze styles or create prompts.

## Logging

The application generates two types of logs in the `logs` directory:
- `app.log`: A general log file that records the main events, warnings, and errors of the application's execution.
- `*_log.json`: A detailed JSON file is created for each run, containing the full style analysis, the initial and any tweaked prompts, and the final paths to the generated image and video. This is useful for debugging and tracking results.
