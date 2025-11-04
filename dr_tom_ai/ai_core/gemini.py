import os
import mimetypes
import google.generativeai as genai

# --- Setup ---
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not set. Put it in .env or your environment.")

genai.configure(api_key=API_KEY)

# Models
TEXT_MODEL = genai.GenerativeModel("models/gemini-2.5-flash")
IMAGE_MODEL_NAME = "models/imagen-3.0"  # ✅ true image generator

PROMPT_TEMPLATE = """You are Dr. Tom AI, a helpful medical assistant.
User provided symptoms: {symptoms}
If an image is provided, examine visible features.
Respond with:
1) Possible conditions (top 3–5) with brief rationale
2) Suggested self-care
3) Red flags — when to seek urgent care
4) Suggested next steps (tests, specialist)
Keep it concise, layperson-friendly, and include a clear disclaimer that this is not a medical diagnosis.
"""

# --- Text + image analysis ---
def analyze(symptoms_text: str = "", image_path: str | None = None) -> str:
    prompt = PROMPT_TEMPLATE.format(symptoms=symptoms_text.strip() or "None provided")
    contents = [{"role": "user", "parts": [{"text": prompt}]}]

    if image_path:
        mime, _ = mimetypes.guess_type(image_path)
        mime = mime or "image/jpeg"
        with open(image_path, "rb") as f:
            contents[0]["parts"].append({
                "inline_data": {"mime_type": mime, "data": f.read()}
            })

    try:
        response = TEXT_MODEL.generate_content(contents)
        return response.text.strip() if response.text else "No response from model."
    except Exception as e:
        return f"Sorry, I couldn’t analyze this right now. Error: {e}"

# --- Image generation ---
def generate_medical_image(prompt: str, output_path: str = "generated_image.png") -> str:
    """
    Generate an AI medical illustration using Imagen 3.0
    Example: generate_medical_image("human skin with red itchy rash")
    """
    try:
        result = genai.generate_image(model=IMAGE_MODEL_NAME, prompt=prompt)
        image_data = result.images[0]._image_bytes
        with open(output_path, "wb") as f:
            f.write(image_data)
        return output_path
    except Exception as e:
        return f"Error generating image: {e}"
