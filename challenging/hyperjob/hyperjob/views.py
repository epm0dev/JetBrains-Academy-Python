from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.views import View
from django.shortcuts import render
from resume.models import Resume
from vacancy.models import Vacancy


# A view which inherits from Django's built in CreateView class and displays a form allowing the user to signup.
class MySignupView(CreateView):
    # The form for entering the new user's username and password.
    form_class = UserCreationForm

    # The URL to which the user is redirected upon successfully creating their account.
    success_url = '/login'

    # The name of the template from which to render the view's content.
    template_name = 'signup.html'

    # The model of the object being created. A User in this case.
    model = User


# A view which inherits from Django's built in LoginView class and displays a simple login form.
class MyLoginView(LoginView):
    # The form for entering an existing user's credentials.
    form_class = AuthenticationForm

    # Specify that a user should be redirected once authenticated. The URL of the redirect is specified by
    # LOGIN_REDIRECT_URL in settings.py.
    redirect_authenticated_user = True

    # The name of the template from which to render the view's content.
    template_name = 'login.html'


# Displays the currently authenticated user's profile, if any.
class ProfileView(View):
    # The name of the template from which to render the view's content.
    template_name = 'profile.html'

    # Handle GET requests.
    def get(self, request):
        # Create empty variables to store context for the view's template.
        posts = None
        href = None
        prompt = None

        # Check that the user is logged in.
        if request.user.is_authenticated:
            # Check if the user is staff or not.
            if request.user.is_staff:
                # If the user is staff, they can only create new vacancies, so update the context variables accordingly.
                posts = Vacancy.objects.filter(author=request.user)
                href = '/vacancy/new'
                prompt = 'New Vacancy'
            else:
                # If the user is not staff, they can only create new resumes, so update the context variables
                # accordingly.
                posts = Resume.objects.filter(author=request.user)
                href = '/resume/new'
                prompt = 'New Resume'

        # Store the values of the context variables in a dictionary object.
        context = {'user': request.user, 'list': posts, 'href': href, 'prompt': prompt}

        # Render and return the view's template with the current context.
        return render(request, self.template_name, context)
