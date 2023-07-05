from rest_framework import generics, permissions, response, views
from .models import Course, Task, UserAnswer, UserCourse
from .serializers import CourseSerializer, TaskDetailSerializer, CourseDetailSerializer, LessonSerializer, \
    TaskSerializer


class CourseAPI(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseDetailAPI(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        lessons = list()
        user = self.request.user
        obj = UserCourse.objects.filter(user=user).first()
        instance = self.get_object()
        if obj and (obj.course.id == instance.id):
            data = self.get_serializer(instance).data
            for i in instance.lessons.all():
                ds = LessonSerializer(instance=i).data
                tasks = list()
                for j in i.tasks.all():
                    s = TaskSerializer(instance=j).data
                    k = j.user_answers.filter(user=user).last()
                    if k:
                        s['status'] = k.status
                    else:
                        s['status'] = None
                    tasks.append(s)
                ds['tasks'] = tasks
                lessons.append(ds)
            data['lessons'] = lessons
            return response.Response(data)
        else:
            return response.Response({'success': False, 'message': "Siz avval bu course ni sotib olishingiz zarur!"})


class TaskDetailAPI(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer


class AnswerTaskAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        code = self.request.data['code']
        task = self.request.data['task']
        UserAnswer.objects.create(user_id=self.request.user.id, task_id=task, code=code)
        return response.Response({'success': True})
