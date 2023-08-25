from django.core.exceptions import ValidationError


def only_int(value):
    if value.isdigit() is False:
        raise ValidationError("Solo se permiten números")


def validate_document_number(document_type, document_number):
    if not (
        document_type.min_length
        <= len(document_number)
        <= document_type.max_length
    ):
        if document_type.min_length == document_type.max_length:
            message = (
                f"El {document_type.code} debe tener"
                f" {document_type.min_length} dígitos."
            )
        else:
            message = (
                f"El {document_type.code} debe tener entre"
                f" {document_type.min_length} y"
                f" {document_type.max_length} dígitos."
            )
        raise ValidationError({"document_number": [message]})
