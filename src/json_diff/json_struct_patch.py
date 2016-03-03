#!/bin/env python3
#-*- coding:utf-8 -*-

import json,logging,os,elasticsearch,sys


class JsonStructPatch(object):

    def __init__(self, _template):
        self.logger = logging.getLogger("templatevalidator")
        self.template = _template

    def diff_template(self,json_doc):
        """Calculates structural diff between json_doc and json template file"""
        return self._diff_template_helper(json_doc, self.template, "", [])
    

    def _diff_template_helper(self, json_doc, template, current_path, patch):
        if not json_doc:
            return [];
        for key in json_doc.keys():
            if key in template:
                if isinstance(json_doc[key],dict):
                    if self._have_properties(key,template):
                        patch.extend(self._diff_template_helper(json_doc[key],template[key]['properties'], current_path + "." + str(key), []))
                    elif self._has_objecttype(key, template):
                        #self.logger.debug("object type detected for key %s, template %s", key, template)
                        pass
                    else:
                        patch.append( (current_path + "." + str(key), "incorrect type"))
            else:
                path = current_path + "." + str(key)
                patch.append( (path, "not_in_template"))
        return patch

    def _is_in_template_properties(self,key,template):
        """True if key is in template or in properties of the template"""
        #if key in template:
        #    return True;
        if 'properties' in template:
            if key in template['properties']:
                return True;
        return False

    def _have_properties(self, key,template):
        if not isinstance(template[key], dict):
            return False
        if 'properties' in template[key]:
            if isinstance(template[key]['properties'],dict):
                return True;
        return False

    def _has_objecttype(self, key,template):
        if not isinstance(template[key], dict):
            return False
        if template[key].get('type','') == "object":
            return True
        return False

    def print_diff(self, json_diff):
        self.logger.info("-"*80)
        if json_diff == []:
            self.logger.info("The document is fully compliant with the template")
        else:
            for (field,msg) in json_diff:
                self.logger.info("|Field: %s| Message: %s|", field, msg)
        self.logger.info("-"*80)

    def compare_series(self,json_array):
        diff = []
        for json in json_array:
            diff.extend(self.diff_template(json));
            #self.logger.debug("Current diff in series is %s", self.diff_template(json))
        return list(set(diff))
