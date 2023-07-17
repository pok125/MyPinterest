from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PinCreationForm
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


### PinCreate
class PinCreateView(LoginRequiredMixin, View):
    # pin생성 페이지
    def get(self, request):
        form = PinCreationForm()
        context = {
            'form': form
        }

        return render(request, 'pins/create.html', context=context)
    
    # pin생성 요청
    def post(self, request):
        form = PinCreationForm(data=request.POST, files=request.FILES)
        user = request.user

        #  form 유효성 체크
        if form.is_valid():
            pin = form.save(commit=False)
            pin.writer = user
            pin.save()
            
            return redirect('pins:list')
        
        messages.add_message(request, messages.ERROR, 'Pin생성에 실패하였습니다.')
        context = {
            'form': form
        }
        
        return render(request, 'pins/create.html', context=context)

