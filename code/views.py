from django.shortcuts import render

def index(request):
  views_name = "θιΈζη¨"
  return  render(request,"index.html", {"name":views_name})