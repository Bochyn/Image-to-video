import openai
from config import PROMPT_CREATOR_CONFIG
from .prompt_enhancer import PromptEnhancer

class PromptCreator:
    """
    Creates an optimized prompt for an image generation model based on a style description.
    """
    def __init__(self):
        """
        Initializes the PromptCreator with configuration from config.py.
        """
        self.config = PROMPT_CREATOR_CONFIG
        self.client = openai.OpenAI()
        self.enhancer = PromptEnhancer()

    def create_prompt(self, description: str) -> str:
        """
        Generates a prompt and allows the user to iteratively refine it.

        Args:
            description: A detailed description of the artistic style.

        Returns:
            A string containing the user-approved generated prompt.
        """
        print("\n--- Prompt Creation ---")
        print("Generating initial prompt from style description...")
        
        response = self.client.chat.completions.create(
            model=self.config["model_name"],
            messages=[
                {"role": "system", "content": self.config["system_prompt"]},
                {"role": "user", "content": description}
            ],
            temperature=self.config["temperature"],
            top_p=self.config["top_p"],
            max_tokens=150
        )
        generated_prompt = response.choices[0].message.content.strip()

        while True:
            print("\n--- Generated Prompt ---")
            print(f"'{generated_prompt}'")
            print("------------------------")

            while True:
                choice = input("\nChoose an action: [1] Accept, [2] Modify: ").strip()
                if choice in ['1', '2']:
                    break
                print("Invalid choice. Please enter 1 or 2.")

            if choice == '1':
                print("Prompt accepted.")
                return generated_prompt
            
            modification_request = input("Describe the changes you want: ")
            if not modification_request.strip():
                print("No modification request. Accepting the current prompt.")
                return generated_prompt

            generated_prompt = self.enhancer.enhance_prompt(generated_prompt, modification_request) 