# Putting it all together

- We've used and extended the base auth model.
- We've used Django forms to streamline validations and the form writing process.
- We've used class-based views!

### Now, let's incorporate Django REST Framework!

- Hold on, what's that?

It's a framework (a tool)
that uses Django
to easily and rapidly
build RESTful APIs!

- APIs?
 - Yeah, the interface by which requests are sent to, and data returned from, remote servers!
- Does that mean all our servers we've built are APIs?
 - Yup.
- And you're telling me I can do it easier?
 - Yup.

### Okay, now let's really begin.
- First we turn on our Django virtual environment and navigate (in our terminal) to a good place for a new project, inside our Django projects folder

 - someplace like ~/Code/Python/Django

 First off, in our terminal and with our virtual environment active, we will `pip install djangorestframework`. I'm assuming that at minimum t


- Next we start a new Django project:
	- `django-admin startproject djangoREST`
	- `cd djangoREST`
	- `mkdir apps`
	- `cd apps`
	- `touch __init__.py`
- And add a new app:
	- `../manage.py startapp root_app`
	- `cd ..`

Great! Now we have an app. To incorporate the Django Rest Framework bits, we'll need to add it to INSTALLED_APPS in our djangoREST/settings.py file!

```python
INSTALLED_APPS = {
	'apps.root_app',
	'rest_framework',
	... #(all the stuff that was there before)
}
```

We will also update our main project folder's urls.py file:

root_app/urls.py
```python
from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
	url(r'^', include('apps.root_app.urls', namespace='root_app')),
	url(r'^api/', include('rest_framework.urls', namespace='rest_framework')),
]
```

Now we're done with the project-level stuff and can move in to the app! Click in to apps/root_app in your text editor's tree view.

Now create a root_app/urls.py file and add more than usual to it:

```python
from django.conf.urls import url, include
from rest_framework import routers
from . import views

"""
instead of manually creating each RESTful route in our views.py, we can import rest_framework's routers, which will set all of that up for us in one line.
The first parameter is the prefix which will belong to this cluster of urls. The second parameter, the ViewSet, is the collection of methods which provide the functionality.

	router.register(r'users', views.UserViewSet)

The single line above is equivalent to the following:

	url(r'groups/$', views.index, name="index"),
	url(r'groups/(?P<id>)/$', views.show, name="detail")

"""
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

#here we include our router's urls
urlpatterns = [
	url(r'^', include(router.urls)),
]

```

Almost there! What's next? Moving in to our views.py to define these ViewSets. Class Based Views for the win!

root_app/views.py
```python
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from serializers import UserSerializer, GroupSerializer

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all().order_by('-date_joined')
	serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
	queryset = Group.objects.all()
	serializer_class = GroupSerializer
```

Yes, that was our ENTIRE views.py file. Skinny controllers, remember? The ViewSet is taking care of the related show and index pages all in one go!

You'll also notice that we're importing Django's base User and Group models. This saves us from having to do _anything_ in our models.py file at this point.

Finally, on to serializers.py, a new file we'll create:

root_app/serializers.py
```python
from django.contrib.auth.models import User, Group
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Group
		fields = ('url', 'name')

```

A serializer takes your data and formats it so it can saved to disk or sent to someone else. It would be possible to serialize our data into consistent, computer-independent Python code using python's built in Pickle module, but in this case we'll be serializing our data into JSON, a pretty standard choice for APIs. Django Rest Framework makes this super easy for us!

If you've done all this, you should be able to make migrations (`python manage.py makemigrations`, `python manage.py migrate` in your terminal) and fire up your server (`python manage.py runserver`) and see an auto-generated API web interface!

To actually add data, though, we'll need to add a superuser to our database.

Thankfully, that's only one more terminal command.
`python manage.py createsuperuser`
You will be prompted for username, email, password, and password confirmation.

Once you've done that, 'runserver' again and hit the 'Log In' button in the top right corner of localhost:8000. 

Log in with your newly created superuser's credentials and play with your very own API and its slick web interface!
