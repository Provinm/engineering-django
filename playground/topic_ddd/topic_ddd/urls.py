"""
URL configuration for topic_ddd project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from example1.views import poll as example1_poll
from example2.views import poll as example2_poll
from example3.views import info, purchase
from example4.views import info as example4_info
from example4.views import purchase as example4_purchase

urlpatterns = [
    path("api/example1/poll", view=example1_poll, name="example1_poll"),
    path("api/example2/poll", view=example2_poll, name="example2_poll"),
    path("api/example3/info", view=info, name="info"),
    path("api/example3/purchase", view=purchase, name="purchase"),
    path("api/example4/purchase", view=example4_purchase, name="purchase4"),
    path("api/example4/info", view=example4_info, name="info4"),
]
