from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import PinGroup
from .forms import PinGroupCreationForm


### PinGroupList
class PinGroupListView(LoginRequiredMixin, View):
    # PinGroup 페이지
    def get(self, request):
        pingroups = PinGroup.objects.all()
        context = {
            'pingroup_list': pingroups
        }

        return render(request, 'pingroups/list.html', context=context)

### PinGroupCreate
class PinGroupCreateView(LoginRequiredMixin, View):
    # PinGroup생성 페이지
    def get(self, request):
        form = PinGroupCreationForm()
        context = {
            'form': form
        }
        
        return render(request, 'pingroups/create.html', context=context)
    
    # PinGroup생성 요청
    def post(self, request):
        form = PinGroupCreationForm(data=request.POST, files=request.FILES)
        user = request.user

        if form.is_valid():
            pingroup = form.save(commit=False)
            pingroup.user = user
            pingroup.save()

            return redirect('pingroups:list')
        
        messages.add_message(request, messages.ERROR, 'PinGroup생성에 실패했습니다.')
        context = {
            'form': form
        }

        return render(request, 'pingroups/create', context=context)