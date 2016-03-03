#!/usr/bin/env python
#-*- coding:utf-8 -*-

import logging

from ..json_struct_patch import JsonStructPatch

def test_properties_diff():
    local = {'rsyslog': {'facility': 2}}
    template = { "rsyslog": {
                    "properties": {
                        "facility": {
                            "index": "not_analyzed",
                            "type": "string"
                        }}}}
    patch = JsonStructPatch(template)
    delta = patch.diff_template(local)
    logging.debug('delta == %s',(delta))
    assert delta == []

def test_nested_properties_diff():
    local = {'rsyslog': {'facility': {'local':1}}}
    template = { "rsyslog": {
                    "properties": {
                        "facility": {
                             "properties":{
                              "local":{
                            "index": "not_analyzed",
                            "type": "string"
                        }}}}}}
    patch = JsonStructPatch(template)
    delta = patch.diff_template(local)
    logging.debug('delta == %s',(delta))
    assert delta == []

def test_neg_properties_diff():
    local = {'rsyslog': {'facility':'sss', 'fromhost': 'openstack'}}
    template = { "rsyslog": {
                    "properties": {
                        "facility": {
                             "properties":{
                              "local":{
                            "index": "not_analyzed",
                            "type": "string"
                        }}}}}}
    patch = JsonStructPatch(template)
    delta = patch.diff_template(local)
    logging.debug('delta == %s',(delta))
    assert delta == [(".rsyslog.fromhost","not_in_template")]

def test_2array_simple_diff():
    local = {'CEE': {}, 'systemd': {}, 'rsyslog': {'facility':'ll','protocol-version':11}}
    template = {                 "CEE": {
                    "type": "object"
                }, "rsyslog":{
                     "properties": {
                        "facility": {
                            "index": "not_analyzed",
                            "type": "string"
                        }}},
                    "systemd": {
                    "properties": {
                        "k": {
                            "properties": {
                                "KERNEL_DEVICE": {
                                    "index": "not_analyzed",
                                    "type": "string"
                                }}}}}}
    patch = JsonStructPatch(template)
    delta = patch.diff_template(local)
    logging.debug('delta == %s',(delta))
    assert delta == [(".rsyslog.protocol-version","not_in_template")]

if __name__ == '__main__':
    import nose
    nose.runmodule()

