#!/usr/bin/env python
#-*- coding:utf-8 -*-

import logging

from ..json_struct_patch import JsonStructPatch

def test_2el_diff():
    local = [{'rsyslog': {'facility': 2}},{}]
    template = { "rsyslog": {
                    "properties": {
                        "facility": {
                            "index": "not_analyzed",
                            "type": "string"
                        }}}}
    patch = JsonStructPatch(template)
    delta = patch.compare_series(local)
    logging.debug('delta == %s',(delta))
    assert delta == []

def test_2el_simple_diff():
    local = [{'rsyslog': 'd'}, {'lopata': 11}]
    template = { "rsyslog": 32 }
    patch = JsonStructPatch(template)
    delta = patch.compare_series(local)
    logging.debug('delta == %s',(delta))
    assert delta == [(".lopata","not_in_template")]

def test_2el_properties_diff():
    local = [{'rsyslog': {'facility': {'local':1}}},{'rsyslog': {'facility': {'local':1, 'round': {} }}}]
    template = { "rsyslog": {
                    "properties": {
                        "facility": {
                             "properties":{
                              "local":{
                            "index": "not_analyzed",
                            "type": "string"
                        }}}}}}
    patch = JsonStructPatch(template)
    delta = patch.compare_series(local)
    logging.debug('delta == %s',(delta))
    assert delta == [(".rsyslog.facility.round", "not_in_template")]

def test_emptyarray_simple_diff():
    local = [{'CEE': {}, 'systemd': {}}, {'rsyslog': 11}]
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
    delta = patch.compare_series(local)
    logging.debug('delta == %s',(delta))
    assert delta == []

def test_2array_simple_diff():
    local = [{'CEE': {}, 'systemd': {}}, {'rsyslog': 11},{'CEE': {}, 'systemd': {}, 'rsyslog': {'facility':'ll','protocol-version':11}}]
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
    delta = patch.compare_series(local)
    logging.debug('delta == %s',(delta))
    assert delta == [(".rsyslog.protocol-version","not_in_template")]

if __name__ == '__main__':
    import nose
    nose.runmodule()

