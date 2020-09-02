from django.views import View
from django.http.response import HttpResponse, Http404
from django.shortcuts import render, redirect
from . import models


# Handle requests for the welcome page.
class WelcomeView(View):
    # Respond to GET requests with a simple HTTP Response containing an HTML header and a welcome message.
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


# Handle requests for the menu page.
class MenuView(View):
    # Define the relative path of the View's HTML template.
    template_name = 'tickets/menu.html'

    # Respond to GET requests by rendering the View's HTML template.
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


# Handle requests for the ticket page.
class TicketView(View):
    # Define the relative path of the View's HTML template.
    template_name = 'tickets/ticket.html'

    # Respond to GET requests by creating a new service ticket and rendering the View's HTML template populated with
    # the id of the new ticket and the wait time for that ticket.
    def get(self, request, *args, **kwargs):
        # Determine the service type of the new ticket to create based on the requested URL.
        if request.path.startswith('/get_ticket/change_oil'):
            service = 'O'
        elif request.path.startswith('/get_ticket/inflate_tires'):
            service = 'T'
        elif request.path.startswith('/get_ticket/diagnostic'):
            service = 'D'
        else:
            # If none of the above conditions evaluate to true, the request is invalid, so raise an exception.
            raise Http404()

        # Determine the current wait for the new ticket, before creating it in the database.
        wait = models.Ticket.objects.current_wait(service)

        # Create the new ticket and store its id.
        ticket_id = models.Ticket.objects.new_ticket(service)

        # Construct a dictionary containing the new ticket's id and its wait time.
        context = {'ticket_number': ticket_id, 'wait_time': wait}

        # Render and return the View's HTML template populated with the values in the context dictionary.
        return render(request, self.template_name, context=context)


# Handle requests for the operator page.
class OperatorView(View):
    # Define the relative path of the View's HTML template.
    template_name = 'tickets/operator.html'

    # Respond to GET requests by retrieving the quantities of services of each service type in the database and
    # rendering the View's HTML template, populated with those values.
    def get(self, request, *args, **kwargs):
        context = models.Ticket.objects.amounts()
        return render(request, self.template_name, context=context)

    # Respond to POST requests by processing the next service ticket and redirecting the user back to the same page.
    def post(self, request, *args, **kwargs):
        models.Ticket.objects.process_next()
        return redirect('/processing')


# Handle requests for the next ticket page.
class NextView(View):
    # Define the relative path of the View's HTML template.
    template_name = 'tickets/next.html'

    # Respond to GET requests by retrieving the id of the next ticket in the database to be processed, then rendering
    # the View's HTML template, populated with the next ticket's id.
    def get(self, request, *args, **kwargs):
        context = {'next_ticket': models.Ticket.objects.next_ticket()}
        return render(request, self.template_name, context=context)
