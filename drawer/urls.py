from django.urls import path
from .views import tag_list, tag_create, tag_update, tag_delete, file_list, file_create, file_delete, file_archive

urlpatterns = [
    path("tags/", tag_list, name="tag_list"),
    path("tags/create/", tag_create, name="tag_create"),
    path("tags/<int:pk>/update/", tag_update, name="tag_update"),
    path("tags/<int:pk>/delete/", tag_delete, name="tag_delete"),

    # for files

    path("files/", file_list, name="file_list"),
    path("files/create/", file_create, name="file_create"),
    path("files/<int:pk>/archive/", file_archive, name="file_archive"),
    path("files/<int:pk>/delete/", file_delete, name="file_delete"),


]