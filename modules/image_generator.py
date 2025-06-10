import os
import requests
import replicate
from config import IMAGE_GENERATOR_CONFIG, IMAGE_DIR
import logging

class ImageGenerator:
    """
    Generates an image using the Replicate API based on a given prompt.
    """
    def __init__(self, api_key: str):
        """
        Initializes the ImageGenerator with configuration from config.py.
        """
        if not api_key:
            raise ValueError("Replicate API key is required.")
        self.config = IMAGE_GENERATOR_CONFIG
        self.client = replicate.Client(api_token=api_key)

    def generate(self, prompt: str, output_name: str, input_image_path: str = None) -> str:
        """
        Generates an image and saves it to the image directory.

        Args:
            prompt: The prompt to use for image generation.
            output_name: The filename for the output image (without extension).
            input_image_path: The path to the input image file (optional, currently unused).

        Returns:
            The path to the generated image file.
        """
        logging.info(f"Generating image with prompt: '{prompt}'")

        try:
            # Prepare input parameters for the Replicate model
            input_params = {
                "prompt": prompt,
                "seed": self.config.get('seed'),
                "aspect_ratio": self.config.get('aspect_ratio'),
                "output_format": self.config.get('output_format'),
                "safety_tolerance": self.config.get('safety_tolerance'),
            }

            # For image-to-image models, open the input image and pass it
            if input_image_path:
                logging.info(f"Using input image: {input_image_path}")
                # The replicate library expects a file-like object, so we open it in binary read mode
                input_image_file = open(input_image_path, "rb")
                input_params["input_image"] = input_image_file
            else:
                # Handle case where no input image is provided for an img2img model
                # Depending on the model, this might be an error or fallback to text-to-image
                logging.warning("No input image provided for an image-to-image generation process.")


            # Run the model on Replicate
            try:
                output = self.client.run(
                    self.config["model"],
                    input=input_params
                )
            finally:
                # Ensure the file is closed after the API call
                if 'input_image' in input_params and input_params['input_image']:
                    input_params['input_image'].close()
            
            if not output:
                raise Exception("Image generation failed. No output from Replicate API.")

            logging.info("Image generation complete. Saving file...")

            # The output from replicate.run is a FileOutput object.
            # Use its .read() method to get the binary content directly.
            image_data = output.read()
            
            # Save the image
            image_filename = f"{output_name}.{self.config.get('output_format', 'png')}"
            image_path = os.path.join(IMAGE_DIR, image_filename)

            with open(image_path, 'wb') as f:
                f.write(image_data)
            
            logging.info(f"Image successfully downloaded and saved to '{image_path}'")
            return image_path

        except replicate.exceptions.ReplicateError as e:
            logging.error(f"Replicate API error during image generation: {e}")
            raise
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to download the generated image: {e}")
            raise
        except Exception as e:
            logging.error(f"An unexpected error occurred during image generation: {e}")
            raise 