# Slot-booking

Planning to host a meeting or conduct an interview in a private and highly business-like environment?  We have rental meeting room with facilities for a range of requirements. Also, you can book a meeting room by slot basis.

##### Types Of User:
 - Customer
 - Manager
    
##### General User
 - Allows new users to register.
 - Allows existing users to sign in.
 - Allows authenticated User to change password, edit profile.
  
##### Manager
 - Room Manager can add and delete Time Slots.
 - Room Manager can view upcoming bookings by customer.
 - Room Manager can edit the number of days to book in advance.

##### Customer
 - A Customer can book Time Slot, once booked, the time slotslot cannot be booked by another Customer for same time slot on same date.
 - A Customer can book a room x days in advance specifed by the manager.
 - The customer can view all bookings as well as cancelled bookings.

### Prerequisites

Python 3 and higher version.
Django 2.1.7


### Installing
1. How to install virtualenv

$ pip install virtualenv 
$ virtualenv -p /usr/bin/python env
$ source env/bin/activate


2. Installing requirements

$ pip install -r requirement.txt


3. Change directory to main

$ cd main
$ python manage.py makemigrations account
$ python manage.py makemigrations manager
$ python manage.py makemigrations client
$ python manage.py migrate


4. Run the application, running on localhost.

$ python3 manage.py runserver

open [localhost](http://127.0.0.1:8000/) in browser.

### Running the tests

$ python manage.py test
