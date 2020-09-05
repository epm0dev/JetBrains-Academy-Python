from django.views import View
from django.shortcuts import render


# Displays a simple menu containing hyperlinks for the user to navigate the website.
class MenuView(View):
    # The name of the template from which to render the view's content.
    template_name = 'menu/menu.html'

    # Handle GET requests.
    def get(self, request):
        # Render and return the view's template without a context dictionary.
        return render(request, self.template_name)
