import logging
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME

logger = logging.getLogger(__name__)

def setup_tracing(service_name: str = "service", otlp_endpoint: str = "http://jaeger:4317") -> None:
    provider = TracerProvider(
        resource=Resource.create({SERVICE_NAME: service_name})
    )
    exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)
    logger.info("Tracing is initiolized for '%s', endpoint: %s", service_name, otlp_endpoint)