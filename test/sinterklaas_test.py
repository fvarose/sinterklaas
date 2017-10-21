#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Unit tests for sinterklaas.py """

import argparse
import mock
import sinterklaas as sk

def test_interpret_arguments_action_test():
    args = argparse.Namespace(action="test")
    assert sk.interpret_arguments(args) == True

def test_interpret_arguments_action_execute():
    with mock.patch('builtins.input', return_value='y'):
        args = argparse.Namespace(action="execute")
        assert sk.interpret_arguments(args) == False
