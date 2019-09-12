from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse, FileResponse
from django.views.decorators.http import require_POST
import json
from constance import config
from .models import Assignment, GradingJob, JobStatusEnum, translate_okpy_status
from django.db import transaction
from .k8s import add_k_workers


def index(request: HttpRequest):
    return redirect("admin:index")


def _get_assignment(file_id):
    query = Assignment.objects.filter(assignment_id=file_id)
    result = get_object_or_404(query)
    return result


@require_POST
@transaction.atomic
def grade_batch(request: HttpRequest):
    req_data = json.loads(request.body)
    access_token = req_data["access_token"]
    backup_ids = req_data["subm_ids"]

    assignment_key = req_data["assignment"]
    assignment = _get_assignment(assignment_key)

    add_k_workers(len(backup_ids))

    # TODO(simon):
    # Address the issue of queue backpresssure:
    # specifically, okpy has a short retry period.
    # we need to check if the backup_id is already in queue
    # to avoid creating another task
    job_ids = []
    for backup_id in backup_ids:
        job = GradingJob(
            assignment=assignment, backup_id=backup_id, access_token=access_token
        )
        job.save()

        job_ids.append(job.job_id)

    return JsonResponse({"jobs": job_ids})


@require_POST
def check_result(request):
    jobs_ids = json.loads(request.body)
    status = {}
    for job_id in jobs_ids:
        job = GradingJob.objects.get(job_id=job_id)
        # str.split is used to normalized enum name
        status[job_id] = {"status": translate_okpy_status(job.status)}
    return JsonResponse(status)


def fetch_job(request):
    queued_jobs = GradingJob.objects.filter(status=JobStatusEnum.QUEUED).order_by(
        "enqueued_time"
    )
    if len(queued_jobs) == 0:
        return JsonResponse({"queue_empty": True})
    else:
        next_job = queued_jobs[0]
        next_job.dequeue()
        next_job.save()
        return JsonResponse(
            {
                "queue_empty": False,
                "skeleton": next_job.assignment.assignment_id,
                "backup_id": next_job.backup_id,
                "access_token": next_job.access_token,
                "job_id": next_job.job_id,
            }
        )


def get_file(request: HttpRequest, assignment_id):
    file = _get_assignment(assignment_id).file
    return FileResponse(file)


@require_POST
def report_done(request: HttpRequest, job_id):
    query = GradingJob.objects.filter(job_id=job_id)
    result = get_object_or_404(query)

    result.done()
    result.log_html = request.body.decode()

    result.save()
    return HttpResponse(status=200)


def get_job_log(request: HttpRequest, job_id):
    query = GradingJob.objects.filter(job_id=job_id)
    result = get_object_or_404(query)
    return HttpResponse(result.log_html)