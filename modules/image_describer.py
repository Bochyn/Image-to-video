import base64
import openai
from config import IMAGE_DESCRIBER_CONFIG

class ImageDescriber:
    """
    Analyzes the artistic style of an image using an AI vision model.
    """
    def __init__(self):
        """
        Initializes the ImageDescriber with configuration from config.py.
        """
        self.config = IMAGE_DESCRIBER_CONFIG
        
        if self.config["model_type"] == "local":
            self.client = openai.OpenAI(
                base_url=self.config["local_server_url"],
                api_key="not-needed" # API key is not needed for local server
            )
        else:
            # Assumes OPENAI_API_KEY is set in the environment for the default client
            self.client = openai.OpenAI()

    def _encode_image(self, image_path: str) -> str:
        """
        Encodes the image at the given path to a base64 string.

        Args:
            image_path: The path to the image file.

        Returns:
            The base64 encoded image string.
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def describe(self, image_path: str) -> str:
        """
        Analyzes the given image and returns a description of its artistic style.

        Args:
            image_path: The path to the image to be analyzed.

        Returns:
            A string containing the detailed description of the image's style.
        """
        base64_image = self._encode_image(image_path)

        response = self.client.chat.completions.create(
            model=self.config["model_name"],
            messages=[
                {
                    "role": "user",
                    "content": [
                        {   "type": "text",
                            "text": self.config["system_prompt"]
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            temperature=self.config["temperature"],
            top_p=self.config["top_p"],
            max_tokens=500
        )

        return response.choices[0].message.content 