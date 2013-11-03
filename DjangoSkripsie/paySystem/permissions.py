"""
Provides a set of pluggable permission policies.
"""
from __future__ import unicode_literals
import inspect
import warnings

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']

class BasePermission(object):
    """
    A base class from which all permission classes should inherit.
    """

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if len(inspect.getargspec(self.has_permission).args) == 4:
            warnings.warn(
                'The `obj` argument in `has_permission` is deprecated. '
                'Use `has_object_permission()` instead for object permissions.',
                DeprecationWarning, stacklevel=2
            )
            return self.has_permission(request, view, obj)
        return True

class IsVendor(BasePermission):
	"""
	Allows access only to vendor users.
	"""

	def has_permission(self, request, view):
		if request.user.is_authenticated:
			if request.method == "GET":
				return True
		
			else:
				if(request.user.is_staff):
					return True
				if(request.user.groups.filter(name="Vendor").count() != 0):
					return True
        
		return False
