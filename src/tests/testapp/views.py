from django.utils.timezone import now
from django.views.generic import TemplateView


class TransExampleView(TemplateView):
    def get_context_data(self, **kwargs):
        context_data = super(TransExampleView, self).get_context_data(**kwargs)
        context_data['date'] = now()
        return context_data