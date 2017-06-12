from BugTracker.models import Issue,Comment,State
from BugTracker.serializers import IssueSerializer,CommentSerializer,StateSerializer,UserSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions
from .permissions import IsOwnerOrReadOnly,ReadOnly

class IssueList(generics.ListCreateAPIView):
    queryset = Issue.objects.all().order_by('-creationDate')
    serializer_class = IssueSerializer
    permission_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly,)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class IssueDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly,)
    
    def patch(self, request, *args, **kwargs):
        closedStateId = State.objects.get(name='Closed').id
        if 'state' in request.data:
            if request.data['state'] == str(closedStateId):
                print("Send Emails To EveryBody")
        return self.partial_update(request, *args, **kwargs)
    
class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly,)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly,)
    
    
class CommentForIssueList(APIView):
    permission_classes = (permissions.IsAuthenticated,ReadOnly)

    def get(self, request, pk):
        queryset = Comment.objects.filter(issue=pk)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)
    

class StateList(generics.ListAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = (permissions.IsAdminUser,)
    
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
class UserRegister(generics.CreateAPIView):
    model = User
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = UserSerializer