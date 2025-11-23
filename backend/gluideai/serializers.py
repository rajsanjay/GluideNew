"""
Serializers for GluideAI app.
"""

from rest_framework import serializers
from django.conf import settings


class TranscriptParseSerializer(serializers.Serializer):
    """
    Validates input for transcript parsing endpoint.
    CRITICAL: Field names and validation MUST match documentation exactly.
    Reference: REWRITE_SPECIFICATION.md lines 88-118
    """
    file_path = serializers.CharField(
        max_length=500,
        required=True,
        help_text="S3 path to PDF file (must end with .pdf)"
    )
    webhook_url = serializers.URLField(
        required=True,
        help_text="HTTP/HTTPS callback URL for results"
    )

    def validate_file_path(self, value):
        """
        Validate that:
        1. File ends with .pdf (case-insensitive)
        2. File exists in S3 bucket (DATABASE mode) or mock exists (TEST mode)
        """
        # Check PDF extension
        if not value.lower().endswith('.pdf'):
            raise serializers.ValidationError(
                "Only PDF files are supported for transcript parsing"
            )

        # In TEST mode, skip S3 validation
        if getattr(settings, 'USE_TEST_MODE', False):
            return value

        # In DATABASE mode, validate S3 file exists
        try:
            import boto3
            from botocore.exceptions import ClientError

            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME
            )

            s3_client.head_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=value
            )
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '')
            if error_code == '404':
                raise serializers.ValidationError(
                    f"File does not exist at the specified S3 path: {value}"
                )
            else:
                raise serializers.ValidationError(
                    f"Error validating S3 file path: {str(e)}"
                )

        return value

    def validate_webhook_url(self, value):
        """
        Validate webhook URL starts with http:// or https://
        """
        if not (value.startswith('http://') or value.startswith('https://')):
            raise serializers.ValidationError(
                "Webhook URL must start with http:// or https://"
            )
        return value
