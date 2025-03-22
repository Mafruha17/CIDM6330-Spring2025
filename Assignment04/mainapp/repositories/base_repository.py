from abc import ABC, abstractmethod
from django.shortcuts import get_object_or_404


class BaseRepository(ABC):
    @classmethod
    @abstractmethod
    def get_model(cls):
        """Each subclass must return its model class"""
        raise NotImplementedError("Subclasses must implement get_model()")

    @classmethod
    def get_all(cls):
        return cls.get_model().objects.all()

    @classmethod
    def get_by_id(cls, object_id):
        return get_object_or_404(cls.get_model(), id=object_id)

    @classmethod
    def create(cls, data):
        return cls.get_model().objects.create(**data)

    @classmethod
    def update(cls, instance, data):
        for field, value in data.items():
            setattr(instance, field, value)
        instance.save()
        return instance

    @classmethod
    def delete(cls, instance):
        instance.delete()
