from django import forms

MAX_MB = 8
ALLOWED = {"image/jpeg","image/png","image/webp"}

class AnalyzeForm(forms.Form):
    symptoms_text = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 5,
            'placeholder': 'Describe symptoms (duration, severity, location, triggers)...'
        })
    )
    image = forms.ImageField(required=False)

    def clean_image(self):
        img = self.cleaned_data.get("image")
        if not img:
            return img
        if img.size > MAX_MB * 1024 * 1024:
            raise forms.ValidationError(f"Image must be under {MAX_MB} MB.")
        if img.content_type not in ALLOWED:
            raise forms.ValidationError("Only JPG, PNG, or WebP images are allowed.")
        return img
