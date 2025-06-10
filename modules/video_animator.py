import os
import replicate
import requests
from config import VIDEO_ANIMATOR_CONFIG, VIDEO_DIR
import logging

class VideoAnimator:
    """
    Animates an image using a video model on Replicate.
    """
    def __init__(self, api_key: str):
        """
        Initializes the VideoAnimator with configuration from config.py.
        """
        if not api_key:
            raise ValueError("Replicate API key is required.")
        self.config = VIDEO_ANIMATOR_CONFIG
        self.client = replicate.Client(api_token=api_key)
        os.makedirs(VIDEO_DIR, exist_ok=True)
        logging.info("VideoAnimator initialized.")

    def animate(self, image_path: str, output_name: str, prompt: str) -> str:
        """
        Animates an image using the configured Replicate model.

        Args:
            image_path: The path to the input image to animate.
            output_name: The base name for the output video file (without extension).
            prompt: The text prompt to guide the video generation.

        Returns:
            The full path to the generated video file.
        """
        logging.info(f"Starting animation for '{image_path}' with prompt: '{prompt}'")

        try:
            with open(image_path, "rb") as image_file:
                # Run the model on Replicate
                output = self.client.run(
                    self.config['model'],
                    input={
                        "prompt": prompt,
                        "start_image": image_file,
                        "duration": self.config.get('duration', 5),
                        "cfg_scale": self.config.get('cfg_scale', 0.5),
                        "negative_prompt": self.config.get('negative_prompt', "")
                    }
                )
            
            video_url = output
            if not video_url:
                raise Exception("Replicate API did not return a video URL.")

            logging.info(f"Animation generated, video URL: {video_url}")

            # Download the video
            response = requests.get(video_url, stream=True)
            response.raise_for_status()

            video_filename = f"{output_name}.mp4"
            video_path = os.path.join(VIDEO_DIR, video_filename)

            with open(video_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            logging.info(f"Video successfully downloaded and saved to '{video_path}'")
            return video_path

        except replicate.exceptions.ReplicateError as e:
            logging.error(f"Replicate API error during animation: {e}")
            raise
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to download the animated video: {e}")
            raise
        except Exception as e:
            logging.error(f"An unexpected error occurred during animation: {e}")
            raise 