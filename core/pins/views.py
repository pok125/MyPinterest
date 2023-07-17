from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseBadRequest
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


### PinDetail
class PinDetailView(View):
    # Pin상세 페이지
    def get(self, request, pin_id):
        pin = get_object_or_404(Pin, pk=pin_id)
        context = {
            'pin_id': pin_id,
            'pin_writer_id': pin.writer.pk,
            'pin_image_url': pin.image.url,
            'pin_title': pin.title,
            'pin_content': pin.content,
            'pin_like_count': pin.like_count
        }
        
        return render(request, 'pins/detail.html', context=context)


### PinUpdate
class PinUpdateView(LoginRequiredMixin ,View):
    
    def get_initial(self, pin):
        initial = dict()
        initial['title'] = pin.title
        initial['group'] = pin.group
        initial['image'] = pin.image
        initial['content'] = pin.content
        return initial
    
    # Pin수정 페이지
    def get(self, request, pin_id):
        pin = get_object_or_404(Pin, pk=pin_id)
        user = request.user

        if pin.writer != user:
            return HttpResponseBadRequest()
        
        initial = self.get_initial(pin)
        form = PinCreationForm(initial=initial)
        context = {
            'pin_id': pin_id,
            'form': form
        }

        return render(request, 'pins/update.html', context=context)
    
    # Pin수정 요청
    def post(self, request, pin_id):
        pin = get_object_or_404(Pin, pk=pin_id)
        form = PinCreationForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            pin.title = form.cleaned_data['title']
            pin.group = form.cleaned_data['group']
            pin.image = form.cleaned_data['image']
            pin.content = form.cleaned_data['content']
            pin.save()

            return redirect('pins:detail', pin_id=pin_id)
        
        messages.add_message(request, messages.ERROR, 'Pin수정에 실패하였습니다.')
        context = {
            'pin_id': pin_id,
            'form': form
        }

        return render(request, 'pins/update.html', context=context)