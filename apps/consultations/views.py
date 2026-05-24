from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Consultation
from .forms import ConsultationForm

@login_required
def client_ai(request):
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            consultation = form.save(commit=False)
            consultation.user = request.user
            consultation.answer = f"Получен запрос: {consultation.question}"
            consultation.save()
            return redirect('client_ai')
    else:
        form = ConsultationForm()
    consultations = Consultation.objects.filter(user=request.user).order_by('-datetime_create')
    return render(request, 'consultations/ai.html', {'consultations': consultations, 'form': form})