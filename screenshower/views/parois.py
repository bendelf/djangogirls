from screenshower.models import Paroi
from screenshower.forms import ParoiForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


@login_required
def paroi_edit(request, pk):
    paroi = get_object_or_404(Paroi, pk=pk)
    if request.method == "POST":
        form = ParoiForm(request.POST, instance=paroi)
        if form.is_valid():
            paroi = form.save(commit=False)
            paroi.save()
            return redirect('app', pk=paroi.project_id)
    else:
        form = ParoiForm(instance=paroi)
    return render(request, 'screenshower/app/paroi_edit.html', {'form': form})
