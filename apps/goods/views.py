from django.shortcuts import render
from django.views import View


class IndexView(View):
    """首页"""
    def get(self, request):
        """显示首页"""
        return render(request, "index.html")
