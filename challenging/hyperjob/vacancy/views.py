from django.shortcuts import render
from django.views.generic.base import View
from .models import Vacancy
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied


# A simple view which displays a list of all of the vacancies stored in the database.
class VacancyListView(View):
    # The name of the template from which to render the view's content.
    template_name = 'vacancy/vacancy-list.html'

    # Handle GET requests.
    def get(self, request):
        # Render and return the view's template with a context dictionary containing all of the vacancies from the
        # database in a QuerySet located by the 'list' key.
        # noinspection PyUnresolvedReferences
        return render(request, self.template_name, {'list': Vacancy.objects.all()})


# A view class which only handles POST requests for creating new vacancies.
class NewVacancyView(View):
    # Handle POST requests.
    @staticmethod
    def post(request):
        # Ensure that the POST request was sent by an authenticated user who is a staff member.
        if not request.user.is_authenticated or not request.user.is_staff:
            # If the user who sent the request does not meet these criteria, raise an exception.
            raise PermissionDenied('User must be logged in as a staff user to create a new vacancy')

        # Create a new vacancy object in the database which has the description from the request and the username of the
        # user who sent the request.
        # noinspection PyUnresolvedReferences
        Vacancy.objects.create(description=request.POST.get('description'), author=request.user)

        # Redirect the user back to the home menu.
        return redirect('/home')
