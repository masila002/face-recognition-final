from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from profiles.utils import is_ajax, classify_face
import base64

# from logs.models import Log
from django.core.files.base import ContentFile

# from django.contrib.auth.models import User
from .models import Profile, LoginHistory, Log
import logging

# Configure logging
logger = logging.getLogger(__name__)

#### Additional Importations
from django.shortcuts import render, redirect
from django.contrib.auth import login

from .forms import UserRegistrationForm
import face_recognition
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import CustomUser
from .forms import UserLoginForm
import json
from django.utils.timezone import now
from io import BytesIO
from PIL import Image
from .models import UserProfile, AttendanceRecord
from datetime import timedelta


# from .forms import CustomUserCreationForm


def login_view(request):
    return render(request, "home.html")


##### Additional codes      !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


# def face_login(request):
#     return render(request, "face_login.html")


# profiles/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import CustomUser

##from .forms import UserRegistrationForm  # Make sure to import your registration form
import face_recognition
import numpy as np


# ### User register form without the inclusion of live capture image


### Register with an included image live capture


def register(request):
    error_message = None  # Initialize error_message to None

    if request.method == "POST":
        form = UserRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)  # Don't save the user yet

            # Check if face image is provided as a live capture in base64 format
            if "face_image" in request.POST and request.POST["face_image"]:
                # Get the base64 image
                face_image_data = request.POST["face_image"]

                # try:
                #     # Decode base64 image
                #     format, imgstr = face_image_data.split(";base64,")
                #     ext = format.split("/")[-1]
                #     decoded_image = ContentFile(
                #         base64.b64decode(imgstr), name=f"face_image.{ext}"
                #     )

                #     # Process the image
                #     face_image = Image.open(BytesIO(base64.b64decode(imgstr)))
                #     face_image_np = np.array(face_image)  # Convert to NumPy array

                #     # Generate face encodings
                #     encodings = face_recognition.face_encodings(face_image_np)

                #     # Validate if a face is detected
                #     if not encodings:
                #         error_message = (
                #             "No face found in the captured image. Please try again."
                #         )
                #     else:
                #         # Save the user and face details
                #         user.save()
                #         user_profile = UserProfile.objects.create(user=user)
                #         user_profile.face_encoding = json.dumps(encodings[0].tolist())
                #         user_profile.face_image = decoded_image  # Save the image file
                #         user_profile.save()

                #         # Log the user in and redirect to the homepage
                #         login(request, user)
                #         return redirect("home")
                # except Exception as e:
                #     print("Error processing face image:", e)
                #     error_message = "There was an issue processing your face image. Please try again."

                image_data = request.POST["face_image"]
                try:
                    format, imgstr = image_data.split(";base64,")
                    ext = format.split("/")[-1]
                    img = ContentFile(
                        base64.b64decode(imgstr), name=f"face_image.{ext}"
                    )
                    print("Image successfully converted")

                    # Process the uploaded face image
                    uploaded_face = face_recognition.load_image_file(img)
                    uploaded_face_encodings = face_recognition.face_encodings(
                        uploaded_face
                    )

                    # Validate if face is detected
                    if not uploaded_face_encodings:
                        error_message = "No face found in the captured image."
                    else:
                        user.face_image = img
                        user.face_encoding = json.dumps(
                            uploaded_face_encodings[0].tolist()
                        )
                        user.save()
                        login(request, user)
                        return redirect("home")
                except Exception as e:
                    print("Error processing face image:", e)
                    error_message = "There was an issue processing your face image. Please try again."
            else:
                error_message = "Please capture an image for registration."
        else:
            print("Form is invalid:", form.errors)
            error_message = "Form validation failed. Please correct the errors below."
    else:
        form = UserRegistrationForm()

    context = {"form": form, "error": error_message}
    return render(request, "register.html", context)


"""def register(request):
    error_message = None  # Initialize error_message to None

    if request.method == "POST":
        form = UserRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)  # Don't save the user yet

            # Check if face image is provided as a live capture in base64 format
            if "face_image" in request.POST and request.POST["face_image"]:
                # Get the base64 image
                image_data = request.POST["face_image"]
                print("Face Image received successfully")

                try:
                    format, imgstr = image_data.split(";base64,")
                    ext = format.split("/")[-1]
                    img = ContentFile(
                        base64.b64decode(imgstr), name=f"face_image.{ext}"
                    )
                    print("Image successfully converted")

                    # Process the uploaded face image
                    uploaded_face = face_recognition.load_image_file(img)
                    uploaded_face_encodings = face_recognition.face_encodings(
                        uploaded_face
                    )

                    # Validate if face is detected
                    if not uploaded_face_encodings:
                        error_message = "No face found in the captured image."
                    else:
                        user.face_image = img
                        user.face_encoding = json.dumps(
                            uploaded_face_encodings[0].tolist()
                        )
                        user.save()
                        login(request, user)
                        return redirect("home")
                except Exception as e:
                    print("Error processing face image:", e)
                    error_message = "There was an issue processing your face image. Please try again."

            else:
                error_message = "Please capture an image for registration."
                print("No face_image in POST data")
        else:
            print("Form is invalid:", form.errors)
            error_message = "Form validation failed. Please correct the errors below."

    else:
        form = UserRegistrationForm()

    context = {"form": form, "error": error_message}
    return render(request, "register.html", context)"""


### for uploading the user image, this view correctly handles it
def upload_face_login(request):
    if request.method == "POST" and "face_image" in request.FILES:
        uploaded_image = request.FILES["face_image"]
        uploaded_face = face_recognition.load_image_file(uploaded_image)
        uploaded_face_encodings = face_recognition.face_encodings(uploaded_face)

        if uploaded_face_encodings:
            uploaded_face_encoding = uploaded_face_encodings[0]

            # Loop through each user and compare the uploaded face encoding to stored face encodings
            for user in CustomUser.objects.all():
                if user.face_encoding:  # Ensure face_encoding exists for the user
                    # Retrieve the stored face encoding
                    stored_face_encoding = json.loads(
                        user.face_encoding
                    )  # Convert JSON back to list

                    # Perform face comparison
                    match = face_recognition.compare_faces(
                        [stored_face_encoding], uploaded_face_encoding
                    )

                    if match[0]:  # If the face matches
                        login(request, user)
                        # return redirect("home")
                        return render(request, "trials.html")

        # If no match found, return an error message
        return render(
            request,
            "upload_face_login.html",
            {"error": "Face not recognized. Please try again."},
        )

    return render(request, "upload_face_login.html")


### The login view below allows for users to login through their images taken in the process
def face_login(request):
    if request.method == "POST" and "face_image" in request.POST:
        # Get the base64 image
        image_data = request.POST["face_image"]
        format, imgstr = image_data.split(";base64,")  # Get the format
        ext = format.split("/")[-1]  # Get the file extension

        # Convert base64 string to an image
        img = ContentFile(base64.b64decode(imgstr), name=f"face_image.{ext}")

        # Process the uploaded image for facial recognition
        uploaded_face = face_recognition.load_image_file(img)
        uploaded_face_encodings = face_recognition.face_encodings(uploaded_face)

        if uploaded_face_encodings:
            uploaded_face_encoding = uploaded_face_encodings[0]

            # Loop through each user and compare the uploaded face encoding to stored face encodings
            for user in CustomUser.objects.all():
                if user.face_encoding:  # Ensure face_encoding exists for the user
                    # Retrieve the stored face encoding
                    stored_face_encoding = json.loads(
                        user.face_encoding
                    )  # Convert JSON back to list

                    # Perform face comparison
                    match = face_recognition.compare_faces(
                        [stored_face_encoding], uploaded_face_encoding
                    )

                    if match[0]:  # If the face matches
                        login(request, user)
                        # return redirect("home")
                        return render(request, "trials.html")

            # If no match found, set an error message
            error_message = (
                "Face not recognized. The captured image isn't found in the database."
            )
        else:
            # No face encodings found in the uploaded image
            error_message = "No face detected in the captured image. Please try again."

        return render(request, "face_login.html", {"error": error_message})

    return render(request, "face_login.html")


### User login through their password ###
def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(
                    "home"
                )  # Change to your desired redirect URL after login
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = UserLoginForm()

    return render(request, "password_login.html", {"form": form})


##### end of additional codes         !!!!!!!!!!!!!!!!!!!!!!!!!!


def logout_view(request):
    logout(request)
    return redirect("home")


def user_profile(request):
    return render(request, "user_profile.html")


def employees(request):
    users = CustomUser.objects.all()
    user = request.user.username
    count = LoginHistory.objects.all()
    login_histories = LoginHistory.objects.all()
    return render(request, "employees.html", {"users": users, "count": count})


from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render


# views.py or any other file


def home_view(request):
    return render(request, "home.html")


def trials(request):
    # Your logic here
    return render(request, "trials.html")


def find_user_view(request):
    if is_ajax(request):
        photo = request.POST.get("photo")
        logger.debug("Photo received: %s", photo)  # Log the received photo

        # Decode the photo
        _, str_img = photo.split(";base64")
        decoded_file = base64.b64decode(str_img)

        # Initialize Log instance
        x = Log()
        x.user_id = (
            request.user.id
        )  # Set the user_id to avoid the NOT NULL constraint error
        x.photo.save(
            "upload.png", ContentFile(decoded_file)
        )  # Save the decoded image to the photo field

        # Classify the face
        res = classify_face(x.photo.path)
        logger.debug(
            "Face classification result: %s", res
        )  # Log the classification result

        if res:
            user_exists = user.objects.filter(username=res).exists()
            logger.debug("User exists: %s", user_exists)  # Log if the user exists
            if user_exists:
                user = user.objects.get(username=res)
                profile = Profile.objects.get(user=user)

                # Set the profile and save the Log instance
                x.profile = profile
                x.save()

                # Increment login count
                history, created = LoginHistory.objects.get_or_create(
                    user=user.username
                )
                history.user = user.username
                history.count += 1
                history.save()

                # Log the user in
                login(request, user)
                logger.debug("User logged in: %s", user.username)
                return JsonResponse({"success": True})
            else:
                logger.debug("User not found for classification result: %s", res)
                return JsonResponse({"success": False, "message": "User not found."})

        logger.debug("No face detected or classification failed.")
        return JsonResponse({"success": False, "message": "No face detected."})


def process_frame(request):
    if request.method == "POST":
        try:
            # Parse the frame data from the request
            frame_data = json.loads(request.body).get("frame")
            if not frame_data:
                return JsonResponse({"error": "No frame data provided."}, status=400)

            # Decode the base64 frame
            try:
                format, imgstr = frame_data.split(";base64,")
                img = Image.open(BytesIO(base64.b64decode(imgstr)))
            except Exception as e:
                return JsonResponse(
                    {"error": f"Error decoding image: {str(e)}"}, status=400
                )

            # Convert the PIL image to a NumPy array
            img_array = np.array(img)

            # Extract face encodings
            captured_encodings = face_recognition.face_encodings(img_array)
            if not captured_encodings:
                return JsonResponse({"error": "No face detected."}, status=400)

            captured_encoding = captured_encodings[0]

            # Check and log the captured encoding
            print(f"Captured Encoding: {captured_encoding}")

            # Match the face and update attendance
            users = UserProfile.objects.select_related("user")
            for profile in users:
                stored_encoding = json.loads(profile.user.face_encoding)
                stored_encoding = np.array(stored_encoding)

                # Check and log the stored encoding
                print(f"Stored Encoding: {stored_encoding}")

                matches = face_recognition.compare_faces(
                    [stored_encoding], captured_encoding
                )
                if matches[0]:
                    if profile.last_scan_time and (
                        now() - profile.last_scan_time < timedelta(minutes=1)
                    ):
                        time_left = timedelta(minutes=1) - (
                            now() - profile.last_scan_time
                        )
                        time_left_str = (
                            f"{time_left.seconds // 60}m {time_left.seconds % 60}s"
                        )
                        return JsonResponse(
                            {
                                "error": f"Face scan not allowed. Please wait {time_left_str} before scanning again."
                            },
                            status=403,
                        )

                    action = (
                        "logout" if profile.last_login_status == "login" else "login"
                    )
                    AttendanceRecord.objects.create(
                        user=profile.user, action=action, timestamp=now()
                    )
                    profile.last_login_status = action
                    profile.save()
                    return JsonResponse(
                        {
                            "status": "success",
                            "user": profile.user.username,
                            "action": action,
                        }
                    )
            return JsonResponse({"status": "no_match"})

        except Exception as e:
            return JsonResponse({"error": f"Unexpected error: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)


def get_face_encodings(request):
    try:
        profiles = UserProfile.objects.select_related("user")
        data = [
            {
                "name": profile.user.username,
                "encoding": json.loads(profile.user.face_encoding),
            }
            for profile in profiles
        ]
        return JsonResponse({"encodings": data})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
