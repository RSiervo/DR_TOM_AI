import google.generativeai as genai

genai.configure(api_key="YAIzaSyC8ADAX3RVMh1KmW7XnYmx-LK92rfjhpkA")

print("Available Gemini models that support content generation:\n")

for m in genai.list_models():
    if hasattr(m, "supported_generation_methods") and "generateContent" in m.supported_generation_methods:
        print(m.name)
