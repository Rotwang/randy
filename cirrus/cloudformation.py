#!/usr/bin/env python
# -*- coding: utf-8 -*-

import inspect
import numbers
import collections


def name(n):
        def decorate(cls):
                cls.__name__ = n
                return cls
        return decorate

class Meta(type):
        def __repr__(cls):
                return str(cls.__name__)

class CloudFormationList(list):
        __metaclass__ = Meta
        def __init__(self):
                for name, obj in sorted(inspect.getmembers(self.__class__), key=lambda t: t[0]):
                        if name in ('__class__', '__module__', '__metaclass__'):
                                continue
                        if inspect.isclass(obj):
                                self.append(obj())
                        elif isinstance(obj, (bool, basestring, collections.Sequence, dict, numbers.Number)):
                                self.append(obj)

class CloudFormationObject(dict):
        __metaclass__ = Meta
        def __init__(self):
                for name, obj in inspect.getmembers(self.__class__):
                        if name in ('__class__', '__module__', '__metaclass__'):
                                continue
                        if inspect.isclass(obj):
                                self[str(obj)] = obj()
                        elif isinstance(obj, (bool, basestring, collections.Sequence, dict, numbers.Number)):
                                self[name] = obj


class CloudFormationTemplate(CloudFormationObject):
        def __init__(self, *args, **kwargs):
                self["AWSTemplateFormatVersion"] = "2010-09-09"
                for e in args:
                        self[str(e)] = e()
                self.update(**kwargs)

