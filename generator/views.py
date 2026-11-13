import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    ContentGenerationSerializer,
    SaveContentSerializer,
    UpdateContentSerializer,
)

from .services import generate_ai_content

from .contentful_service import (
    save_content_to_contentful,
    get_saved_content_from_contentful,
    update_content_in_contentful,
    delete_content_from_contentful,
)


# 1. Generate Content (Mock Generation)

@api_view(["POST"])
def generate_content(request):
    serializer = ContentGenerationSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    data = serializer.validated_data

    try:
        generated_content = generate_ai_content(
            topic=data["topic"],
            content_type=data["content_type"],
            tone=data["tone"],
            length=data.get("length", "Medium")
        )

        return Response(
            {
                "success": True,
                "message": "Content generated successfully using mock generation.",
                "generated_content": generated_content
            },
            status=status.HTTP_200_OK
        )

    except Exception as e:
        print("Mock Generation Error:", repr(e))

        return Response(
            {
                "success": False,
                "message": "Unable to generate content."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# 2. Save Content to Contentful

@api_view(["POST"])
def save_content(request):
    serializer = SaveContentSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        entry_id = save_content_to_contentful(
            **serializer.validated_data
        )

        return Response(
            {
                "success": True,
                "message": "Content saved successfully.",
                "entry_id": entry_id
            },
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        print("Contentful Save Error:", repr(e))

        return Response(
            {
                "success": False,
                "message": "Unable to save content to Contentful."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# 3. Get Saved Content

@api_view(["GET"])
def get_saved_content(request):
    try:
        saved_content = get_saved_content_from_contentful()

        return Response(
            {
                "success": True,
                "data": saved_content
            },
            status=status.HTTP_200_OK
        )

    except Exception as e:
        print("Contentful Get Error:", repr(e))

        return Response(
            {
                "success": False,
                "message": "Unable to retrieve saved content."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# 4. Update Content

@api_view(["PUT"])
def update_content(request, entry_id):
    serializer = UpdateContentSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        update_content_in_contentful(
            entry_id=entry_id,
            **serializer.validated_data
        )

        return Response(
            {
                "success": True,
                "message": "Content updated successfully.",
                "entry_id": entry_id
            },
            status=status.HTTP_200_OK
        )

    except Exception as e:
        print("Contentful Update Error:", repr(e))

        return Response(
            {
                "success": False,
                "message": "Unable to update content in Contentful."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# 5. Delete Content

@api_view(["DELETE"])
def delete_content(request, entry_id):
    try:
        delete_content_from_contentful(entry_id)

        return Response(
            {
                "success": True,
                "message": "Content deleted successfully.",
                "entry_id": entry_id
            },
            status=status.HTTP_200_OK
        )

    except requests.exceptions.HTTPError as e:
        print("Contentful Delete HTTP Error:", repr(e))

        if e.response is not None:
            print("Contentful Response:", e.response.text)

        return Response(
            {
                "success": False,
                "message": "Unable to delete content from Contentful."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    except Exception as e:
        print("Contentful Delete Error:", repr(e))

        return Response(
            {
                "success": False,
                "message": "Unable to delete content from Contentful."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
