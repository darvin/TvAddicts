from google.appengine.ext import db
from appengine_admin.db_extensions import ManyToManyProperty


choices = ['one', 'two', 'three', 'four']

# Models
class ReferencedModel(db.Model):
    name = db.StringProperty("Name", required = True)
    whencreated = db.DateTimeProperty("Created", auto_now_add = True)
    whenupdated = db.DateTimeProperty("Updated", auto_now = True)

    def __unicode__(self):
        return unicode(self.name)

    def __str__(self):
        return self.__unicode__()

class TestModel(db.Model):
    stringField = db.StringProperty("String field")
    textField = db.TextProperty("Text field")
    choicesField = db.StringProperty("Choices field", choices = choices)
    integerField = db.IntegerProperty("Integer field", default = 0)
    booleanField = db.BooleanProperty("Boolean field")
    referenceField = db.ReferenceProperty(ReferencedModel, verbose_name = "Foreign key field")
    dateField = db.DateProperty("Date field")
    timeField = db.TimeProperty("Time field")
    datetimeField = db.DateTimeProperty("Date and Time field")
    userField = db.UserProperty("User field")
    categoryField = db.CategoryProperty("Category field")
    linkField = db.LinkProperty("Link field")
    emailField = db.EmailProperty("Email field")
    imField = db.IMProperty("IM Field")
    phoneNumberField = db.PhoneNumberProperty("Phone number field")
    postalAddressField = db.PostalAddressProperty("Postal address field")
    ratingField = db.RatingProperty("Rating field")
    whencreated = db.DateTimeProperty("Created", auto_now_add = True)
    whenupdated = db.DateTimeProperty("Updated", auto_now = True)

    def __unicode__(self):
        return self.stringField


class BaseTestModel(db.Model):
    stringField = db.StringProperty("String field in base class")

class DerivedTestModel(BaseTestModel):
    textField = db.TextProperty("Text field in derived class")

class DerivedTestModel2(DerivedTestModel):
    booleanField = db.BooleanProperty("Boolean field in derived class")
    blobField = db.BlobProperty()
    blobField_meta = db.BlobProperty()

class BaseTestModel2(db.Model):
    whencreated = db.DateTimeProperty("Created", auto_now_add = True)
    whenupdated = db.DateTimeProperty("Updated", auto_now = True)

class DerivedTestModel3(BaseTestModel2, DerivedTestModel2):
    pass

class ManyToManyTestModel(db.Model):
    name = db.StringProperty("Name")
    manyToManyRef = ManyToManyProperty(ReferencedModel, verbose_name = "Many to many reference")
