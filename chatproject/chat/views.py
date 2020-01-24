from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import FormMixin
from django.views.generic import DetailView, ListView
from .forms import ComposeForm
from .models import Thread, ChatMessage


class InboxView(LoginRequiredMixin, ListView):
    count =0
    print('view-> inboxView')
    count += 1
    template_name = 'chat/inbox.html'
    def get_queryset(self):
        print('view->InboxView->get_queryset')
        return Thread.objects.by_user(self.request.user)


class ThreadView(LoginRequiredMixin, FormMixin, DetailView):
    print('view-> ThreadView')
    template_name = 'chat/thread.html'
    form_class = ComposeForm
    success_url = "./"

    def get_queryset(self):
        print('view->ThreadView-> get_queryset')
        print("get_queryset")
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        print("view->ThreadView-> get_object")
        other_username  = self.kwargs.get("username")
        print("other username = ",other_username)
        obj, created    = Thread.objects.get_or_new(self.request.user, other_username)
        if obj == None:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        print("view->ThreadView-> get_context_data")
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        print("view->ThreadView-> posts")
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        print("view->ThreadView-> form_valid")
        thread = self.get_object()
        user = self.request.user
        message = form.cleaned_data.get("message")
        ChatMessage.objects.create(user=user, thread=thread, message=message)
        return super().form_valid(form)
