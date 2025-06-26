from .core import *
from .report import *
from .link import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    """
    API Root - provides discoverable links to all available endpoints.
    
    This endpoint serves as the entry point for API clients, providing
    hypermedia links to all available resources and operations.
    """
    return Response({
        'meta': {
            'api_version': '1.0',
            'description': 'Reporting Platform API',
            'documentation': {
                'swagger': request.build_absolute_uri(reverse('api:swagger')),
                'redoc': request.build_absolute_uri(reverse('api:redoc')),
                'schema': request.build_absolute_uri(reverse('api:schema')),
            }
        },
        'endpoints': {
            'reports': {
                'list': request.build_absolute_uri(reverse('api:report-list')),
                'metadata': f"{request.build_absolute_uri(reverse('api:report-list'))}metadata/",
                'summary': f"{request.build_absolute_uri(reverse('api:report-list'))}summary/",
                'description': 'Manage reports and their configurations'
            },
            'report_modifiers': {
                'list': request.build_absolute_uri(reverse('api:report-modifier-list')),
                'metadata': f"{request.build_absolute_uri(reverse('api:report-modifier-list'))}metadata/",
                'description': 'Manage report modifiers and date-based configurations'
            },
            'jobs': {
                'list': request.build_absolute_uri(reverse('api:job-list')),
                'metadata': f"{request.build_absolute_uri(reverse('api:job-list'))}metadata/",
                'description': 'Track and manage job executions'
            },
            'events': {
                'base_events': request.build_absolute_uri(reverse('api:event-list')),
                'ring_events': request.build_absolute_uri(reverse('api:ring-event-list')),
                'box_events': request.build_absolute_uri(reverse('api:box-event-list')),
                'geo_events': request.build_absolute_uri(reverse('api:geo-event-list')),
                'event_groups': request.build_absolute_uri(reverse('api:event-group-list')),
                'description': 'Manage different types of geographical events'
            },
            'relationships': {
                'link_single': f"{request.build_absolute_uri().rstrip('/')}link-modifier/single/",
                'link_multiple': f"{request.build_absolute_uri().rstrip('/')}link-modifier/multiple/",
                'link_summary': f"{request.build_absolute_uri().rstrip('/')}link-modifier/summary/",
                'description': 'Manage relationships between reports and modifiers'
            }
        },
        'authentication': {
            'token_obtain': request.build_absolute_uri(reverse('api:token_obtain_pair')),
            'token_refresh': request.build_absolute_uri(reverse('api:token_refresh')),
            'description': 'JWT-based authentication endpoints'
        }
    })
