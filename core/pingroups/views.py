from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .forms import PinGroupCreationForm
from .models import PinGroup


### PinGroupList
class PinGroupListView(LoginRequiredMixin, View):
    # PinGroup 페이지
    def get(self, request):
        user = request.user
        pingroups = user.pingroup.annotate(pin_count=Count("pin"))
        context = {"pingroup_list": pingroups}

        return render(request, "pingroups/list.html", context=context)


### PinGroupCreate
class PinGroupCreateView(LoginRequiredMixin, View):
    # PinGroup생성 페이지
    def get(self, request):
        form = PinGroupCreationForm()
        context = {"form": form}

        return render(request, "pingroups/create.html", context=context)

    # PinGroup생성 요청
    def post(self, request):
        form = PinGroupCreationForm(data=request.POST, files=request.FILES)
        user = request.user

        if form.is_valid():
            pingroup = form.save(commit=False)
            pingroup.user = user
            pingroup.save()

            return redirect("pingroups:list")

        messages.add_message(request, messages.ERROR, "PinGroup생성에 실패했습니다.")
        context = {"form": form}

        return render(request, "pingroups/create", context=context)


### PinGroupDetail
class PinGroupDetailView(LoginRequiredMixin, View):
    # PinGroup 상세 페이지
    def get(self, request, pingroup_id):
        pingroup = get_object_or_404(
            PinGroup.objects.select_related("user").prefetch_related("pin"),
            pk=pingroup_id,
        )
        user = request.user

        if pingroup.user != user:
            return HttpResponseBadRequest()

        pin_list = pingroup.pin.all()
        pin_count = len(pin_list)
        context = {"pingroup": pingroup, "pin_count": pin_count, "pin_list": pin_list}

        return render(request, "pingroups/detail.html", context=context)


### PinGroupUpdate
class PinGroupUpdateView(LoginRequiredMixin, View):

    def get_initial(self, pingroup):
        initial = dict()
        initial["title"] = pingroup.title
        initial["image"] = pingroup.image
        initial["content"] = pingroup.content

        return initial

    # update 페이지
    def get(self, request, pingroup_id):
        pingroup = get_object_or_404(PinGroup, pk=pingroup_id)
        user = request.user

        if pingroup.user != user:
            return HttpResponseBadRequest()

        initial = self.get_initial(pingroup)
        form = PinGroupCreationForm(initial=initial)
        context = {"pingroup_id": pingroup_id, "form": form}

        return render(request, "pingroups/update.html", context=context)

    # PinGroup 수정 요청
    def post(self, request, pingroup_id):
        pingroup = get_object_or_404(PinGroup, pk=pingroup_id)
        form = PinGroupCreationForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            pingroup.title = form.cleaned_data["title"]
            pingroup.image = form.cleaned_data["image"]
            pingroup.content = form.cleaned_data["content"]
            pingroup.save()

            return redirect("pingroups:list")

        messages.add_message(request, messages.ERROR, "PinGroup수정에 실패했습니다.")
        context = {"pingroup_id": pingroup_id, "form": form}

        return render(request, "pingroups/update.html", context=context)


### PinGroupDelete
class PinGroupDeleteView(LoginRequiredMixin, View):
    # 삭제 요청
    def post(self, request, pingroup_id):
        pingroup = get_object_or_404(PinGroup, pk=pingroup_id)
        user = request.user

        if pingroup.user != user:
            return HttpResponseBadRequest()

        pingroup.delete()

        return redirect("pingroups:list")
