"""
Django Views
"""
from django.views.generic import TemplateView
from reactor import Component


class IndexView(TemplateView):
    template_name = "live_view/index.html"


class XCounter(Component):

    _amount = None  # Counter Value

    @property
    def amount(self):
        return self._amount

    # reference the template from above
    template_name = 'live_view/x_counter.html'

    # A component is instantiated during normal rendering and when the component
    # connects from the front-end. Then  __init__ is called passing `context` of
    # creation (in case of HTML  rendering is the context of the template, in
    # case of a WebSocket connection is the scope of django channels) Also the
    # `id` is passed if any is provided, otherwise a `uuid4` is  generated on
    # the fly.

    # This method is called after __init__ passing the initial state of the
    # Component, this method is responsible taking the state of the component
    # and construct or reconstruct the component. Sometimes loading things from
    # the database like tests of this project.
    def mount(self, amount=0, **kwargs):
        self._amount = amount

    # This method is used to capture the essence of the state of a component
    # state, so it can be reconstructed at any given time on the future.
    # By passing what ever is returned by this method to `mount`.
    def serialize(self):
        return dict(id=self.id, amount=self._amount)

    # This are the event handlers they always start with `receive_`

    def receive_inc(self, **kwargs):
        self._amount += 1

    def receive_dec(self, **kwargs):
        self._amount -= 1

    def receive_set_to(self, amount, **kwargs):
        self._amount = amount
