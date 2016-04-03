# local imports
from nautilus.conventions.services import api_gateway_name
from nautilus.network.amqp.actionHandlers import noop_handler
from .service import Service

class APIGateway(Service):
    """
        This provides a single endpoint that other services and clients can
        use to query the cloud without worrying about the distributed nature
        of the system.

        Args:
            schema (graphql.core.type.GraphQLSchema): The schema to use that
                encapsultes the overall topology of the cloud.

            action_handler (optional, function): The callback function fired
                when an action is recieved. If None, the service does not
                connect to the action queue.

        Example:

            .. code-block:: python

                # external imports
                from nautilus import APIGateway
                # local imports
                from .schema import schema

                # create a nautilus service with just the schema
                service = APIGateway(schema=schema)

    """

    def __init__(self, **kwargs):
        # create the service
        super().__init__(
            name=kwargs.pop('name', None) or api_gateway_name(),
            **kwargs
        )
