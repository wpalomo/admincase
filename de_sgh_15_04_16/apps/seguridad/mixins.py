from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.http import urlquote
from sgh.settings.dev import LOGIN_URL


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class PermissionRequiredMixin(object):
    """
    View mixin which verifies that the logged in user has the specified
    permission.

    Class Settings
    `permission_required` - the permission to check for.
    `login_url` - the login url of site
    `redirect_field_name` - defaults to "next"
    `raise_exception` - defaults to False - raise 403 if set to True

    Example Usage

        class SomeView(PermissionRequiredMixin, ListView):
            ...
            # required
            permission_required = "app.permission"

            # optional
            login_url = "/signup/"
            redirect_field_name = "hollaback"
            raise_exception = True
            ...
    """
    login_url = LOGIN_URL
    permission_required = None
    raise_exception = False
    redirect_field_name = REDIRECT_FIELD_NAME

    def dispatch(self, request, *args, **kwargs):
        # Verify class settings
        if self.permission_required == None or len(
           self.permission_required.split(".")) != 2:
            raise ImproperlyConfigured("'PermissionRequiredMixin' requires "
                                       "'permission_required'"
                                       " attribute to be set.")

        has_permission = request.user.has_perm(self.permission_required)

        if not has_permission:
            if self.raise_exception:
                return HttpResponseForbidden()
            else:
                path = urlquote(request.get_full_path())
                tup = self.login_url, self.redirect_field_name, path
                return HttpResponseRedirect("%s?%s=%s" % tup)

        return super(PermissionRequiredMixin, self).dispatch(
            request, *args, **kwargs)