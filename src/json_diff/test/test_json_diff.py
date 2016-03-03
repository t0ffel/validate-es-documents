#!/usr/bin/env python
#-*- coding:utf-8 -*-

import logging

from ..json_struct_patch import JsonStructPatch

def test_1elem_diff():
    local = {'foo': 1, 'bar': 2}
    template = {'foo': 2, 'baz': 3}
    patch = JsonStructPatch(template)
    delta = patch.diff_template(local)
    logging.debug('delta == %s',(delta))
    assert delta == [ ('.bar',"not_in_template")]

def test_2elem_diff():
    local = {'foo': 1, 'bar': 2}
    template = {'fou': 2, 'baz': 3}
    patch = JsonStructPatch(template)
    delta = patch.diff_template(local)
    logging.debug('delta == %s',(delta))
    assert sorted(delta) == sorted([ ('.foo', "not_in_template"),('.bar',"not_in_template")])

def test_empty_diff():
    local = {}
    template = {'foo': 2, 'baz': 3}
    patch = JsonStructPatch(template)
    delta = patch.diff_template(local)
    logging.debug('delta == %s',(delta))
    assert delta == []

def test_eq_1elem_diff():
    local = {'foo': 1, 'bar': 2}
    template = {'foo': 2, 'bar': 3}
    patch = JsonStructPatch(template)
    delta = patch.diff_template(local)
    logging.debug('delta == %s',(delta))
    assert delta == []

def test_type_1nest_diff():
    local = {'foo': { 'foo':'foo'}, 'bar': 2}
    template = {'foo': 2, 'bar': 3}
    patch = JsonStructPatch(template)
    delta = patch.diff_template(local)
    logging.debug('delta == %s',(delta))
    assert delta == [ ('.foo',"incorrect type")]

def test_eq_1nest_diff():
    local = {'foo': { 'foo':'foo'}}
    template = {'foo': {'properties':{'foo':'bar'}}}
    patch = JsonStructPatch(template)
    delta = patch.diff_template(local)
    logging.debug('delta == %s',(delta))
    assert delta == []

def test_neq_1nest_diff():
    local = {'foo': { 'foo':'foo', 'bar':33}}
    template = {'foo': {'properties':{'foo':'bar'}}}
    patch = JsonStructPatch(template)
    delta = patch.diff_template(local)
    logging.debug('delta == %s',(delta))
    assert delta == [('.foo.bar',"not_in_template")]

def test_eq_2nest_diff():
    local = {'foo': { 'foo': {'bar': 44}}}
    template = {'foo': {'properties':{'foo':{'properties':{'bar':443, 'foo_b':'foo'}}}}}
    patch = JsonStructPatch(template)
    delta = patch.diff_template(local)
    logging.debug('delta == %s',(delta))
    assert delta == []

def test_neq_2nest_diff():
    local = {'foo': { 'foo': {'bar': 44, '3rd_level_bar': 555}}}
    template = {'foo': {'properties': {'foo':{'properties':{'bar':443, 'foo_b':'foo'}}}}}
    patch = JsonStructPatch(template)
    delta = patch.diff_template(local)
    logging.debug('delta == %s',(delta))
    assert sorted(delta) == sorted([('.foo.foo.3rd_level_bar', "not_in_template")])

def test_combined_2nest_diff():
    local = {'foo': { 'foo': {'bar': 44, '3rd_level_bar': 555}, '2nd_level_foo': 66}}
    template = {'foo': {'properties':{'foo':{'properties':{'bar':443, 'foo_b':'foo'}}}}}
    patch = JsonStructPatch(template)
    delta = patch.diff_template(local)
    logging.debug('delta == %s',(delta))
    assert sorted(delta) == sorted([('.foo.2nd_level_foo',"not_in_template"),('.foo.foo.3rd_level_bar', "not_in_template")])


if __name__ == '__main__':
    import nose
    nose.runmodule()

