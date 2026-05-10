from rest_framework import serializers
from .models import Task, Project, Category, Comment
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ["owner"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ["owner"]

class TaskSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source="project.name", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)
    class Meta:
        model = Task
        fields = "__all__"
        extra_kwargs = {
            "project": {"required": False, "allow_null": True},
            "category": {"required": False, "allow_null": True},
        }
    def validate_project(self, value):
        request = self.context.get("request")
        if value and request and value.owner != request.user:
            raise serializers.ValidationError("Invalid project")
        return value
    def validate_category(self, value):
        request = self.context.get("request")
        if value and request and value.owner != request.user:
            raise serializers.ValidationError("Invalid category")
        return value

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"