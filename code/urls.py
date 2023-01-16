from django.urls import re_path as url
from . import views,testdb,search,search2
 
urlpatterns = [
    url(r'^hello/$', views.index),
    url(r'^testdb/[a-zA-Z]{5}/$', testdb.testdb),
    url(r'^search-form/$', search.search_form,name='search-form'),
    url(r'^del-form/$',search.del_form,name="del-form"),
    url(r'^delete/$',search.delete,name='del'),
    url(r'^search/$', search.search,name='search'),
    url(r'^search-post/$', search2.search_post,name='search-post'),
    url(r'^rank/$',search.rank,name='rank'),
    url(r'^OLAP/$',search.OLAP_form,name='OLAP'),
    url(r'^OLAPS/$',search.OLAP,name='OLAPS'),
    url(r'^sql-form/$',search.sql_form,name='sql-form'),
    url(r'^sql/$',search.sql,name='sql'),
    url(r'^cust-form/$',search.cust_form,name='cust-form'),
    url(r'^cust/$',search.cust,name='cust'),
    url(r'^login/$',search.login,name='login')
]