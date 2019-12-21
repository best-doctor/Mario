from typing import Any, Mapping

from django.core.management.base import BaseCommand

from super_mario import BasePipeline


class PipelineForDjangoManagementCommand(BasePipeline, BaseCommand):
    def get_pipeline_kwargs(self, command_options: Mapping[str, Any]) -> Mapping[str, Any]:
        return {}

    def handle(self, *args: Any, **options: Any) -> None:
        self.run(**self.get_pipeline_kwargs(command_options=options))
