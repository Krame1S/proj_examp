import logging

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.asyncpg import AsyncPGInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)


def setup_tracing(service_name: str = "my-backend", otlp_endpoint: str = "http://jaeger:4317") -> None:
    """Инициализируем трейсинг через OpenTelemetry → Jaeger.

    Вызывается один раз при старте приложения.
    otlp_endpoint — адрес Jaeger внутри Docker-сети (jaeger:4317).
    """
    provider = TracerProvider()

    # OTLPSpanExporter отправляет спаны в Jaeger по протоколу gRPC (OTLP).
    # Jaeger слушает на порту 4317 внутри Docker-сети.
    exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
    provider.add_span_processor(BatchSpanProcessor(exporter))

    trace.set_tracer_provider(provider)

    # Автоматически инструментирует все asyncpg-запросы — изменения в pool.py не нужны.
    AsyncPGInstrumentor().instrument()

    logger.info("Tracing инициализирован для сервиса '%s', endpoint: %s", service_name, otlp_endpoint)


class TracingMiddleware(BaseHTTPMiddleware):
    """Оборачивает каждый HTTP-запрос в OpenTelemetry span.

    Span — это единица трейса: запись о том, что произошло, когда и сколько длилось.
    В Jaeger UI ты увидишь их в виде временной шкалы для каждого запроса.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        # Имя спана: например "GET /api/v1/tasks"
        span_name = f"{request.method} {request.url.path}"

        with tracer.start_as_current_span(span_name) as span:
            # Добавляем атрибуты — метаданные, которые видны в Jaeger UI
            span.set_attribute("http.method", request.method)
            span.set_attribute("http.url", str(request.url))
            span.set_attribute("http.route", request.url.path)

            response: Response = await call_next(request)

            span.set_attribute("http.status_code", response.status_code)

            # Если сервер вернул 5xx — помечаем спан как ошибочный
            if response.status_code >= 500:
                span.set_status(trace.StatusCode.ERROR)

            return response