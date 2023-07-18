from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import Comment
from .forms import CommentCreationForm
from pins.models import Pin


### CommentCreate
class CommentCreateView(LoginRequiredMixin ,View):
    # 댓글 생성 요청
    def post(self, request, pin_id):
        pin = get_object_or_404(Pin, pk=pin_id)
        user = request.user
        form = CommentCreationForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.writer = user
            comment.pin = pin
            comment.save()

            return redirect('pins:detail', pin_id=pin_id)
        
        messages.add_message(request, messages.ERROR, '댓글 생성에 실패했습니다.')
        comments = pin.comment.all()
        context = {
            'pin_id': pin_id,
            'pin_writer_id': pin.writer.pk,
            'pin_image_url': pin.image.url,
            'pin_title': pin.title,
            'pin_content': pin.content,
            'pin_like_count': pin.like_count,
            'comments': comments
        }

        return render(request, 'pins/detail.html', context=context)


### CommentDelete
class CommentDeleteView(LoginRequiredMixin, View):
    # 삭제 요청
    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        user = request.user

        if user != comment.writer:
            return HttpResponseBadRequest()
        
        pin_id = comment.pin.pk
        comment.delete()

        return redirect('pins:detail', pin_id=pin_id)
