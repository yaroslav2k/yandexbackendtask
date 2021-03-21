import json

from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.http import require_http_methods

from restapi.models import Courier, Order
import restapi.helpers as helpers

class CourierView(View):
  http_method_names = ["get", "post", "patch"]

  def get(self, request, *args, **kwargs):
    courier = self.__find_courier(kwargs["id"])
    if not(courier): return HttpResponse(status=400)

    response_body = {
      "courier_id": courier.identifier,
      "courier_type": courier.category,
      "regions": courier.regions,
      "working_hours": courier.working_hours,
      "earnings": courier.earnings()
    }

    rating = courier.rating()
    if rating is not None: response_body["rating"] = rating

    return JsonResponse(response_body)

  def post(self, request, *args, **kwargs):
    parsed_request_body = json.loads(request.body)

    invalid_entries_ids = self.__validate_post_request_body(parsed_request_body)
    if len(invalid_entries_ids) > 0:
      return helpers.render_http_400(invalid_entries_ids, "couriers")

    created_entries_ids = []
    data = parsed_request_body["data"]
    for entry in data:
      courier = Courier(
        identifier=entry["courier_id"],
        category=entry["courier_type"],
        regions=entry["regions"],
        working_hours=entry["working_hours"]
      )
      courier.save()
      created_entries_ids.append(courier.identifier)

    return helpers.render_http_201(created_entries_ids, "couriers")

  def patch(self, request, *args, **kwargs):
    request_body = json.loads(request.body)

    if not self.__validate_patch_request_body(request_body): return HttpResponse(status=400)

    courier = self.__find_courier(kwargs["id"])
    if not courier: return HttpResponse(status=400)

    if "courier_type" in request_body: courier.category = request_body["courier_type"]
    if "regions" in request_body: courier.regions = request_body["regions"]
    if "working_hours" in request_body: courier.working_hours = request_body["working_hours"]
    courier.save()

    orders = Order.objects.filter(status=Order.ASSIGNED, courier=courier)
    for order in orders:
      if not(courier.order_acceptance(order)):
        order.unassign()

    return JsonResponse(courier.as_json())

  def __find_courier(self, id):
    try:
      return Courier.objects.get(identifier=id)
    except Courier.DoesNotExist:
      pass

  def __validate_post_request_body(self, request_body):
    entry_fields = ["courier_id", "courier_type", "regions", "working_hours"]
    invalid_entries_ids = []

    for entry in request_body["data"]:
      if list(entry.keys()) != entry_fields:
        invalid_entries_ids.append(entry["courier_id"])

    return invalid_entries_ids

  def __validate_patch_request_body(self, request_body):
    keys = list(request_body.keys())

    for key in keys:
      if key not in ["courier_type", "regions", "working_hours"]:
        return False

    return True
