from django.utils import timezone
from screenshower.models import Project, Paroi, Volume
from screenshower.forms import ProjectForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from screenshower.app_class.screen_shower import ScreenShower
# Create your views here.


def project_list(request):
    """
    view to list all project of user
    :param request:
    :return:
    """
    me = User.objects.get(username=request.user)
    projects = Project.objects.filter(author=me)
    return render(request, 'screenshower/app/project_list.html', {'projects': projects})


@login_required
def project_new(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            project.published_date = timezone.now()
            project.save()
            return redirect('app', pk=project.pk)
    else:
        form = ProjectForm()
    return render(request, 'screenshower/app/project_edit.html', {'form': form})


@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            project.published_date = timezone.now()
            project.save()
            return redirect('app', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'screenshower/app/project_edit.html', {'form': form})


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if project.author == request.user:
        return render(request, 'screenshower/app/project_detail.html', {'project': project})
    else:
        # TODO : à modifier
        project = get_object_or_404(Project, pk=-9999)
        return render(request, 'screenshower/app/project_detail.html', {'project': project})


@login_required
def project_remove(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    return redirect('project_list')


@login_required
def app(request, pk):
    project = get_object_or_404(Project, pk=pk)
    parois = Paroi.objects.filter(project_id=pk)
    sc = ScreenShower(project.closed_screenshower)
    sc.load_paroi(parois)
    print(parois)
    for paroi_app in sc.parois:
        volumes = Volume.objects.filter(paroi_id=paroi_app.id)
        sc.load_volume(paroi_app, volumes)

    sc.generate_position_pieces(sc.parois)

    return render(request, 'screenshower/app/app.html', {'project': project,
                                                         'sc': sc}
                  )