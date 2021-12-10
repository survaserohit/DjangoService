from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
import json
from django.utils.decorators import  method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import CartItem
# Create your views here.
# By default, Django adds a layer of protection for CSRF(Cross site request forgery attacks)
#In practice, This token is stored in our browser's cookies and is sent with every request made to the server.
# As this API will be used without a browser or cookies, the requests will never have a CSRF token.
# Therefore, we have to tell Django that this POST method does not need a CSRF token.
@method_decorator(csrf_exempt, name='dispatch')
class ShoppingCart(View):
    def post(self,request):
        data = json.loads(request.body.decode("utf-8"))
        p_name = data.get('product_name')
        p_price = data.get('product_price')
        p_quantity = data.get('product_quantity')
        
        # created a product_data dictionary to hold our fields and their values
        product_data = {
            'product_name' : p_name,
            'product_price': p_price,
            'product_quantity': p_quantity,            
            }
        # persisted a CartItem to our database, via the create() method of the Model class, filling it with our product_data
        cart_item = CartItem.objects.create(**product_data)
        
        data = {
            'message':f"New item added to the cart with item id: {cart_item.id}"}
       #Using JsonResponse class to convert our python dict into a valid Json object.      
        return JsonResponse(data,status = 201)
    
    def get(self,request):
        #count() method counts the number of occurrences in the database
        items_count = CartItem.objects.count()
        #the all() method retrieves them into a list of entities
        items = CartItem.objects.all()
        
        items_data =[]
        for item in items:
            items_data.append({
            'product_name':item.product_name,
            'product_price':item.product_price,
            'product_quantity':item.product_quantity,
        })
            
        data ={
            'item_count':items_count,
            'item':items_data,
        }    
        return JsonResponse(data,status = 201)
    
@method_decorator(csrf_exempt, name='dispatch')
class ShoppingCartUpdate(View):

    def patch(self, request, item_id):
        data = json.loads(request.body.decode("utf-8"))
        item = CartItem.objects.get(id=item_id)
        item.product_quantity = data['product_quantity']
        item.save()

        data = {
            'message': f'Item {item_id} has been updated'
        }

        return JsonResponse(data)
    def delete(self, request, item_id):
        item = CartItem.objects.get(id=item_id)
        item.delete()

        data = {
            'message': f'Item {item_id} has been deleted'
        }

        return JsonResponse(data)