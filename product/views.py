from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer, SurveySerializer, DiscountItemSerializer
from .models import Product, Survey, DiscountItem
from rest_framework import status
from datetime import date, datetime
import segno
import io
from django.core.files.base import ContentFile

WEEKDAY = {
    'MONDAY': 0,
    'TUESDAY': 1,
    'WEDNESDAY': 2,
    'THURSDAY': 3,
    'FRIDAY': 4,
    'SATURDAY': 5,
    'SUNDAY': 6,
}


@api_view()
def survey_list(request):

    if request.method != 'GET':
        content = {'Invalid request': 'nothing to see here'}
        return Response(content, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    items = list()
    items.extend(Survey.objects.all())
    serializer = SurveySerializer(items, many=True)

    return Response(serializer.data)


@api_view(['POST'])
def survey(request):

    if request.method != 'POST':
        content = {'Invalid request': 'nothing to see here'}
        return Response(content, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    serializer = SurveySerializer(data=request.data)
    print(serializer)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view()
def coupon_check(request, item_pk):

    if request.method != 'GET':
        content = {'Invalid request': 'nothing to see here'}
        return Response(content, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        item = DiscountItem.objects.get(pk=item_pk)
        item.delete()
        return Response("Successful execution!")
    except DiscountItem.DoesNotExist:
        content = {'No content': 'nothing to see here'}
        return Response(content, status=status.HTTP_204_NO_CONTENT)


@api_view()
def coupon_list(request):

    if request.method != 'GET':
        content = {'Invalid request': 'nothing to see here'}
        return Response(content, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    item = DiscountItem.objects.all()
    serializer = DiscountItemSerializer(item, many=True)

    return Response(serializer.data)

@api_view()
def coupon(request, item_pk):

    if request.method != 'GET':
        content = {'Invalid request': 'nothing to see here'}
        return Response(content, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        item = Product.objects.get(pk=item_pk)
        item.quantity -= 1
        item.save()

        discounted_item = DiscountItem(
            name=item.name,
            price=str(format(float(item.price) * (float((100 - item.discount) / 100)), '.2f')),
            quantity=1
            )
        discounted_item.save()

        qr = segno.make_qr(str(discounted_item.pk))
        buff = io.BytesIO()
        qr.save(buff, kind='png', scale=3, dark='darkblue')
        discounted_item.image.save(discounted_item.name + '.jpg', ContentFile(buff.getvalue()), save=True)
        discounted_item.save()
        item = DiscountItem.objects.filter(pk=discounted_item.pk)
        serializer = DiscountItemSerializer(item, many=True)

        return Response(serializer.data)
    except Product.DoesNotExsist:
        content = {'No content': 'nothing to see here'}
        return Response(content, status=status.HTTP_204_NO_CONTENT)

@api_view()
def list_items(request):

    if request.method != 'GET':
        content = {'Invalid request': 'nothing to see here'}
        return Response(content, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    items = list()
    items.extend(Product.objects.all())

    serializer = ProductSerializer(items, many=True)

    return Response(serializer.data)


@api_view()
def result(request):

    if request.method != 'GET':
        content = {'Invalid request': 'nothing to see here'}
        return Response(content, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    current_time = datetime.now().time()
    items = list()
    discount_list = list()

    if request.GET.get('Bakery'):
        items.extend(Product.objects.filter(section='Bakery'))

    if request.GET.get('Drink'):
        items.extend(Product.objects.filter(section='Drink'))

    if request.GET.get('Candy'):
        items.extend(Product.objects.filter(section='Candy'))

    for item in items:
        if item.monday and (date.today().weekday() == WEEKDAY['MONDAY']):
            if (item.discountTimeStart <= current_time) and (item.discountTimeEnd >= current_time):
                discount_list.append(item)
            elif (item.discountTimeEnd < current_time) and (not item.repeat_discount):
                item.monday = False

        if item.tuesday and (date.today().weekday() == WEEKDAY['TUESDAY']):
            if (item.discountTimeStart <= current_time) and (item.discountTimeEnd >= current_time):
                discount_list.append(item)
            elif (item.discountTimeEnd < current_time) and (not item.repeat_discount):
                item.tuesday = False

        if item.wednesday and (date.today().weekday() == WEEKDAY['WEDNESDAY']):
            if (item.discountTimeStart <= current_time) and (item.discountTimeEnd >= current_time):
                discount_list.append(item)
            elif (item.discountTimeEnd < current_time) and (not item.repeat_discount):
                item.wednesday = False

        if item.thursday and (date.today().weekday() == WEEKDAY['THURSDAY']):
            if (item.discountTimeStart <= current_time) and (item.discountTimeEnd >= current_time):
                discount_list.append(item)
            elif (item.discountTimeEnd < current_time) and (not item.repeat_discount):
                item.thursday = False

        if item.friday and (date.today().weekday() == WEEKDAY['FRIDAY']):
            if (item.discountTimeStart <= current_time) and (item.discountTimeEnd >= current_time):
                discount_list.append(item)
            elif (item.discountTimeEnd < current_time) and (not item.repeat_discount):
                item.friday = False

        if item.saturday and (date.today().weekday() == WEEKDAY['SATURDAY']):
            if (item.discountTimeStart <= current_time) and (item.discountTimeEnd >= current_time):
                discount_list.append(item)
            elif (item.discountTimeEnd < current_time) and (not item.repeat_discount):
                item.saturday = False

        if item.sunday and (date.today().weekday() == WEEKDAY['SUNDAY']):
            if (item.discountTimeStart <= current_time) and (item.discountTimeEnd >= current_time):
                discount_list.append(item)
            elif (item.discountTimeEnd < current_time) and (not item.repeat_discount):
                item.sunday = False

    serializer = ProductSerializer(discount_list, many=True)

    return Response(serializer.data)




