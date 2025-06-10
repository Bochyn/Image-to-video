import openai
from config import PROMPT_ENHANCER_CONFIG

class PromptEnhancer:
    """
    Enhances a given prompt based on user modification requests.
    """
    def __init__(self):
        """
        Initializes the PromptEnhancer with configuration from config.py.
        """
        self.config = PROMPT_ENHANCER_CONFIG
        self.client = openai.OpenAI()

    def enhance_prompt(self, original_prompt: str, modification_request: str) -> str:
        """
        Generates a new, improved prompt by integrating the user's modification
        request into the original prompt.

        Args:
            original_prompt: The prompt to be enhanced.
            modification_request: The user's instructions for changes.

        Returns:
            A new, enhanced prompt.
        """
        print("Enhancing prompt with your modifications...")
        
        user_content = f"The previous prompt was: '{original_prompt}'. The user wants to modify it with these instructions: '{modification_request}'."

        response = self.client.chat.completions.create(
            model=self.config["model_name"],
            messages=[
                {"role": "system", "content": self.config["system_prompt"]},
                {"role": "user", "content": user_content}
            ],
            temperature=self.config["temperature"],
            top_p=self.config["top_p"],
            max_tokens=self.config["max_tokens"]
        )
        
        enhanced_prompt = response.choices[0].message.content.strip()
        return enhanced_prompt 