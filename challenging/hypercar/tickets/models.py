from django.db import models


# A custom Manager class which handles common operations needed when working with tickets stored in the database.
class TicketManager(models.Manager):
    def __init__(self):
        # On initialization, first call the superclass constructor.
        super().__init__()

        # Create fields containing the id to assign to the next ticket created and to store a reference to the current
        # ticket being processed.
        self.current_id = 1
        self.current_ticket = None

    # Return a dictionary containing the quantity of each type of service ticket stored in the database.
    def amounts(self):
        # Retrieve the number of entries of each service type by filter the database by service type.
        oil = self.all().filter(service='O').count()
        tire = self.all().filter(service='T').count()
        diag = self.all().filter(service='D').count()

        # Store the retrieved quantities in a dictionary.
        dictionary = {'O': oil, 'T': tire, 'D': diag}

        # If there is a ticket currently being processed, subtract 1 from the number of entries found of its same
        # service type.
        if self.current_ticket is not None:
            dictionary[self.current_ticket.service] -= 1

        # Return the dictionary containing ticket quantities to the caller.
        return dictionary

    # Return the id field of the ticket that is currently being processed, if any.
    def next_ticket(self):
        if self.current_ticket is not None:
            return self.current_ticket.id

        # Return an invalid id value if no ticket is currently being processed.
        return 0

    # Calculate and return the current wait time for the specified service type.
    def current_wait(self, service: str):
        # Store a dictionary containing the quantities of tickets of each service type.
        amounts = self.amounts()

        # Calculate the current wait time for the specified ticket type.
        if service == 'O':
            # If the specified service type is an oil change, it must only wait for other oil changes to be completed.
            return 2 * amounts['O']
        elif service == 'T':
            # If the specified service type is a tire rotation, it must wait for other tire rotations as well as all oil
            # changes to be completed.
            return 2 * amounts['O'] + 5 * amounts['T']
        elif service == 'D':
            # If the specified service type is an diagnostic, it must wait for other diagnostics as well as all oil
            # changes and tire rotations to be completed.
            return 2 * amounts['O'] + 5 * amounts['T'] + 30 * amounts['D']
        else:
            # If the specified service does not match any of the possible service types, raise an exception.
            raise ValueError()

    # Create a new ticket of the specified service type.
    def new_ticket(self, service):
        # Create the new database table entry.
        ticket = self.create(id=self.current_id, service=service)

        # Increment the current id counter field.
        self.current_id += 1

        # Return the id of the newly created ticket.
        return ticket.id

    # Process the next ticket in the queue.
    def process_next(self):
        # Store a dictionary containing the quantities of tickets of each service type.
        amounts = self.amounts()

        # If there is a reference to a ticket saved in the current ticket field, delete it.
        if self.current_ticket is not None:
            self.all().filter(id=self.current_ticket.id).delete()

        # Update the current ticket field with the next ticket to be processed, if any.
        if amounts['O'] > 0:
            # If there are any oil change tickets in the queue, process the one with the lowest id next.
            self.current_ticket = self.all().filter(service='O').first()
        elif amounts['T'] > 0:
            # Otherwise, if there are any tire rotation tickets in the queue, process the one with the lowest id next.
            self.current_ticket = self.all().filter(service='T').first()
        elif amounts['D'] > 0:
            # Otherwise, if there are any diagnostic tickets in the queue, process the one with the lowest id next.
            self.current_ticket = self.all().filter(service='D').first()
        else:
            # Otherwise, the queue is empty, so empty the current ticket field.
            self.current_ticket = None


# A Model class that represents a database table entry that contains a service ticket.
class Ticket(models.Model):
    # Defines the types of service requests and their names.
    SERVICE_CHOICE = (
        ('O', 'Change Oil'),
        ('T', 'Inflate Tires'),
        ('D', 'Diagnostic')
    )

    # Explicitly define a key field.
    id = models.AutoField(primary_key=True)

    # Define a field containing the service type of a ticket.
    service = models.CharField(max_length=1, choices=SERVICE_CHOICE)

    # Define a custom Manager to provide methods for specialized database operations.
    objects = TicketManager()

    # Order the database table by the id field of each entry and specify its name.
    class Meta:
        ordering = ['id']
        db_table = 'tickets'
