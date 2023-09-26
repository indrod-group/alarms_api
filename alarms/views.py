from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Detail, User
from .serializers import DetailSerializer, UserSerializer

class DetailViewSet(viewsets.ModelViewSet):
    queryset = Detail.objects.all()
    serializer_class = DetailSerializer

    def create(self, request, *args, **kwargs):
        imei = request.data.get('imei')
        alarm_time = request.data.get('alarm_time')
        alarm_code = request.data.get('alarm_code')

        # Verifica si ya existe un detalle con el mismo imei, alarm_time y alarm_code
        existing_detail = Detail.objects.filter(
            imei=imei,
            alarm_time=alarm_time,
            alarm_code=alarm_code
        ).first()
        if existing_detail is not None:
            # Si ya existe, retorna el detalle existente en lugar de crear uno nuevo
            serializer = self.get_serializer(existing_detail)
        else:
            # Si no existe, crea un nuevo detalle como normalmente
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        """
        Este método se utiliza para recuperar la consulta para este punto final.
        Filtra los usuarios basándose en el parámetro 'is_tracking' de la solicitud.
        """
        queryset = User.objects.all()
        is_tracking = self.request.query_params.get('is_tracking', None)
        if is_tracking is not None:
            if is_tracking.lower() == 'true':
                queryset = queryset.filter(is_tracking=True)
            elif is_tracking.lower() == 'false':
                queryset = queryset.filter(is_tracking=False)
        return queryset

    def create(self, request, *args, **kwargs):
        imei = request.data.get('imei')
        user = User.objects.filter(imei=imei).first()

        if user is not None:
            # Si el usuario ya existe, actualizamos los datos
            serializer = self.get_serializer(user, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)

        # Si el usuario no existe, creamos uno nuevo
        return super().create(request, *args, **kwargs)
