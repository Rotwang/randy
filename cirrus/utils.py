#!/usr/bin/env python
# -*- coding: utf-8 -*-

def ref(s):
        return {"Ref": s}

def join(glue, *args):
        return { "Fn::Join": [glue, args] }
