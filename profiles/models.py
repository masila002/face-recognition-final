from django.contrib.auth.models import AbstractUser
from django.db import models
import json


class CustomUser(AbstractUser):
    face_image = models.ImageField(upload_to="user_faces/", blank=True, null=True)
    face_encoding = models.TextField(
        blank=True, null=True
    )  # JSON encoded face encoding

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_groups",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    def set_face_encoding(self, encoding):
        """Convert the face encoding to JSON and store it."""
        self.face_encoding = json.dumps(
            encoding.tolist()
        )  # Convert numpy array to list and then to JSON

    def get_face_encoding(self):
        """Retrieve the face encoding as a list."""
        if self.face_encoding:
            return json.loads(self.face_encoding)  # Convert JSON string back to list
        return None

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    photo = models.ImageField(blank=True, upload_to="photos")
    bio = models.TextField()
    emp_no = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"profile of {self.user.username}"


class LoginHistory(models.Model):
    user = models.CharField(max_length=200, null=True)
    count = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.user


class Log(models.Model):
    user = models.ForeignKey("profiles.CustomUser", on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to="photos/", null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.action}"


# Implementing both logout and Login


class AttendanceRecord(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    action = models.CharField(
        max_length=10, choices=[("login", "Login"), ("logout", "Logout")]
    )
    timestamp = models.DateTimeField(auto_now_add=True)


class UserProfile(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    last_login_status = models.CharField(
        max_length=10,
        default="logout",
        choices=[("login", "Login"), ("logout", "Logout")],
    )
    last_scan_time = models.DateTimeField(null=True, blank=True)  # New field
    face_encoding = models.JSONField(default=list)
    face_image = models.ImageField(
        upload_to="user_faces/", null=True, blank=True
    )  # Store the image

    def __str__(self):
        return self.user.username
