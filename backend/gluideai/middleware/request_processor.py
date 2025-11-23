from rest_framework.response import Response
from datetime import datetime
import time


class RequestProcessor:
    """
    Middleware to wrap all API responses in standardized format.
    Reference: REWRITE_SPECIFICATION.md lines 1150-1235

    Adds:
    - location: request path
    - body: original response data
    - metadata: execution_time, timestamp, status_code
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Record start time
        request.start_time = time.time()

        # Get response
        response = self.get_response(request)

        # Only process DRF responses
        if isinstance(response, Response):
            execution_time = time.time() - request.start_time

            # Wrap response if not already wrapped
            if not isinstance(response.data, dict) or 'location' not in response.data:
                wrapped_data = {
                    "location": request.path,
                    "body": response.data,
                    "metadata": {
                        "execution_time": f"{execution_time:.3f}s",
                        "timestamp": datetime.utcnow().isoformat() + '+00:00',
                        "status_code": response.status_code
                    }
                }
                response.data = wrapped_data
                response.content = response.rendered_content

        return response
