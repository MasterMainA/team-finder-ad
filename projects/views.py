import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from .models import Project, Skill
from .forms import ProjectForm

class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 12

    def get_queryset(self):
        queryset = Project.objects.all().order_by('-created_at')
        skill_name = self.request.GET.get('skill')
        if skill_name:
            queryset = queryset.filter(skills__name=skill_name)
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_skills'] = Skill.objects.all()
        context['active_skill'] = self.request.GET.get('skill')
        context['search_query'] = self.request.GET.get('q', '')
        return context

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project-details.html'
    context_object_name = 'project'

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/create-project.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = False
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        self.object.participants.add(self.request.user)
        return response

    def get_success_url(self):
        return reverse('projects:detail', kwargs={'pk': self.object.pk})

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/create-project.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        return context

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def get_success_url(self):
        return reverse('projects:detail', kwargs={'pk': self.object.pk})

class ProjectCompleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        if request.user == project.owner and project.status == 'open':
            project.status = 'closed'
            project.save()
            return JsonResponse({"status": "ok", "project_status": "closed"})
        return JsonResponse({"status": "error"}, status=403)

class ProjectParticipateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        if request.user in project.participants.all():
            project.participants.remove(request.user)
        else:
            project.participants.add(request.user)
        return redirect('projects:detail', pk=pk)

class ProjectFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        if request.user in project.favorites.all():
            project.favorites.remove(request.user)
        else:
            project.favorites.add(request.user)
        return redirect(request.META.get('HTTP_REFERER', 'projects:detail'))

def skills_search(request):
    query = request.GET.get('q', '')
    skills = Skill.objects.filter(name__icontains=query).order_by('name')[:10]
    data = [{"id": skill.id, "name": skill.name} for skill in skills]
    return JsonResponse(data, safe=False)

@csrf_exempt
@require_POST
def skill_add(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    project = get_object_or_404(Project, pk=pk)
    if project.owner != request.user:
        return JsonResponse({'error': 'Forbidden'}, status=403)
    data = json.loads(request.body)
    skill_id = data.get('skill_id')
    name = data.get('name')
    created = False
    added = False
    skill = None
    if skill_id:
        skill = get_object_or_404(Skill, id=skill_id)
    elif name:
        skill, created = Skill.objects.get_or_create(name=name.strip())
    if skill:
        if skill not in project.skills.all():
            project.skills.add(skill)
            added = True
        return JsonResponse({
            "skill_id": skill.id,
            "created": created,
            "added": added
        })
    return JsonResponse({'error': 'Bad Request'}, status=400)

@csrf_exempt
@require_POST
def skill_remove(request, pk, skill_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    project = get_object_or_404(Project, pk=pk)
    if project.owner != request.user:
        return JsonResponse({'error': 'Forbidden'}, status=403)
    skill = get_object_or_404(Skill, id=skill_id)
    if skill in project.skills.all():
        project.skills.remove(skill)
    return JsonResponse({"status": "ok"})