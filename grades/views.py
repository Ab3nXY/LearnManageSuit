from django.shortcuts import render
from django.core.mail import send_mail
from .forms import ExamForm, ExamFormSet

def exam_grading(request):
    if request.method == 'POST':
        formset = ExamFormSet(request.POST)
        if formset.is_valid():
            students = formset.save(commit=False)

            for student in students:
                if student.score > 89:
                    message = f"Good job {student.name}, you have passed the exam with distinction."
                elif student.score > 79:
                    message = f"Congratulations {student.name}, you have passed the exam successfully."
                else:
                    message = f"Hi {student.name}, you might need to improve your study method."

                # Sending email
                send_mail(
                    'Exam Result',
                    message,
                    'abenxy0@gmail.com',  # Replace with your email address
                    [student.email],
                    fail_silently=False,  # Set to True if you want to suppress errors
                )

                student.email_sent = True
                student.save()

            return render(request, 'grades/success.html', {'message': message})
    else:
        formset = ExamFormSet(queryset=ExamFormSet.model.objects.none())  # Initialize with an empty queryset

    return render(request, 'grades/exam_grading.html', {'formset': formset})
