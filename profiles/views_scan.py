import json
from django.utils.timezone import now
from django.shortcuts import render
from django.http import JsonResponse
from .models import AttendanceRecord, UserProfile
import face_recognition

from django.shortcuts import render, redirect
from .models import AttendanceRecord
from django.core.files.base import ContentFile
import base64
import face_recognition
from .models import UserProfile, AttendanceRecord


def face_scan(request):
    if request.method == "POST":
        # Retrieve image data from the form submission
        image_data = request.POST.get("face_image")
        if not image_data:
            return JsonResponse({"error": "No image data provided."}, status=400)

        # Decode the base64 image
        try:
            format, imgstr = image_data.split(";base64,")
            img = face_recognition.load_image_file(
                ContentFile(base64.b64decode(imgstr))
            )
        except (ValueError, TypeError):
            return JsonResponse({"error": "Invalid image data format."}, status=400)

        # Extract face encodings from the captured image
        captured_encodings = face_recognition.face_encodings(img)
        if not captured_encodings:
            return JsonResponse({"error": "No face detected."}, status=400)

        captured_encoding = captured_encodings[0]

        # Compare with registered users
        users = UserProfile.objects.select_related("user")
        for profile in users:
            stored_encoding = json.loads(profile.user.face_encoding)
            matches = face_recognition.compare_faces(
                [stored_encoding], captured_encoding
            )
            if matches[0]:
                # Determine the next action
                action = "logout" if profile.last_login_status == "login" else "login"

                # Record the action in AttendanceRecord
                AttendanceRecord.objects.create(
                    user=profile.user, action=action, timestamp=now()
                )

                # Update last login status
                profile.last_login_status = action
                profile.save()
                # Perform login/logout action
                if action == "login":
                    login(request, profile.user)
                else:
                    logout(request)

                # Return the success response with the necessary data
                return JsonResponse(
                    {
                        "success": True,
                        "user": profile.user.username,
                        "action": action,
                        "timestamp": now().strftime("%Y-%m-%d %H:%M:%S"),
                    }
                )

                redirect("home")

                return render(request, "home.html")

        return render(request, "face_scan.html")

    # Render the face_scan.html template if the request is GET
    return render(request, "face_scan.html")


def attendance_records(request):
    records = AttendanceRecord.objects.order_by("-timestamp")
    return render(request, "attendance.html", {"records": records})
