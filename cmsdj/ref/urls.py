from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^$',          views.index, name='ref_index'),
    url(r'^pmu/$',      views.pmu_list, name='pmu_list'),
)
