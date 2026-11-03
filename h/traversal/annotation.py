from dataclasses import dataclass

from h.models import Annotation
from h.services.annotation_read import AnnotationReadService


@dataclass
class AnnotationContext:
    """Context for annotation-based views."""

    annotation: Annotation

    admin_delete_enabled: bool = False
    """Whether the `admin_annotation_delete` feature flag is on for the user."""

    @property
    def group(self):
        return self.annotation.group


class AnnotationRoot:
    """Root factory for routes whose context is an `AnnotationContext`."""

    def __init__(self, request) -> None:
        self._request = request
        self._annotation_read_service: AnnotationReadService = request.find_service(
            AnnotationReadService
        )

    def __getitem__(self, annotation_id):
        annotation = self._annotation_read_service.get_annotation_by_id(annotation_id)
        if annotation is None:
            raise KeyError

        return AnnotationContext(
            annotation,
            admin_delete_enabled=self._request.feature("admin_annotation_delete"),
        )
