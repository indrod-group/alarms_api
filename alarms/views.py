from datetime import timedelta
from typing import Optional
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Detail, User
from .serializers import DetailSerializer, UserSerializer

class DetailViewSet(viewsets.ModelViewSet):
    queryset = Detail.objects.all()
    serializer_class = DetailSerializer

    def filter_queryset_by_alarm_code(self, request):
        alarm_codes = request.query_params.get('alarm_codes')
        if alarm_codes is not None:
            # Se convierte el parámetro en una lista separando por comas
            alarm_codes = alarm_codes.split(',')
            # Se filtra el queryset por los valores de la lista
            self.queryset = self.queryset.filter(alarm_code__in=alarm_codes)

    def filter_queryset_by_alarm_time(self, request):
        last_alarms = request.query_params.get('last_alarms', 'false') == 'true'
        if last_alarms:
            seconds = int(request.query_params.get('seconds', '120'))
            time_ago = timezone.now() - timedelta(seconds=seconds)
            time_ago_unix = int(time_ago.timestamp())
            self.queryset = self.queryset.filter(alarm_time__gte=time_ago_unix)
            return True  # Indica que se aplicó este filtro

    def filter_queryset_by_imei(self, request):
        imei = request.query_params.get('imei', None)
        if imei is not None:
            self.queryset = self.queryset.filter(imei=imei)

    def filter_queryset_by_time_range(self, request):
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time', int(timezone.now().timestamp()))
        if start_time is not None:
            self.queryset = self.queryset.filter(
                alarm_time__gte=start_time,
                alarm_time__lte=end_time
            )

    def list(self, request, *args, **kwargs):
        # Si se aplica el filtro de last_alarms, no se aplica el filtro de time_range
        if not self.filter_queryset_by_alarm_time(request):
            self.filter_queryset_by_time_range(request)
        # Se aplica el filtro de alarm_code si se especifica
        self.filter_queryset_by_alarm_code(request)
        self.filter_queryset_by_imei(request)
        return super().list(request, *args, **kwargs)

    def get_existing_detail(self, imei, alarm_time, alarm_code):
        return Detail.objects.filter(
            imei=imei,
            alarm_time=alarm_time,
            alarm_code=alarm_code
        ).first()

    def create(self, request, *args, **kwargs):
        imei = request.data.get('imei')
        alarm_time = request.data.get('alarm_time')
        alarm_code = request.data.get('alarm_code')

        existing_detail = self.get_existing_detail(imei, alarm_time, alarm_code)
        if existing_detail is not None:
            serializer = self.get_serializer(existing_detail)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_208_ALREADY_REPORTED,
                headers=headers
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # Sobrescribe el método update para no permitir modificar los datos de Details
    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # Sobrescribe el método destroy para no permitir eliminar las alarmas
    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        """
        Este método se utiliza para recuperar la consulta para este punto final.
        Filtra los usuarios basándose en el parámetro 'is_tracking' de la solicitud.
        """
        queryset = super().get_queryset()
        is_tracking: Optional[str] = self.request.query_params.get('is_tracking', None)
        if is_tracking is not None:
            if is_tracking.lower() == 'true':
                queryset = queryset.filter(is_tracking=True)
            elif is_tracking.lower() == 'false':
                queryset = queryset.filter(is_tracking=False)
        return queryset

    def create(self, request, *args, **kwargs):
        imei = request.data.get('imei')
        if imei is not None:
            user, _ = User.objects.update_or_create(
                imei=imei,
                defaults=request.data
            )
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Si el imei no existe, creamos un nuevo usuario
        return super().create(request, *args, **kwargs)

    # Implementa el método update para actualizar los datos de un usuario existente por su imei
    def update(self, request, *args, **kwargs):
        imei = request.data.get('imei')
        if imei is not None:
            user = User.objects.filter(imei=imei).first()
            if user is not None:
                # Si el usuario existe, actualizamos sus datos
                serializer = self.get_serializer(user, data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return Response(serializer.data)

        # Si el imei no existe o el usuario no existe, devolvemos un error
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # Implementa el método destroy para eliminar a un usuario por su imei
    def destroy(self, request, *args, **kwargs):
        imei = request.query_params.get('imei')
        if imei is not None:
            user = User.objects.filter(imei=imei).first()
            if user is not None:
                # Si el usuario existe, lo eliminamos
                self.perform_destroy(user)
                return Response(status=status.HTTP_204_NO_CONTENT)

        # Si el imei no existe o el usuario no existe, devolvemos un error
        return Response(status=status.HTTP_400_BAD_REQUEST)
