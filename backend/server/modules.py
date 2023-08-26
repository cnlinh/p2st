import logging

from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Module, Topic

logger = logging.getLogger(__name__)


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ["id", "code"]


class TopicSerializer(serializers.ModelSerializer):
    module = ModuleSerializer()

    class Meta:
        model = Topic
        fields = ["id", "module", "name"]


class TopicView(APIView):
    def get(self, request):
        try:
            module_code = request.query_params.get("module")
            if module_code:
                module = Module.objects.get(code__iexact=module_code)
                topics = Topic.objects.filter(module=module)
            else:
                topics = Topic.objects.all()

            serializer = TopicSerializer(topics, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Module.DoesNotExist:
            return Response([], status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e)
            return Response(
                {"error": "Internal server error."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
