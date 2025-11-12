from django.shortcuts import render
from .rag_agent import ask_rag_agent
from django.http.response import HttpResponse,JsonResponse
from .forms import ContactForm
import json
from django.views.decorators.csrf import csrf_exempt
def index(request):
    form = ContactForm()
    if request.method =='POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
    context ={'form':form}        
    return render(request,'index.html',context)
@csrf_exempt
def chat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            question = data.get("question", "")
            print(question)
            if not question:
                return JsonResponse({"error": "Please provide a question."}, status=400)

            answer = ask_rag_agent(question)
            
            if isinstance(answer, list):
                answer_text = "\n".join([a.get("text", "") for a in answer if isinstance(a, dict)])
            elif isinstance(answer, dict) and "text" in answer:
                answer_text = answer["text"]
            else:
                answer_text = str(answer)
            return JsonResponse({"answer": answer_text})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)