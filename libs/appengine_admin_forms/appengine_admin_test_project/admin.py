import models
import models_utf8
import appengine_admin

## Admin views ##
class AdminTestModel(appengine_admin.ModelAdmin):
    model = models.TestModel
    listFields = (
        'stringField',
        'textField',
        'choicesField',
        'integerField',
        'booleanField',
        'referenceField',
        'dateField',
        'timeField',
        'datetimeField',
        'userField',
        'categoryField',
        'linkField',
        'emailField',
        'imField',
        'phoneNumberField',
        'postalAddressField',
        'ratingField',
        'whencreated',
        'whenupdated')
    editFields = (
        'stringField',
        'textField',
        'choicesField',
        'integerField',
        'booleanField',
        'referenceField',
        'dateField',
        'timeField',
        'datetimeField',
        'userField',
        'categoryField',
        'linkField',
        'emailField',
        'imField',
        'phoneNumberField',
        'postalAddressField',
        'ratingField')
    readonlyFields = ('whencreated', 'whenupdated')
    listGql = 'order by stringField, integerField'

class AdminReferencedModel(appengine_admin.ModelAdmin):
    model = models.ReferencedModel
    listFields = ('name', 'whencreated', 'whenupdated')
    editFields = ('name',)
    readonlyFields = ('whencreated', 'whenupdated')
    listGql = 'order by name'

class AdminUtf8TestModel(appengine_admin.ModelAdmin):
    model = models_utf8.Utf8TestModel
    listFields = (
        'stringField',
        'testMethod',
        'textField',
        'integerField',
        'booleanField',
        'referenceField',
        'whencreated',
        'whenupdated',
    )
    editFields = (
        'stringField',
        'textField',
        'integerField',
        'booleanField',
        'referenceField',
    )
    readonlyFields = ('whencreated', 'whenupdated')

class AdminUtf8ReferencedModel(appengine_admin.ModelAdmin):
    model = models_utf8.Utf8ReferencedModel
    listFields = ('name', 'whencreated', 'whenupdated')
    editFields = ('name',)
    readonlyFields = ('whencreated', 'whenupdated')
    listGql = 'order by name'

class AdminDerivedTestModel(appengine_admin.ModelAdmin):
    model = models.DerivedTestModel
    listFields = ('stringField',)
    editFields = ('stringField', 'textField')

class AdminDerivedTestModel2(appengine_admin.ModelAdmin):
    model = models.DerivedTestModel2
    listFields = ('blobField', 'stringField', 'booleanField', 'blobField')
    editFields = ('stringField', 'textField', 'booleanField', 'blobField')
    readonlyFields = ('blobField',)

class AdminDerivedTestModel3(appengine_admin.ModelAdmin):
    model = models.DerivedTestModel3
    listFields = ('stringField', 'booleanField', 'whencreated', 'whenupdated')
    editFields = ('stringField', 'textField', 'booleanField')
    readonlyFields = ('whencreated', 'whenupdated')

class AdminManyToManyTestModel(appengine_admin.ModelAdmin):
    model = models.ManyToManyTestModel
    listFields = ('name', 'manyToManyRef')
    editFields = ('name', 'manyToManyRef')
    
appengine_admin.register(
    AdminTestModel,
    AdminReferencedModel,
    AdminUtf8TestModel,
    AdminUtf8ReferencedModel,
    AdminDerivedTestModel,
    AdminDerivedTestModel2,
    AdminDerivedTestModel3,
    AdminManyToManyTestModel,
)
