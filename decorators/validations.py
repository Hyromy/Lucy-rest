from functools import wraps
from inspect import iscoroutinefunction

from rest_framework.response import Response
from rest_framework import status

def require_token(func):
    def helper(request):
        auth_header = request.headers.get('Authorization')
            
        if not auth_header:
            return Response(
                {"ok": False, "error": "Authorization header is required"},
                status = status.HTTP_401_UNAUTHORIZED
            )
            
        parts = auth_header.split()
        if len(parts) == 2 and parts[0].lower() == 'bearer':
            token = parts[1]
        else:
            token = auth_header
            
        if not token:
            return Response(
                {"ok": False, "error": "Token is required"},
                status = status.HTTP_401_UNAUTHORIZED
            )
            
        request.validated_token = token
        return None

    if iscoroutinefunction(func):
        @wraps(func)
        async def async_wrapper(self, request, *args, **kwargs):
            err_request = helper(request)
            if err_request:
                return err_request
            return await func(self, request, *args, **kwargs)
        
        return async_wrapper
    
    else:
        @wraps(func)
        def sync_wrapper(self, request, *args, **kwargs):
            err_request = helper(request)
            if err_request:
                return err_request
            return func(self, request, *args, **kwargs)
        
        return sync_wrapper
    