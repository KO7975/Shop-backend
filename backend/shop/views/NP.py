import os
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from novaposhta import NovaPoshtaApi 
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiExample
    )


np = NovaPoshtaApi(api_key=os.getenv("NOVA_POSHTA_API_KEY"))
   

class NPAreas(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
            description='Get areass',
            responses={
                200:OpenApiResponse(description='Get full information about available areas')
            }
    )
    def get(self, request):
        areas = np.address.get_areas().json()

        return Response(areas)
    

class NPCity(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
            description='Get city inform from city name',
            parameters=[
                OpenApiParameter(
                    name='city',
                    type=dict,
                    examples=[
                    OpenApiExample('city', value={'city': 'str'})
                    ]
                )
            ],
            responses={
                200:OpenApiResponse(description='return city data for current city')
            }            
    )
    def get(self, request):
        city_name = request.data['city']
        city = np.address.search_settlements(city_name=city_name, limit=10).json()

        return Response(city)
    

class NPWarehouses(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
            description='Get warehouses inform from city name',
            parameters=[
                OpenApiParameter(
                    name='city',
                    type=dict,
                    examples=[
                    OpenApiExample('city', value={'city': 'str'}, request_only=True)
                    ],
                )
            ],
            responses={
                200:OpenApiResponse(description='return warehouses data for current city')
            }
    )
    def get(self, request):
        city_name = request.data['city']
        warehouses = np.address.get_warehouses(city_name=city_name).json()

        return Response(warehouses)
