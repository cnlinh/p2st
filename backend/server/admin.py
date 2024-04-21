from server.utils import ImportUtils
from django.contrib import admin
from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from import_export.admin import ImportExportModelAdmin
import json

from .models import (
    Module, Enrollment, Topic, Conversation, 
    Question, Answer, Message, Rating
)

admin.site.register(Module)
admin.site.register(Topic)
admin.site.register(Conversation)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Message)
admin.site.register(Rating)

class CsvImportForm(forms.Form):
    csv_file = forms.FileField()

@admin.register(Enrollment)
class EnrollmentAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ("module","student_id")

    def import_action(self,request):
        import_object_status = []
        create_new_enrollments = []

        if request.method == "POST":
            create_new_enrollments = []
            csv_file = json.loads(request.POST.get("file_name"))
            reader = json.loads(request.POST.get("rows"))
            column_headers = json.loads(request.POST.get("csv_headers"))

            seen_pairs = set()
            util_obj = ImportUtils(column_headers)

            for row in reader:
                module_id = util_obj.validate_data(row[util_obj.get_column("module_id")])
                module_name = util_obj.validate_data(row[util_obj.get_column("module_name")])
                student_id = util_obj.validate_data(row[util_obj.get_column("student_id")])

                pair = (module_id, student_id)

                if pair in seen_pairs:
                    import_object_status.append({
                        "module_id": module_id,
                        "module_name": module_name,
                        "student_id": student_id,
                        "status": "SKIPPED",
                        "msg": "Duplicate entry in file skipped"
                    })
                    continue
                seen_pairs.add(pair)
                
                if not Module.objects.filter(id=module_id).exists():
                    import_object_status.append({
                        "module_id": module_id,
                        "module_name": module_name,
                        "student_id": student_id,
                        "status": "SKIPPED",
                        "msg": "Module ID not found"
                    })
                    continue

                if Enrollment.objects.filter(module_id=module_id, student_id=student_id).exists():
                    import_object_status.append({
                        "module_id": module_id,
                        "module_name": module_name,
                        "student_id": student_id,
                        "status": "SKIPPED",
                        "msg": "Duplicate entry in db skipped"
                    })
                    continue
                
                create_new_enrollments.append(
                    Enrollment(module_id=module_id, student_id=student_id)
                )
                import_object_status.append({
                    "module_id": module_id,
                    "module_name": module_name,
                    "student_id": student_id,
                    "status": "ENROLLED",
                    "msg": "Student enrolled successfully"
                })

            # bulk create objects
            Enrollment.objects.bulk_create(create_new_enrollments)

            context = {
                "file": csv_file,
                "entries": len(import_object_status),
                "results": import_object_status
            }
            return HttpResponse(json.dumps(context), content_type="application/json")

        form = CsvImportForm()
        context = {"form": form, "form_title": "Upload list of student id to enroll into a module in csv format.",
                    "description": "The file should have following headers: "
                                    "[module_id, module_name, student_id]."}
        return render(
            request, "admin/import_enrollments.html", context
        )
