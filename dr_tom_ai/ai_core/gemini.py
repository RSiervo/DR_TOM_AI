import os, mimetypes
import google.generativeai as genai

API_KEY = os.getenv("GOOGLE_API_KEY")  # set this in .env or environment
if not API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not set. Put it in .env or your environment.")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

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

def analyze(symptoms_text: str = "", image_path: str | None = None) -> str:
    prompt = PROMPT_TEMPLATE.format(symptoms=symptoms_text.strip() or "None provided")

    # Build parts for multimodal
    parts = [prompt]
    if image_path:
        mime, _ = mimetypes.guess_type(image_path)
        mime = mime or "image/jpeg"
        with open(image_path, "rb") as f:
            parts.append({"mime_type": mime, "data": f.read()})

    try:
        resp = model.generate_content(parts if len(parts) > 1 else prompt)
        return (resp.text or "").strip()
    except Exception as e:
        return f"Sorry, I couldn’t analyze this right now. Error: {e}"
