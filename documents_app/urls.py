from django.urls import path
from .views import CategoryDocumentsListView, DocumentsByCategoryListView, DocumentUploadView


urlpatterns = [
    path('get_categories/<int:residence_id>/' ,CategoryDocumentsListView.as_view() , name='get_categories'),
    path('get_documents_bycat/<int:residence_id>/<str:category>/',DocumentsByCategoryListView.as_view() , name='get_documents_bycat' ),
    path('upload_document/<int:residence_id>/' ,DocumentUploadView.as_view() , name='upload_document' ),
    
]