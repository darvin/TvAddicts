# -*- coding: utf-8 -*-
from google.appengine.ext import db
from appengine_admin.encoding import encoded_str_utf8

# Models
class Utf8ReferencedModel(db.Model):
    name = db.StringProperty("Name", required = True)
    whencreated = db.DateTimeProperty("Created", auto_now_add = True)
    whenupdated = db.DateTimeProperty("Updated", auto_now = True)

    @encoded_str_utf8
    def __str__(self):
        return self.__unicode__()
        
    def __unicode__(self):
        return u"Glāžšķūņu rūķīši %s" % self.name

class Utf8TestModel(db.Model):
    stringField = db.StringProperty("String field")
    textField = db.TextProperty("Text field")
    integerField = db.IntegerProperty("Integer field", default = 0)
    booleanField = db.BooleanProperty("Boolean field")
    referenceField = db.ReferenceProperty(Utf8ReferencedModel, verbose_name = "Foreign key field")
    whencreated = db.DateTimeProperty("Created", auto_now_add = True)
    whenupdated = db.DateTimeProperty("Updated", auto_now = True)

    def testMethod(self):
        return u'STR: %s' % self.stringField
    testMethod.verbose_name = 'Teh Test Method'
