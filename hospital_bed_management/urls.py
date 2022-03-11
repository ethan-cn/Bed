"""hospital_bed_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from user import views as user_views
from patient import views as patient_views
from bed import views as bed_views

urlpatterns = [
                  path('', user_views.login),
                  path('index/', user_views.main),
                  path('user/', user_views.index),
                  path('user/show/', user_views.show),
                  path('login_check/', user_views.login_check),
                  path('delete_user/', user_views.delete_user),
                  path('login_out/', user_views.login_out),
                  path('redirect_new_user/', user_views.redirect_new_user),
                  path('get_user_by_name/', user_views.get_user_by_name),
                  path('get_user_by_id/', user_views.get_user_by_id),
                  path('add_user/', user_views.add_user),
                  path('modify_user/', user_views.modify_user),
                  path('redirect_patient/', patient_views.redirect_patient),
                  path('add_patient/', patient_views.add_patient),
                  path('query_patient/', patient_views.query_patient),
                  path('get_patient_by_id/', patient_views.get_patient_by_id),
                  path('get_patient_by_name/', patient_views.get_patient_by_name),
                  path('delete_patient/', patient_views.delete_patient),
                  path('redirect_new_patient/', patient_views.redirect_new_patient),
                  path('redirect_bed/', bed_views.redirect_bed),
                  path('modify_patient/', patient_views.modify_patient),
                  path('redirect_new_bed/', bed_views.redirect_new_bed),
                  path('get_bed_by_id/', bed_views.get_bed_by_id),
                  path('modify_bed/', bed_views.modify_bed),
                  path('query_bed/', bed_views.query_bed),
                  path('add_bed/', bed_views.add_bed),
                  path('delete_bed/', bed_views.delete_bed),
                  path('get_bed_by_name/', bed_views.get_bed_by_name),
                  path('query_department/', patient_views.query_department),
                  path('add_department/', patient_views.add_department),
                  path('modify_department/', patient_views.modify_department),
                  path('delete_department/', patient_views.delete_department),
                  path('redirect_new_department/', patient_views.redirect_new_department),
                  path('redirect_department/', patient_views.redirect_department),
                  path('get_department_by_name/', patient_views.get_department_by_name),
                  path('get_department_by_id/', patient_views.get_department_by_id),
                  path('admin/', admin.site.urls),



              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
