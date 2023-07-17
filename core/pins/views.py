from django.shortcuts import render
from django.views import View
from .models import Pin


### PinList
class PinListView(View):
    # pin리스트 페이지
    def get(self, request):
        pins = Pin.objects.all()
        context = {
            'pin_list': pins
        }
        
        return render(request, 'pins/list.html', context=context)
