from rest_framework import permissions
import logging
# permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class IsOwnerOrReadOnly(permissions.BasePermission):

    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # raise Exception("hi")
        # print obj
        # return False
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        # return obj.owner == request.user
        return False

    def has_permission(self, request, view, obj=None):
        # print obj
        # print request
        # print objects
        # print "hi"
        # print >>sys.stderr, 'Goodbye, cruel world!'
        # raise Exception(obj)
        # print "aa"
        # logging.debug('awesome stuff dude: %s' % obj)

        return True
        # raise Exception(obj)
        return False
        # ip_addr = request.META['REMOTE_ADDR']
        # blacklisted = Blacklist.objects.filter(ip_addr=ip_addr).exists()
        # return not blacklisted
