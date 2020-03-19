from .serializers import TaskSeriaizer, ProjectSerializer, TasksReprioritizeSerializer
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Project, Task
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import OrderingFilter


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    serializer_class = ProjectSerializer
    task_serializer_class = TaskSeriaizer
    reprioritaze_serializer_class = TasksReprioritizeSerializer

    def get_queryset(self):
        token = self.request.META.get('HTTP_AUTHORIZATION').split(' ')[1]

        user = Token.objects.get(key=token).user

        queryset = Project.objects.filter(owner=user)

        return queryset

    def get_serializer_class(self):
        if self.action == 'add_task':
            return self.task_serializer_class
        elif self.action == 'reprioritize':
            return self.reprioritaze_serializer_class
        else:
            return super(ProjectViewSet, self).get_serializer_class()

    @action(detail=True, methods=['post'])
    def add_task(self, request, pk=None):
        serializer = self.get_serializer_class()(data=request.data, context={'request': request})

        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        project = self.get_object()

        serializer.save()

        task = serializer.instance
        task.priority = len(project.tasks.all())

        task.save()

        project.tasks.add(task)

        data = self.serializer_class(instance=project, context={'request': request}).data

        self.sort_tasks(data)

        return Response(data=data, status=status.HTTP_200_OK)

    def sort_tasks(self, project):
        project['tasks'] = sorted(project['tasks'], key=lambda task: task['priority'])

    def sort_projects_tasks(self, projects):
        for project in projects:
            self.sort_tasks(project)

    def list(self, request):
        response = super(ProjectViewSet, self).list(request)

        if response.status_code != status.HTTP_200_OK:
            return response

        data = response.data

        self.sort_projects_tasks(data)

        response.data = data

        return response

    def retrieve(self, request, pk=None):
        response = super(ProjectViewSet, self).retrieve(request, pk)

        if response.status_code != status.HTTP_200_OK:
            return response

        data = response.data

        self.sort_tasks(data)

        response.data = data

        return response

    def perform_create(self, serializer):
        token = self.request.META.get('HTTP_AUTHORIZATION').split(' ')[1]

        user = Token.objects.get(key=token).user

        serializer.save(owner=user)

    @action(detail=True, methods=['post'])
    def reprioritize(self, request, pk=None):
        serializer = self.get_serializer_class()(data=self.request.data)

        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        priority = serializer.data['index']
        up = serializer.data['up']

        project = self.get_object()
        tasks = project.tasks.order_by('priority').all()

        from_task = tasks[priority]
        to_task = None

        if up and priority > 0:
            to_task = tasks[priority - 1]
        elif not up and priority < len(tasks) - 1:
            to_task = tasks[priority + 1]

        if to_task != None:
            temp = from_task.priority
            from_task.priority = to_task.priority
            to_task.priority = temp

            to_task.save()
            from_task.save()

        data = self.serializer_class(instance=project, context={'request': request}).data

        self.sort_tasks(data)

        return Response(data=data, status=status.HTTP_200_OK)

class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    serializer_class = TaskSeriaizer
    queryset = Task.objects.all()

    def destroy(self, request, pk=None):
        task = self.get_object()

        project = task.project_set.first()

        response = super(TaskViewSet, self).destroy(request, pk)

        tasks = project.tasks.order_by('priority').all()

        for index in range(len(tasks)):
            tasks[index].priority = index
            tasks[index].save()

        return response
