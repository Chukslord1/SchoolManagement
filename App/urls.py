import os
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.conf.urls.static import static
from . import views

app_name = "APP"
urlpatterns = [
    path("", views.login, name="login"),
    path("index.html", views.index, name="index"),
    path("index1.html", views.index, name="index1"),
    path("auth-login.html", views.login, name="login"),
    path("pages-recoverpw-2.html", views.recover, name="recover"),
    path("auth-lock-screen.html", views.verify, name="verify"),
    path("logout.html", views.logout, name="logout"),
    path("gen.html", views.generate, name="gen"),
    path("add-student.html", views.addStudent, name="addStudent"),
    path("add-student/bulkstudent.html", views.BulkStudent, name="BulkStudent"),
    path("student.html", views.Student, name="Student"),
    path("time-table.html", views.timeTable, name="timeTable"),
    path("syllabus.html", views.syllabus, name="syllabus"),
    path("subject.html", views.subject, name="subject"),
    path("sms.html", views.sms, name="sms"),
    path("profile.html", views.profile, name="profile"),
    path("manage-teacher.html", views.manageTeacher, name="manage-teacher"),
    path("manage-student.html", views.manageStudent, name="manage-student"),
    path("manage-parent.html", views.manageParent, name="manage-parent"),
    path("manage-libarian.html", views.manageLibarian, name="manage-libarian"),
    path("manage-admin.html", views.manageAdmin, name="manage-admin"),
    path("manage-accountant.html", views.manageAccountant, name="manage-accountant"),
    path("department.html", views.Dept, name="department"),
    path("daily-attendance.html", views.Attend, name="daily-attendance"),
    path("class.html", views.Class, name="class"),
    path("chat.html", views.Chat, name="chat"),
    path("calendar.html", views.Calendar, name="calendar"),
    path("admission.html", views.Admission, name="admission"),
    path("test_attend.html", views.test_attend, name="test_attend"),
    path("qr_code.html", views.decode_qr, name="qr_code"),







]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
