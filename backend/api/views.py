from rest_framework import viewsets, status
from rest_framework.response import Response
import hashlib
import subprocess
import json
from django.conf import settings

class LandViewSet(viewsets.ViewSet):
    def create(self, request):
        try:
            name = request.data.get('name')
            address = request.data.get('address')
            coordinates = request.data.get('coordinates')
            pdf_data = request.data.get('pdf_data')
            issuer_id = request.data.get('issuer_id', None)

            # Compute PDF hash
            pdf_hash = hashlib.sha256(pdf_data.encode()).hexdigest()

            # Call Sui CLI to create land
            cmd = [
                'sui', 'client', 'call',
                '--package', settings.SUI_PACKAGE_ID,
                '--module', 'land',
                '--function', 'create_land',
                '--args', f'"{name}"', f'"{address}"', f'"{coordinates}"', f'0x{pdf_hash}',
                f'"{issuer_id}"' if issuer_id else '[]',
                settings.SUI_REGISTRY_OBJECT_ID,
                '--gas-budget', '10000000'
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            output = json.loads(result.stdout)

            return Response({
                'success': True,
                'tx_digest': output['digest'],
                'land_id': output['effects']['created'][0]['reference']['objectId']
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        try:
            land_id = pk
            name = request.data.get('name')
            address = request.data.get('address')
            coordinates = request.data.get('coordinates')
            pdf_data = request.data.get('pdf_data')
            issuer_id = request.data.get('issuer_id', None)

            # Compute PDF hash
            pdf_hash = hashlib.sha256(pdf_data.encode()).hexdigest()

            # Call Sui CLI to update land
            cmd = [
                'sui', 'client', 'call',
                '--package', settings.SUI_PACKAGE_ID,
                '--module', 'land',
                '--function', 'update_land',
                '--args', f'"{land_id}"', f'"{name}"', f'"{address}"', f'"{coordinates}"', f'0x{pdf_hash}',
                f'"{issuer_id}"' if issuer_id else '[]',
                settings.SUI_REGISTRY_OBJECT_ID,
                '--gas-budget', '10000000'
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            output = json.loads(result.stdout)

            return Response({
                'success': True,
                'tx_digest': output['digest']
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        try:
            # Call Sui CLI to get user's lands
            cmd = [
                'sui', 'client', 'call',
                '--package', settings.SUI_PACKAGE_ID,
                '--module', 'land',
                '--function', 'get_my_lands',
                '--gas-budget', '10000000'
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            output = json.loads(result.stdout)

            # Note: Fetch full land details via Sui object queries
            return Response({
                'success': True,
                'lands': output['results']
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)