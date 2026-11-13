
from django.urls import path

from .views import (
    generate_content,
    save_content,
    get_saved_content,
    update_content,
    delete_content
)

urlpatterns = [
    path(
        "generate-content/",
        generate_content,
        name="generate_content"
    ),
    path(
        "save-content/",
        save_content,
        name="save_content"
    ),
    path(
        "saved-content/",
        get_saved_content,
        name="get_saved_content"
    ),
    path(
        "update-content/<str:entry_id>/",
        update_content,
        name="update_content"
    ),
    path(
        "delete-content/<str:entry_id>/",
        delete_content,
        name="delete_content"
    ),
]
