#!/usr/bin/env python3
"""
FamilyValueTone Utility
Provides system prompt segments and logic to ensure LLM responses align with
the family's communication values: Professional, Warm, Concise, and Helpful.
"""

from typing import Optional

class FamilyValueTone:
    """
    Utility to manage and apply the family's preferred communication tone.
    References: docs/knowledge_base/family-values.md
    """

    SYSTEM_PROMPT_FRAGMENT = """
    ## Communication Style Guidelines (Ralph's Persona)
    - **Tone**: Professional yet warm. Be efficient and polite.
    - **Identity**: You are Ralph, the Home Admin Agent.
    - **Conciseness**: Get to the point quickly. Avoid unnecessary chatter.
    - **Clarity**: Use simple, jargon-free language.
    - **Privacy**: Be extremely careful with personal data; do not suggest sharing it externally.
    - **Transparency**: If you make a mistake or a tool fails, acknowledge it clearly.
    """

    @classmethod
    def get_system_prompt(cls, additional_context: Optional[str] = None) -> str:
        """Returns the base system prompt for Ralph's tone."""
        prompt = cls.SYSTEM_PROMPT_FRAGMENT
        if additional_context:
            prompt += f"\n- **Context**: {additional_context}\n"
        return prompt

    @classmethod
    def apply_tone_post_processing(cls, response: str) -> str:
        """
        Optional post-processing to ensure basic quality standards.
        In a real scenario, this might involve checking for banned words
        or ensuring brevity.
        """
        # Basic example: ensure the response starts with a polite opening
        # or doesn't end with excessive filler.
        processed = response.strip()

        # Avoid common LLM filler patterns
        fillers = ["As an AI language model,", "I'm sorry, but as an AI", "Certainly!"]
        for filler in fillers:
            if processed.startswith(filler):
                processed = processed[len(filler):].strip()
                if processed.startswith(","):
                    processed = processed[1:].strip()

        return processed

if __name__ == "__main__":
    # Quick test
    print("--- Ralph's System Prompt Fragment ---")
    print(FamilyValueTone.get_system_prompt())

    test_response = "Certainly! I have finished the task you requested. Is there anything else I can do for you?"
    print("\n--- Before Post-processing ---")
    print(test_response)
    print("\n--- After Post-processing ---")
    print(FamilyValueTone.apply_tone_post_processing(test_response))
