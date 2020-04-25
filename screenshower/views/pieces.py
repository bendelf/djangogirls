from screenshower.models import RefPiece
from screenshower.forms import PieceForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


@login_required
def piece_new(request):
    if request.method == "POST":
        form = PieceForm(request.POST)
        if form.is_valid():
            piece = form.save(commit=False)
            piece.save()
            return redirect('piece_detail', pk=piece.pk)
    else:
        form = PieceForm()
    return render(request, 'screenshower/app/piece_edit.html', {'form': form})


@login_required
def piece_edit(request, pk):
    piece = get_object_or_404(RefPiece, pk=pk)
    if request.method == "POST":
        form = PieceForm(request.POST, instance=piece)
        if form.is_valid():
            piece = form.save(commit=False)
            piece.save()
            return redirect('piece_detail', pk=piece.pk)
    else:
        form = PieceForm(instance=piece)
    return render(request, 'screenshower/app/piece_edit.html', {'form': form})
