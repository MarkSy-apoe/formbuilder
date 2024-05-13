from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
TAG_CHOICES = (
	("School", "School"),
	("Work", "Work"),
	("Community", "Community"),
	("Survey", "Survey"),
	("Religion", "Religion"),
)

FORM_COMP =(
	("Name", "Name"),
	("Gender", "Gender"),
	("Date of birth", "Date of birth"),
	("Email", "Email"),
	("Address", "Address"),
)

class MyAccountManager(BaseUserManager):

	def create_user(self, email, username, first_name, last_name, password=None):
		if not email:
			raise ValueError("Users must have an email address.")
		if not username:
			raise ValueError("Users must have username.")
		if not first_name:
			raise ValueError("Users must have an first_name.")
		if not last_name:
			raise ValueError("Users must have an last_name.")

		user = self.model(
			email=self.normalize_email(email),
			username=username,
			first_name=first_name,
			last_name=last_name,
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, first_name, last_name, password):
		user = self.create_user(
			email=email,
			username=username,
			first_name=first_name,
			last_name=last_name,
			password=password,
		)

		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.is_confirmed = True

		user.save(using=self._db)
		return user
	

class Account(AbstractBaseUser):
	email 			= models.EmailField(verbose_name="email", max_length=60, unique=True)
	username        = models.CharField(max_length=30, unique=True)
	first_name 		= models.CharField(max_length=30, null=True)
	last_name 		= models.CharField(max_length=30, null=True)
	date_joined 	= models.DateTimeField(verbose_name="date joined", auto_now_add=True)
	last_login 		= models.DateTimeField(verbose_name="last_login", auto_now=True)
	is_admin 		= models.BooleanField(default=False)
	is_active 		= models.BooleanField(default=True)
	is_staff 		= models.BooleanField(default=False)
	is_superuser 	= models.BooleanField(default=False)	

	objects = MyAccountManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

	def __str__(self):
		return self.username

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True


class Form(models.Model):
    title           = models.CharField(max_length=100)
    description     = models.TextField(blank=True)
    tag             = models.CharField(choices=TAG_CHOICES, max_length=100)
    creator         = models.ForeignKey(Account, on_delete=models.CASCADE, null = True)
	
    def __str__(self):
        return self.title
	

class FormComponent(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, null = True)
    component_type = models.CharField(choices= FORM_COMP, max_length=100)
    label = models.CharField(max_length=100)
    order = models.IntegerField(default=0)
	
    def __str__(self):
        return self.form.title + " " + str(self.order)

