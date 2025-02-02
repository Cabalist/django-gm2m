"""
Generic many-to-many relations descriptors
"""


class GM2MDescriptor:
    def __init__(self, field):
        self.field = field

    def __get__(self, instance, instance_type=None):
        if instance is None:
            return self
        return self.related_manager_cls(instance)

    def __set__(self, instance, value):
        if not self.through._meta.auto_created:
            opts = self.through._meta
            raise AttributeError(
                f"Cannot set values on a GM2MField which "
                f"specifies an intermediary model. "
                f"Use {opts.app_label}.{opts.object_name}'s Manager instead."
            )
        manager = self.__get__(instance)
        manager.set(value)


class RelatedGM2MDescriptor(GM2MDescriptor):
    """
    Provides a generic many-to-many descriptor for the related models to make
    the source manager available from a target model class
    """

    def __init__(self, related, remote_field):
        super().__init__(related)
        self.remote_field = remote_field

    @property
    def through(self):
        return self.remote_field.through

    @property
    def related_manager_cls(self):
        return self.remote_field.related_manager_cls


class SourceGM2MDescriptor(GM2MDescriptor):
    """
    Provides a generic many-to-many descriptor for the source model to make the
    related manager available from the source model class, and to access field
    management methods
    """

    def add_relation(self, model, on_delete=None, auto=False):
        return self.field.add_relation(model, on_delete=on_delete, auto=auto)

    def get_related_models(self, include_auto=False):
        return self.field.get_related_models(include_auto)

    @property
    def through(self):
        return self.field.remote_field.through

    @property
    def related_manager_cls(self):
        return self.field.remote_field.related_manager_cls

    def __set__(self, instance, value):
        # clear() can change expected output of 'value' queryset,
        # we force evaluation of queryset before clear; django ticket #19816
        value = tuple(value)
        super().__set__(instance, value)
