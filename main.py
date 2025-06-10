import os
import logging
from dotenv import load_dotenv
from config import INPUT_DIR
from modules.image_describer import ImageDescriber
from modules.prompt_creator import PromptCreator
from modules.image_generator import ImageGenerator
from modules.video_animator import VideoAnimator
from modules.json_logger import JSONLogger
from modules.spinner import Spinner

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)

# Load environment variables from .env file
load_dotenv()

def process_image(input_path: str, create_video: bool = False):
    """
    Orchestrates the entire image-to-video pipeline for a single input image.

    Args:
        input_path: The full path to the input image.
        create_video: If True, the process will continue to generate a video.
    """
    if not os.path.exists(input_path):
        logging.error(f"Input file not found at: {input_path}")
        return

    # Inicjalizuj JSON logger
    json_logger = JSONLogger()
    input_filename = os.path.basename(input_path)
    json_logger.start_process(input_filename)

    # Get API key from environment
    replicate_api_key = os.getenv("REPLICATE_API_KEY")
    if not replicate_api_key:
        logging.error("REPLICATE_API_KEY environment variable not found.")
        json_logger.finish_process(success=False, error_message="REPLICATE_API_KEY not found")
        return

    try:
        # --- Step 1: Analyze Image Style ---
        with Spinner("Step 1: Analyzing image style..."):
            describer = ImageDescriber()
            style_description = describer.describe(input_path)
        logging.info("Step 1: Image style analysis complete.")
        logging.info(f"Style description received:\n---\n{style_description}\n---")
        
        # Zapisz opis stylu do JSON
        json_logger.log_style_description(style_description)

        # --- Step 2: Create Generation Prompt ---
        # The new prompt_creator handles the interaction, so we call it directly.
        prompt_creator = PromptCreator()
        generation_prompt = prompt_creator.create_prompt(style_description)
        
        logging.info(f"Step 2: Generation prompt accepted: '{generation_prompt}'")
        
        # Zapisz prompt do JSON
        json_logger.log_generation_prompt(generation_prompt)

        # --- Tweak Loop: Generate Image and allow for modifications ---
        while True:
            # --- Step 3: Generate New Image ---
            with Spinner("Step 3: Generating new image..."):
                image_generator = ImageGenerator(api_key=replicate_api_key)
                output_filename_base = os.path.splitext(os.path.basename(input_path))[0]
                generated_image_path = image_generator.generate(
                    prompt=generation_prompt,
                    output_name=f"{output_filename_base}_generated",
                    input_image_path=input_path
                )
            logging.info(f"Step 3: New image saved at: {generated_image_path}")
            
            json_logger.log_output_image(generated_image_path)

            # --- Ask user to tweak ---
            print("\n--- Image Generated ---")
            
            while True:
                tweak_choice = input(f"Image saved to {generated_image_path}\nWhat would you like to do? [1] Continue, [2] Tweak prompt and regenerate: ").strip()
                if tweak_choice in ['1', '2']:
                    break
                print("Invalid choice. Please enter 1 or 2.")
            
            if tweak_choice == '1':
                break 
            
            print("\n--- Tweak Prompt ---")
            print("Current prompt:")
            print(f"-> {generation_prompt}")
            
            new_prompt = input("Enter your new prompt: ").strip()
            
            if new_prompt:
                generation_prompt = new_prompt
                json_logger.log_generation_prompt(generation_prompt)
                print("Prompt updated. Regenerating image...")
            else:
                print("No changes entered. Continuing with the current image.")
                break

        # --- Step 4: Animate Video (Optional) ---
        if create_video:
            # --- Get user prompt for video ---
            print("\n--- Video Generation ---")
            video_prompt = input("Please enter the prompt for video generation: ")
            if not video_prompt:
                logging.warning("Video prompt is empty, using the auto-generated image prompt.")
                video_prompt = generation_prompt
            json_logger.log_video_prompt(video_prompt) # Log the chosen prompt

            with Spinner("Step 4: Animating video... (this may take a moment)"):
                video_animator = VideoAnimator(api_key=replicate_api_key)
                generated_video_path = video_animator.animate(generated_image_path, f"{output_filename_base}_animated", video_prompt)
            logging.info(f"Step 4: New video saved at: {generated_video_path}")
            
            # Zapisz ścieżkę wideo do JSON
            json_logger.log_output_video(generated_video_path)

        # Zakończ proces jako udany
        json_logger.finish_process(success=True)
        logging.info("Process completed successfully!")

    except Exception as e:
        logging.error(f"An error occurred during the process: {e}", exc_info=True)
        # Zakończ proces jako nieudany
        json_logger.finish_process(success=False)

if __name__ == "__main__":
    # --- Run the process for a test image ---
    # Make sure to place a 'test.jpg' file in the 'input' folder
    test_image_name = "test.jpg"
    test_image_path = os.path.join(INPUT_DIR, test_image_name)

    if not os.path.exists(test_image_path):
        logging.error(f"Test file '{test_image_name}' not found in '{INPUT_DIR}'. Please place it there to run the script.")
    else:
        while True:
            choice = input("What would you like to do?\n[1] Generate Image only\n[2] Generate Image and Video\nEnter choice (1 or 2): ")
            if choice in ['1', '2']:
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")

        create_video_choice = (choice == '2')
        
        logging.info(f"--- Starting Image-to-Video Process for '{test_image_name}' ---")
        process_image(test_image_path, create_video=create_video_choice)
        logging.info("--- Process Finished ---") 