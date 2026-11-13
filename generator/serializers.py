
from rest_framework import serializers


# Generate Content Serializer
class ContentGenerationSerializer(serializers.Serializer):
    topic = serializers.CharField(max_length=200, required=True)

    content_type = serializers.ChoiceField(
        choices=[
            'Blog',
            'Product Description',
            'Social Media Post',
            'SEO Description'
        ],
        required=True
    )

    tone = serializers.ChoiceField(
        choices=[
            'Professional',
            'Friendly',
            'Creative'
        ],
        required=True
    )

    length = serializers.ChoiceField(
        choices=[
            'Short',
            'Medium',
            'Long'
        ],
        required=True
    )


# Save Content Serializer
class SaveContentSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200, required=True)
    topic = serializers.CharField(max_length=200, required=True)
    content_type = serializers.CharField(max_length=100, required=True)
    tone = serializers.CharField(max_length=100, required=True)
    generated_content = serializers.CharField(required=True)


# Update Content Serializer
class UpdateContentSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200, required=True)
    topic = serializers.CharField(max_length=200, required=True)

    content_type = serializers.ChoiceField(
        choices=[
            'Blog',
            'Product Description',
            'Social Media Post',
            'SEO Description'
        ],
        required=True
    )

    tone = serializers.ChoiceField(
        choices=[
            'Professional',
            'Friendly',
            'Creative'
        ],
        required=True
    )

    generated_content = serializers.CharField(required=True)
