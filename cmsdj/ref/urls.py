from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^pmu/$',      views.pmu_list, name='pmu_list'),
)
