from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required

from .models import ChatMessage, HealthRecord
from .serializers import ChatMessageSerializer
from .forms import HealthRecordForm


# ---------------------------
# CHAT API
# ---------------------------
class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all().order_by('-timestamp')
    serializer_class = ChatMessageSerializer

    def create(self, request, *args, **kwargs):
        user_text = request.data.get('text')

        # Save user's message
        user_msg = ChatMessage.objects.create(
            user=request.user if request.user.is_authenticated else None,
            sender='user',
            text=user_text
        )

        # Dummy bot response
        bot_text = "Thank you! I am analyzing your symptoms..."

        bot_msg = ChatMessage.objects.create(
            user=request.user if request.user.is_authenticated else None,
            sender='bot',
            text=bot_text
        )

        return Response({
            "user_message": ChatMessageSerializer(user_msg).data,
            "bot_message": ChatMessageSerializer(bot_msg).data
        }, status=status.HTTP_201_CREATED)


# ---------------------------
# HEALTH RECORDS PAGE
# ---------------------------
@login_required
def health_records(request):

    if request.method == "POST":

        # DELETE
        if "delete_id" in request.POST:
            HealthRecord.objects.filter(id=request.POST["delete_id"], user=request.user).delete()
            return redirect("health-records")

        # UPLOAD
        form = HealthRecordForm(request.POST, request.FILES)
        if form.is_valid():
            rec = form.save(commit=False)
            rec.user = request.user
            rec.save()
            return redirect("health-records")

    else:
        form = HealthRecordForm()

    records = HealthRecord.objects.filter(user=request.user).order_by("-uploaded_at")

    return render(request, "chatbot/health_records.html", {
        "form": form,
        "records": records
    })


# ---------------------------
# STATIC PAGES
# ---------------------------
def chat_page(request):
    return render(request, "chatbot/chat.html")


def dashboard(request):
    return render(request, "chatbot/dashboard.html")


def alerts_page(request):
    return render(request, "chatbot/alerts.html")


def chat_history(request):
    return render(request, "chatbot/chat_history.html")
