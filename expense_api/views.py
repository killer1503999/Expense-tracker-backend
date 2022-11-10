from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
from .serializers import *
from .models import *
from rest_framework import status
from django.http import Http404

from hashlib import new
from pathlib import Path
import mimetypes
from .azure_file_controller import ALLOWED_EXTENTIONS, download_blob, upload_file_to_blob, delete_blob_client
from .queues import sendMessage


class userDetailsList(APIView):
    def get(self, request):

        new_obj = userDetails.objects.all()
        serialzer = userDetailsserializers(new_obj, many=True)
        return Response(serialzer.data)

    def get_object(self, pk):
        try:
            return userDetails.objects.get(pk=pk)
        except userDetails.DoesNotExist:
            raise Http404

    def delete(self, request, pk):

        data_delete = self.get_object(pk)
        try:
            data_delete.delete()
            return Response({"message": "deleted"})
        except:
            return Response({"message": "no"})

    def post(self, request):

        data = request.data
        serializer = userDetailsserializers(data=data)

        if serializer.is_valid():
            try:
                serializer.save()
                return Response({'message': 'succesful'})
            except:
                return Response({"message": "factory not present"})

        return Response(serializer._errors)


class expenseDetailsList(APIView):
    def get(self, request, pk):
        new_obj = expenseDetails.objects.all()
        serializer = expenseDetailsserializers(new_obj, many=True)

        try:
            dummy = []
            for keys in serializer.data:
                if keys["userDetail"] == pk:
                    dummy.append(keys)
            return Response({'message': dummy})
        except:
            return Response({"message": "not found"})

    def post(self, request, pk):

        data = request.data
        print(request.data)
        serializer = expenseDetailsserializers(data=data)

        if serializer.is_valid():
            print(8698)

            try:
                new_obj = userDetails.objects.get(pk=pk)
                print("request.data")

                if request.data['recieptImage'] != '' or request.data['recieptImage']:
                    print(2)

                    file = request.FILES['recieptImage']
                    print(3)

                    new_file = upload_file_to_blob(file)
                    print(4)

                  #   data.recieptImage.name = new_file

                    request.data['recieptImage'].name = new_file
                print("test2")

                serialzernew = userDetailsserializers(new_obj, many=False)

                keys = serialzernew.data
                print(request.data['date'])

                if keys["userId"] == pk:
                    reg = expenseDetails(expenseCategory=request.data['expenseCategory'], amount=request.data['amount'],
                                         comments=request.data['comments'], recieptImage=request.data['recieptImage'], userDetail=userDetails(
                        pk), date=request.data['date'])

                    reg.save()
                    latest_obj_id = str(expenseDetails.objects.latest('id').id)
                    print(keys, latest_obj_id)
                    print("checked lated")

                    sendMessage(latest_obj_id)
                    return Response({'message': 'succesful'})
            except:
                print("test failed")
                return Response({"message": "factory not present"})

        return Response(serializer._errors)


class expenseDetailsDetails(APIView):
    def get_object(self, pk):
        try:
            return expenseDetails.objects.get(pk=pk)
        except expenseDetails.DoesNotExist:
            raise Http404

    def get(self, request, pk, id):
        new_obj = expenseDetails.objects.all()
        serializer = expenseDetailsserializers(new_obj, many=True)

        a = []

        for keys in serializer.data:
            if keys["userDetail"] == pk and keys["id"] == int(id):
                a.append(keys)
        if a != []:
            return Response({'message': a})
        return Response({"message": "Product not found"})

    def put(self, request, pk, id):

        data = self.get_object(id)
        new_obj = expenseDetails.objects.get(pk=id)
        serializers = expenseDetailsserializers(new_obj, many=False)

        a = serializers.data
        print(request.data)
        print(a)

        serializer = expenseDetailsserializers(data, data=request.data)

        if serializer.is_valid():

            try:

                if request.data['recieptImage']:
                    file = request.FILES['recieptImage']
                    new_file = upload_file_to_blob(file)
                    request.data['recieptImage'].name = new_file
            #     else:
            #         request.data['recieptImage'].name = a['recieptImage']
                    print(serializer.data)
                    reg = expenseDetails(id=id, expenseCategory=request.data['expenseCategory'], amount=request.data['amount'],
                                         comments=request.data['comments'], recieptImage=request.data['recieptImage'], userDetail=userDetails(
                        pk), date=request.data['date'])
                else:
                    reg = expenseDetails(id=id, expenseCategory=request.data['expenseCategory'], amount=request.data['amount'],
                                         comments=request.data['comments'], recieptImage=a['recieptImage'], userDetail=userDetails(
                        pk), date=request.data['date'])

                print("try block ran`")
                reg.save()
            #     else:
            #        reg = expenseDetails(id=id, expenseCategory=request.data['expenseCategory'], amount=request.data['amount'],
            #                              comments=request.data['comments'], recieptImage=request.data['recieptImage'], userDetail=userDetails(
            #             pk), date=request.data['date'])

            except:
                reg = expenseDetails(id=id, expenseCategory=request.data['expenseCategory'], amount=request.data['amount'],
                                     comments=request.data['comments'], userDetail=userDetails(
                    pk), date=request.data['date'])
                print("except block ran`")

                reg.save()
            sendMessage(id)

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, id):
        try:
            new_obj = userDetails.objects.get(pk=pk)
            serialzernew = userDetailsserializers(new_obj, many=False)

            data = self.get_object(id)
            productserializer = expenseDetailsserializers(data, many=False)

            if serialzernew.data["userId"] == productserializer.data["userDetail"]:

                data.delete()
                print(data.recieptImage.name)
                check = delete_blob_client(str(data.recieptImage.name))
                print(check)
                return Response({"message": "deleted"})
            return Response({"message": "id requested not in factory"})
        except:
            return Response({"message": "id requested not in factory12"})


class approversAccess(APIView):
    def get_object(self, pk):
        try:
            return expenseDetails.objects.get(pk=pk)
        except expenseDetails.DoesNotExist:
            raise Http404

    def put(self, request, pk, id):

        data = self.get_object(id)
        new_obj = expenseDetails.objects.get(pk=id)
        serializers = expenseDetailsserializers(new_obj, many=False)

        a = serializers.data
        print(request.data)
        print(a)

        serializer = expenseDetailsserializers(data, data=request.data)
        print(serializer.is_valid())

        if serializer.is_valid():

            try:

                if request.data['recieptImage']:

                    #     else:
                    #         request.data['recieptImage'].name = a['recieptImage']
                    print(serializer.data)
                    reg = expenseDetails(id=id, expenseCategory=request.data['expenseCategory'], amount=request.data['amount'],
                                         comments=request.data['comments'], recieptImage=a['recieptImage'], userDetail=userDetails(
                        pk), date=request.data['date'], approvedStatus=request.data['approvedStatus'])
                else:
                    print("else ran")
                    print(request.data)
                    print(request.data['approversComments'])
                    reg = expenseDetails(id=id, expenseCategory=request.data['expenseCategory'], amount=request.data['amount'],
                                         comments=request.data['comments'], recieptImage=request.data['recieptImage'], userDetail=userDetails(
                        pk), date=request.data['date'], approvedStatus=request.data['approvedStatus'], approversComments=request.data['approversComments'],)

                print("try block ran`")
                print(reg.approversComments)
                reg.save()

            #     else:
            #        reg = expenseDetails(id=id, expenseCategory=request.data['expenseCategory'], amount=request.data['amount'],
            #                              comments=request.data['comments'], recieptImage=request.data['recieptImage'], userDetail=userDetails(
            #             pk), date=request.data['date'])

            except:
                reg = expenseDetails(id=id, expenseCategory=request.data['expenseCategory'], amount=request.data['amount'],
                                     comments=request.data['comments'], recieptImage=request.data['recieptImage'], userDetail=userDetails(
                    pk), date=request.data['date'], approvedStatus=request.data['approvedStatus'])
                print("except block ran`")

                reg.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        new_obj = expenseDetails.objects.all()
        serializer = expenseDetailsserializers(new_obj, many=True)

        try:
            dummy = []
            for keys in serializer.data:
                print(keys)
                if keys["userDetail"] == pk and keys["approvedStatus"] == "Pending" and keys["approversComments"] == "RequiresApproval":
                    dummy.append(keys)
            return Response({'message': dummy})
        except:
            return Response({"message": "not found"})
