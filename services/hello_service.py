"""Hello world service for demonstration purposes.

This module provides a simple service that returns a greeting message.
It's useful for testing and demonstrating the endpoint configuration system.
"""

from typing import Any

from core.services.base import BaseService


class HelloService(BaseService):
    """Service that returns a simple hello world message.

    This service demonstrates the simplest possible BaseService implementation.
    It doesn't require external API calls and returns a static response
    with optional customization via parameters.

    The service accepts an optional 'name' parameter in the parameters
    dictionary. If not provided, defaults to "World".

    Examples:
        Example usage in endpoint configuration:

        ```json
        {
            "path": "/api/hello",
            "method": "GET",
            "service": "hello",
            "parameters": {
                "name": "Alice"
            }
        }
        ```

        Using the service directly:

        ```python
        service = HelloService()
        result = await service.call({"name": "Alice"})
        print(result["message"])  # "Hello, Alice!"
        await service.cleanup()
        ```
    """

    service_name = "hello"

    async def call(self, parameters: dict[str, Any] | None = None) -> dict[str, Any]:
        """Return a hello world message.

        Args:
            parameters: Optional service parameters dictionary containing:

                - name (str, optional): Name to greet. Defaults to "World".

        Returns:
            Dictionary containing a greeting message with the following structure:

            ```python
            {
                "message": str,  # e.g., "Hello, World!"
                "name": str,     # The name parameter value
                "service": str   # Service identifier
            }
            ```

        Examples:
            ```python
            service = HelloService()
            result = await service.call({"name": "Alice"})
            print(result["message"])  # "Hello, Alice!"
            await service.cleanup()
            ```
        """
        # Extract name from parameters, defaulting to "World"
        name = "World"
        if parameters and "name" in parameters:
            provided_name = str(parameters["name"]).strip()
            if provided_name:
                name = provided_name

        # Return greeting response
        return {
            "message": f"Hello, {name}!",
            "name": name,
            "service": self.service_name,
        }
