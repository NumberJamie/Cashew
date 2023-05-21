from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from Account.models import Account


class AccountDetailView(LoginRequiredMixin, DetailView):
    model = Account
    template_name = 'account/detail.html'

    def get_object(self, queryset=None):
        return Account.objects.get(username=self.kwargs.get('username'))