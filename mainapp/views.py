from django.shortcuts import render


def get_api_doc(request):
    return render(request, "mainapp/api_doc.html")


