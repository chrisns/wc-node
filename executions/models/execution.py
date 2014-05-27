#!/usr/bin/env python
"""Execution model"""

from picklefield.fields import PickledObjectField
from django.db import models


class Execution(models.Model):
    owner = models.IntegerField()
    data = PickledObjectField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)
