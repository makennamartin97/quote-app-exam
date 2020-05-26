from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def registerValidator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(postData['firstname']) < 2:
            errors['fname'] = "First name is required to be at least 2 characters!"
        if len(postData['email']) == 0:
            errors['emailrequired'] = "Email is required!"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['invalidemail'] = "Email not valid!"
        if len(postData['password']) < 8:
            errors['pw_length'] = "Password should be at least 8 characters!"
        if postData['password'] != postData['confirm']:
            errors['nomatch'] = "Password does not match!"

        return errors

    def loginValidator(self, postData):
        errors = {}
        if len(postData['email']) == 0:
            errors['emailrequired'] = "Email required"
        else:
            usersWithEmail = User.objects.filter(email = postData['email'])
            print(usersWithEmail)
            if len(usersWithEmail)==0:
                errors['emailnotregistered'] = "Email not found, please register."
            else:
                usertocheck = usersWithEmail[0]
                if bcrypt.checkpw(postData['password'].encode(),usertocheck.password.encode()):
                    print('password match')
                else:
                    errors['pwwrong'] = "Password incorrect."
        return errors

class QuoteManager(models.Manager):
    def quoteValidator(self, postData):
        errors = {}
        print(postData)
        print("printing post data")
        if len(postData['message']) <10:
            errors['quotelength'] = "Quote needs to be at least 10 characters"
        if len(postData['quoter']) <2:
            errors['quotedbyLength'] = "Quoted by needs to have at least 2 characters"
        return errors
    #def editValidator(self, postData):
    #    errors = {}
    #    if len(postData['newmessage']) <10:
    #        errors['messagelength'] = "Quote needs to be at least 10 characters"
    #    if len(postData['newquoter']) <2:
    #        errors['quoterlength']="Quoter needs to be at least 2 characters"
    #    return errors

class User(models.Model):
    firstname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    confirm = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return f"User: {self.firstname}"

class Quote(models.Model):
    quotemessage = models.CharField(max_length=255)
    quotedby = models.CharField(max_length=255)
    uploader = models.ForeignKey(User, related_name='quotes_uploaded', on_delete = models.CASCADE)
    favoriters = models.ManyToManyField(User, related_name = "quotes_favorited")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()


# Create your models here.
