from django.urls import path
from .views import CategoryDocumentsListView, DocumentsByCategoryListView


urlpatterns = [
    path('get_categories/<int:residence_id>/' ,CategoryDocumentsListView.as_view() , name='get_categories'),
    path('get_documents_bycat/<int:residence_id>/<str:category>/',DocumentsByCategoryListView.as_view() , name='get_documents_bycat' )
]