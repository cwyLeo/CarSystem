from django.shortcuts import render

def index(request):
  views_name = "菜鸟教程"
  return  render(request,"index.html", {"name":views_name})