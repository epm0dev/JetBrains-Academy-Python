from django.shortcuts import render
from django.views.generic.base import View
from .models import Resume
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied


# A simple view which displays a list of all of the resumes stored in the database.
class ResumeListView(View):
    # The name of the template from which to render the view's content.
    template_name = 'resume/resume-list.html'

    # Handle GET requests.
    def get(self, request):
        # Render and return the view's template with a context dictionary containing all of the resumes from the
        # database in a QuerySet located by the 'list' key.
        # noinspection PyUnresolvedReferences
        return render(request, self.template_name, {'list': Resume.objects.all()})


# A view class which only handles POST requests for creating new resumes.
class NewResumeView(View):
    # Handle POST requests.
    @staticmethod
    def post(request):
        # Ensure that the POST request was sent by an authenticated user who is not a staff member.
        if not request.user.is_authenticated or request.user.is_staff:
            # If the user who sent the request does not meet these criteria, raise an exception.
            raise PermissionDenied('User must be logged in as a non-staff user to create a new resume')

        # Create a new resume object in the database which has the description from the request and the username of the
        # user who sent the request.
        # noinspection PyUnresolvedReferences
        Resume.objects.create(description=request.POST.get('description'), author=request.user)

        # Redirect the user back to the home menu.
        return redirect('/home')
