# Chat Chan
 
A simple chat server implemented using Django and Channels with WebSockets to send the messages asynchronously.

### Installation Guide

* Create a virtual environment
* `pip install -r requirements.txt` in your virtual environment
  * Use Python 3.7 if you have problem with installing `twisted`
* Install and Run Redis `redis-server --service-start`
  * Set your port to `6379` or you can change it in `settings.py`
* cd inside src directory
* `python manage.py migrate`
* `python manage.py runserver`