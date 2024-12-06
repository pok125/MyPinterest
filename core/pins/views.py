from comments.models import Comment
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .forms import CheckBookMarkForm, CheckLikeForm, PinCreationForm
from .models import BookMark, LikeRecord, Pin


### PinList
class PinListView(View):
    # pin리스트 페이지
    def get(self, request):
        pins = Pin.objects.only("id", "image", "title").annotate(
            liker_count=Count("likers")
        )
        context = {"pin_list": pins}

        return render(request, "pins/list.html", context=context)


### PinCreate
class PinCreateView(LoginRequiredMixin, View):
    # pin생성 페이지
    def get(self, request):
        form = PinCreationForm(user=request.user)
        context = {"form": form}

        return render(request, "pins/create.html", context=context)

    # pin생성 요청
    def post(self, request):
        user = request.user
        form = PinCreationForm(user=user, data=request.POST, files=request.FILES)

        #  form 유효성 체크
        if form.is_valid():
            pin = form.save(commit=False)
            pin.writer = user
            pin.save()

            return redirect("pins:list")

        messages.add_message(request, messages.ERROR, "Pin생성에 실패하였습니다.")
        context = {"form": form}

        return render(request, "pins/create.html", context=context)


### PinDetail
class PinDetailView(View):
    # Pin상세 페이지
    def get(self, request, pin_id):
        try:
            pin = Pin.objects.select_related("writer").get(pk=pin_id)
        except ObjectDoesNotExist as e:
            messages.add_message(request, messages.ERROR, "존재하지 않는 pin입니다.")

            return redirect("pins:list")

        comments = Comment.objects.select_related("pin", "writer").filter(
            pin__id=pin_id
        )
        context = {
            "pin": pin,
            "comments": comments,
        }

        return render(request, "pins/detail.html", context=context)


### PinUpdate
class PinUpdateView(LoginRequiredMixin, View):

    def get_initial(self, pin):
        initial = dict()
        initial["title"] = pin.title
        initial["group"] = pin.group
        initial["image"] = pin.image
        initial["content"] = pin.content
        return initial

    # Pin수정 페이지
    def get(self, request, pin_id):
        pin = get_object_or_404(Pin, pk=pin_id)
        user = request.user

        if pin.writer != user:
            return HttpResponseBadRequest()

        initial = self.get_initial(pin)
        form = PinCreationForm(user=user, initial=initial)
        context = {"pin_id": pin_id, "form": form}

        return render(request, "pins/update.html", context=context)

    # Pin수정 요청
    def post(self, request, pin_id):
        pin = get_object_or_404(Pin, pk=pin_id)
        form = PinCreationForm(
            user=request.user, data=request.POST, files=request.FILES
        )

        if form.is_valid():
            pin.title = form.cleaned_data["title"]
            pin.group = form.cleaned_data["group"]
            pin.image = form.cleaned_data["image"]
            pin.content = form.cleaned_data["content"]
            pin.save()

            return redirect("pins:detail", pin_id=pin_id)

        messages.add_message(request, messages.ERROR, "Pin수정에 실패하였습니다.")
        context = {"pin_id": pin_id, "form": form}

        return render(request, "pins/update.html", context=context)


### PinDelete
class PinDeleteView(LoginRequiredMixin, View):
    # 삭제요청
    def post(self, request, pin_id):
        user = request.user
        pin = get_object_or_404(Pin, pk=pin_id)

        if pin.writer != user:
            return HttpResponseBadRequest()

        pin.delete()

        return redirect("pins:list")


### Like
class LikeView(LoginRequiredMixin, View):
    # 좋아요 요청
    def get(self, request, pin_id):
        user = request.user
        pin = get_object_or_404(Pin, pk=pin_id)
        like_record = LikeRecord.objects.filter(user=user, pin=pin)

        # 이미 존재하면 좋아요 취소
        if like_record.exists():
            like_record.delete()
        else:
            form = CheckLikeForm(data={"pin": pin, "user": user})
            if form.is_valid():
                form.save()
            else:
                for errors in form.errors.values():
                    for error in errors:
                        print(f"Form Error - {error}")
                        messages.add_message(request, messages.ERROR, error)

        return redirect("pins:detail", pin_id=pin_id)


### BookMark
class BookMarkView(LoginRequiredMixin, View):
    # 즐겨찾기 요청
    def get(self, request, pin_id):
        user = request.user
        pin = get_object_or_404(Pin, pk=pin_id)
        book_mark = BookMark.objects.filter(user=user, pin=pin)

        # 이미 존재하면 즐겨찾기 취소
        if book_mark.exists():
            book_mark.delete()
        else:
            form = CheckBookMarkForm(data={"pin": pin, "user": user})
            if form.is_valid():
                form.save()
            else:
                for errors in form.errors.values():
                    for error in errors:
                        print(f"Form Error - {error}")
                        messages.add_message(request, messages.ERROR, error)

        return redirect("pins:detail", pin_id=pin_id)


### BookMarkList
class BookMarkListView(LoginRequiredMixin, View):
    # bookmark리스트 페이지
    def get(self, request):
        user = request.user
        bookmarks = BookMark.objects.select_related("pin", "user").filter(user=user)
        pins = [bookmark.pin for bookmark in bookmarks]
        context = {"pin_list": pins}

        return render(request, "pins/bookmark_list.html", context=context)
