from todolist.models import Task

from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    children_tasks = serializers.SerializerMethodField()

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if not rep['children_tasks']:
            rep.pop('children_tasks')
        return rep

    def get_children_tasks(self, instance):
        if instance.children_tasks:
            serializer = TaskSerializer(instance.children_tasks, many=True)
            return serializer.data
        return []

    def create(self, validated_data):
        task = Task.objects.create(**validated_data)
        return task

    def update(self, instance: Task, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.done = validated_data.get('done', instance.done)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.parent_task = validated_data.get('parent_task', instance.parent_task)
        instance.save()
        return instance
    class Meta:
        model = Task
        fields = '__all__'

