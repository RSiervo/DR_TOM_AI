from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import get_template
from xhtml2pdf import pisa
from .forms import AnalyzeForm
from .models import Consultation
from ai_core.gemini import analyze
import io
from django.shortcuts import redirect
from django.shortcuts import render

def privacy_view(request):
    return render(request, "privacy.html")



def home_view(request):
    return render(request, "medical/home.html")

@login_required
def analyze_view(request):
    result = None
    if request.method == "POST":
        form = AnalyzeForm(request.POST, request.FILES)
        if form.is_valid():
            symptoms = form.cleaned_data.get('symptoms_text', '').strip()
            image = form.cleaned_data.get('image')

            c = Consultation(symptoms_text=symptoms, user=request.user)  # link user
            if image:
                c.image = image
            c.save()

            image_path = c.image.path if c.image else None
            result_text = analyze(symptoms, image_path)
            c.result_text = result_text
            c.save(update_fields=['result_text'])

            messages.success(request, "Analysis complete.")
            return redirect(c.get_absolute_url())  # <— go to detail page
    else:
        form = AnalyzeForm()

    # bottom of analyze_view
    return render(request, "medical/analyze.html", {"form": form})


@login_required
def history_view(request):
    items = Consultation.objects.filter(user=request.user).order_by("-created_at")[:100]
    return render(request, "medical/history.html", {"items": items})


@login_required
def consultation_detail(request, pk):
    c = get_object_or_404(Consultation, pk=pk)
    # only owner or staff can view
    if c.user and c.user != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to view this consultation.")
    return render(request, "medical/consultation_detail.html", {"c": c})

@login_required
def consultation_pdf(request, pk):
    c = get_object_or_404(Consultation, pk=pk)
    if c.user and c.user != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to export this consultation.")

    template = get_template("medical/consultation_pdf.html")
    html = template.render({"c": c, "request": request})  # request if you use absolute URIs

    # render to PDF
    result = io.BytesIO()
    pdf = pisa.CreatePDF(src=html, dest=result, encoding='utf-8',
                         link_callback=lambda uri, rel: uri)  # basic resolver

    if pdf.err:
        return HttpResponse("Error generating PDF", status=500)

    filename = f"DrTomAI_Consultation_{c.id}.pdf"
    resp = HttpResponse(result.getvalue(), content_type='application/pdf')
    resp['Content-Disposition'] = f'attachment; filename="{filename}"'
    return resp