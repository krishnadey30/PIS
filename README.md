# Website for IOT based PLANT IRRIGATION SYSTEM
This is an IOT based website which is developed by my team as part of our project in 3rd semester engineering in Indian Institute of Information Technology, SriCity. This website reads the data sent from arduino and update those values in the database.


## Requirements

* [Python](https://www.python.org/)   (2.7 tested)
* [Django]( https://www.djangoproject.com/)
* [PIL]( https://python-pillow.org/)

## Getting Started

To clone and run this application, you'll need Git and Python installed on your computer. I assume you already setup the django environment on your machine, if not yet, then Google is your friend. From your command line:

### Clone this repository
```
$ git clone https://github.com/krishnadey30/Plant-Irrigation-System.git
```

### Go into the repository
```
$ cd Plant-Irrigation-System
```

### Migrate the databse
```
$ python manage.py makemigrations && python manage.py migrate
```

### Run the app
```
$ python manage.py runserver
```

Note: If those commands is not working, please open issue with detailed error messages.
## Contributers

* [Vishakha](https://github.com/vishakhakhurangale)
* [Preethi Hena](https://github.com/preethihena)
* [Sahithi Krishna](https://github.com/sahithikrishna)
* [Renuka Ram](https://github.com/renukaram)
