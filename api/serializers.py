from rest_framework import serializers
from .models import Task, Project, Category, Comment

# project
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"

# category
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

# task
class TaskSerializer(serializers.ModelSerializer):

    project_name = serializers.CharField(source="project.name", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Task
        fields = "__all__"

    def validate_project(self, value):
        if value and value.owner != self.context["request"].user:
            raise serializers.ValidationError("Invalid project")
        return value

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"