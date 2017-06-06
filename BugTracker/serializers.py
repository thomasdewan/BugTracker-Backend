from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Comment,Issue,State

class UserSerializer(serializers.ModelSerializer):
    issue = serializers.PrimaryKeyRelatedField(many=True, queryset=Issue.objects.all())
    comment = serializers.PrimaryKeyRelatedField(many=True, queryset=Comment.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name','last_name', 'issue', 'comment')
        
class IssueSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model=Issue
        fields = ('id','owner','name','description','creationDate','state',)
        
    def create(self, validated_data):
        return Issue.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.owner = validated_data.get('owner', instance.owner)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.state = validated_data.get('state',instance.state)
        instance.save()
        return instance

class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model=Comment
        fields = ('id','owner','comment','issue','creationDate')
        
    def create(self, validated_data):
        return Comment.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.owner = validated_data.get('owner', instance.owner)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.issue = validated_data.get('issue', instance.issue)
        instance.save()
        return instance
        
class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model=State
        fields = ('id','name')
    
    def create(self, validated_data):
        return State.objects.create(**validated_data)