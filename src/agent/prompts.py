from pathlib import Path

_PROMPTS_DIR = Path(__file__).resolve().parent.parent.parent / "config" / "prompts"

CLASSIFICATION_PROMPT = (_PROMPTS_DIR / "classification.txt").read_text()
GENERATION_PROMPT = (_PROMPTS_DIR / "generation.txt").read_text()
