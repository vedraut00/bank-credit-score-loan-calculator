"""
URL configuration for credit_system project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def test_view(request):
    """Simple test view to verify Django is working"""
    return JsonResponse({
        "status": "success",
        "message": "Django is working! 🎉",
        "timestamp": "2024-07-20"
    })

@csrf_exempt
def health_check(request):
    """Health check endpoint"""
    return JsonResponse({
        "status": "healthy",
        "service": "bank-credit-score-loan-calculator"
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('loans/', include('loans.urls')),
    path('test/', test_view, name='test'),
    path('health/', health_check, name='health'),
    path('', test_view, name='home'),  # Temporarily use test view for root
]
