from __future__ import print_function, absolute_import

from ripe.atlas.cousteau import AtlasRequest

from ..streaming import Stream
from .base import Command as BaseCommand


class Command(BaseCommand):

    DESCRIPTION = "Report the results of a measurement"
    URLS = {
        "detail": "/api/v2/measurements/{}.json",
        "latest": "/api/v2/measurements/{}/latest.json",
    }

    def __init__(self, *args, **kwargs):
        BaseCommand.__init__(self, *args, **kwargs)
        self.formatter = None

    def add_arguments(self):
        self.parser.add_argument(
            "measurement_id",
            type=int,
            help="The measurement id you want streamed"
        )

    def run(self):

        pk = self.arguments.measurement_id

        detail = AtlasRequest(url_path=self.URLS["detail"].format(pk)).get()[1]

        try:
            Stream.stream(detail["type"]["name"], pk)
        except KeyboardInterrupt:
            self.ok("Disconnecting from the stream")
