from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Apenas usuarios staff (admin/operador) podem acessar."""

    def test_func(self):
        return self.request.user.is_staff
