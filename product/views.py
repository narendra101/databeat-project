from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from register.views import authenticate
from .serializers import ProductSerializer
from .models import ProductModel
# Create your views here.


class CreateProductView(APIView):
    def post(self, *args, **kwargs):
        logged_in, user = authenticate(self.request)
        self.request.data.update({'user': user.id})        
        if logged_in:
            serializer = ProductSerializer(data=self.request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'success', 'data': self.request.data}, status.HTTP_201_CREATED)
            errors = {}            
            for error in serializer.errors:                
                errors[error] = serializer.errors.get(error)
                for i in range(len(errors[error])):
                    errors[error][i] = errors[error][i].replace(' model', '')
                    
            return Response({'status': 'failed', 'errors': errors}, status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': 'failed', 'message': 'user not loggedin'}, status.HTTP_200_OK)


class DeleteProductView(APIView):
    def delete(self, *args, **kwargs):
        logged_in, user = authenticate(self.request)
        if logged_in:
            id = kwargs.get('id');
            ProductModel.objects.get(id=id).delete()
            return Response({'status': 'success'}, status.HTTP_200_OK)
        else:
            return Response({'status': 'failed delete'}, status.HTTP_200_OK)

class GetAllProductView(APIView):
    def get(self, *args, **kwargs):
        try:
            logged_in, user = authenticate(self.request)
            if logged_in:
                products_objects = user.productmodel_set.all()                
                products = list()
                for product_object in products_objects:                                 
                    products.append({
                        'id': product_object.id,
                        'product_name': product_object.product_name,
                        'quantity': product_object.quantity,
                        'price': product_object.price,
                    })
                return Response({'status': 'success', 'products': products}, status.HTTP_200_OK)
            else:
                return Response({'status': 'failed', 'message': 'Authentication failed'}, status.HTTP_200_OK)
        except Exception as exc:
            print(exc)
            return Response({'status': 'failed', 'message': 'Something went wrong'}, status.HTTP_200_OK)

        
