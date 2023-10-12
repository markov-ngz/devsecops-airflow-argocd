# Temporary view , used to test github social authentication
from django.views.generic import TemplateView

class Home(TemplateView):
    template_name = 'socialaccount/home.html'