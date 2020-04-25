from django.utils import timezone
from screenshower.models import Project, Paroi, Volume, NotchProject, PositionsPieces, PieceProject
from screenshower.forms import ProjectForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from screenshower.app_class.screen_shower import ScreenShower
# Create your views here.


def models_list(request):
    """
    view to list all project of user
    :param request:
    :return:
    """
    projects = Project.objects.filter(models=1)
    return render(request, 'screenshower/app/models_list.html', {'projects': projects})


@login_required
def model_new(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            project.published_date = timezone.now()
            project.save()
            return redirect('model_detail', pk=project.pk)
    else:
        form = ProjectForm()
    return render(request, 'screenshower/app/model_edit.html', {'form': form})


@login_required
def model_duplicate(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        project = duplicate(project)
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            project.published_date = timezone.now()
            project.models = 0
            project.save()
            return redirect('app', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'screenshower/app/model_duplicate.html', {'form': form})


@login_required
def model_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'screenshower/app/model_detail.html', {'project': project})


def duplicate(project):
    old_pk = project.pk
    project.pk = None
    project.save()

    parois = Paroi.objects.filter(project_id=old_pk)

    for paroi in parois:
        volumes = Volume.objects.filter(paroi_id=paroi.pk)
        paroi.pk = None
        paroi.project_id = project.pk
        paroi.save()
        for volume in volumes:
            notches = NotchProject.objects.filter(volume_id=volume.pk)
            volume.pk = None
            volume.paroi_id = paroi.pk
            volume.save()
            for notch in notches:
                notch.pk = None
                notch.volume_id = volume.pk
                notch.save()

    positions_pieces = PositionsPieces.objects.filter(project_id=old_pk)

    for position in positions_pieces:
        position.pk = None
        position.project_id = project.pk
        position.save()

    pieces_project = PieceProject.objects.filter(project_id=old_pk)

    for piece in pieces_project:
        piece.pk = None
        piece.project_id = project.pk
        piece.save()

    return project


