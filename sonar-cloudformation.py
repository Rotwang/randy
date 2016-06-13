#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import inspect
import numbers
import collections
import json

def name(n):
        return lambda x: x

def fn_equals(a, b):
        def hurr(cls):
                cls.__sikret__ = lambda _: { "Fn::Equals": [ a, b ] }
                return cls
                #return lambda x: { "Fn::Equals": [ str(a), str(b) ] }
        return hurr

class Meta(type):
        def __repr__(cls):
                return 'My class %s' % cls.__name__

        def __iter__(cls):
                print dir(cls)

class Parameters(object):
        class VPCId(object):
                #__metaclass__ = Meta
                Type = "AWS::EC2::VPC::Id"
                Description = "VPC for load balancer and logstash instances."

class Mappings(object):
        class RegionMap(object):
                @name("eu-west-1")
                class eu_west_1(object):
                       AMI = "ami-4e6ffe3d"


class Conditions(object):
        __metaclass__ = Meta
        @fn_equals(Parameters.VPCId, "")
        class CreateDB(object):
                pass

class CloudFormationMu(object):
        def __iter__(self):
                for name, obj in self._iter_order(inspect.getmembers(self.__class__)):
                        if name in ('__class__', '__module__'):
                                continue
                        if inspect.isclass(obj):
                                yield self._iter_proxy(name, obj())
                        elif isinstance(obj, (bool, basestring, collections.Sequence, dict, numbers.Number)):
                                yield self._iter_proxy(name, obj)

        def _iter_proxy(self, name, obj):
                return (name, obj)

        def _iter_order(self, l):
                return l

class CloudFormationObject(CloudFormationMu):
        def __new__(cls):
                return dict(super(CloudFormationObject, cls).__new__(cls))

class CloudFormationList(CloudFormationMu):
        def __new__(cls):
                return list(super(CloudFormationList, cls).__new__(cls))

        def _iter_proxy(self, name, obj):
                return obj

        def _iter_order(self, l):
                return sorted(l, key=lambda t: t[0])


def ref(cls):
        return {"Ref": cls.__name__}

class Resources(CloudFormationObject):
        class SonarQubeSecurityGroup(CloudFormationObject):
                Type = "AWS::EC2::SecurityGroup"
                class Properties(CloudFormationObject):
                        GroupDescription = "SonarQube SecurityGroup"
                        VpcId = ref(Parameters.VPCId)
                class SecurityGroupIngress(CloudFormationList):
                        class _0(CloudFormationObject):
                                CidrIp = "abc"
                        class _1(CloudFormationObject):
                                dupa = "zbita"


class CloudFormationTemplate(object):
        pass

class AWSTemplate(CloudFormationTemplate):
        def __init__(self, classes=None, description="Hurr durr."):
                tmpl = {}
                for c in classes:
                        tmpl.update({c.__name__: c()})
                self.tmpl = tmpl


if __name__ == '__main__':
        print json.dumps(AWSTemplate(classes=[Resources], description="Descriptionsnings.").tmpl)

        #clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)

