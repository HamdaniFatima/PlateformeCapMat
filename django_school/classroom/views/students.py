from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django import forms
from ..decorators import student_required
from ..forms import StudentSignUpForm,ProfileCUpdateForm, CapteurForm, EventForm,ProjetForm, EquipeForm,TakeQuizForm, UserUpdateForm, ProfileUpdateForm ,TypeCapteurForm, DomaineForm, SubjectForm, StudentInterestsForm, CommentForm
from ..models import Capteur,Equipe, Quiz,Forum, Student,ExpertListe, TakenQuiz, User, Subject, Profile,Comment, Domaine, TypeCapteur
from  classroom.filters import CasesFilter, ExpertsFilter, CapteurFilter
from django.db.models import Q
from itertools import chain




class FlyerView(CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'flyer.html'







#Subject et mots Clés 

class SubjectCreateView(CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'classroom/informations/subject_add_form.html'

    def form_valid(self, form):
        quiz = form.save(commit=False)
        quiz.save()
        return redirect('subject_add')



#Type Capteurs 

class TypeCapteurCreateView(CreateView):
    model = TypeCapteur
    form_class = TypeCapteurForm
    template_name = 'classroom/informations/type_add_form.html'

    def form_valid(self, form):
        quiz = form.save(commit=False)
        quiz.save()
        return redirect('type_add')



#Nom de Domaines 
class DomaineCreateView(CreateView):
    model = Domaine
    form_class = DomaineForm
    template_name = 'classroom/informations/domaine_add_form.html'

    def form_valid(self, form):
        quiz = form.save(commit=False)
        quiz.save()
        return redirect('domaine_add')



#StudentSignUp

class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        
        login(self.request, user)
        return redirect('students:profile')



@method_decorator([login_required, student_required], name='dispatch')
class first_page(ListView):
    model = Quiz
    template_name = 'Projet/index.html'


#CrereProjet
@method_decorator([login_required, student_required], name='dispatch')
class HomeView(CreateView):
    model = Quiz
    form_class = ProjetForm
    template_name = 'Projet/home_page.html'
    

    def form_valid(self, form):
        quiz = form.save(commit=False)
        quiz.owner = self.request.user
        quiz.save()
        form.save_m2m()
        messages.success(self.request, 'The projet was created with success!' )
        return redirect('students:collaboration_page', quiz.pk)


#MesProjet
@method_decorator([login_required, student_required], name='dispatch')
class MesProjetsView(ListView):
    model = Quiz
    ordering = ('created_at', )
    context_object_name = 'quizzes'
    template_name = 'Projet/mes_projets.html'

    def get_queryset(self):
        queryset = self.request.user.quizzes  \
            .select_related() 
        return queryset



#Mettre à jour mon

@method_decorator([login_required, student_required], name='dispatch')
class QuizUpdateView(UpdateView):
    model = Quiz
    fields =['titre_projet', 'description_projet','type_evt', 'domaine', 'subject','sensibilite', 'stabilite',  'selectivite', 'precision','gamme','format_sortie','temps_reponse','condition_ambiante', 'cout','poids', 'taille','nom_1', 'prenom_1', 'adresse_email_1', 'nom_2','prenom_2','adresse_email_2','adresse_email_3','nom_3',  'file_1', 'file_2', 'confidentalite']
    context_object_name = 'quiz'
    template_name = 'Projet/projet_change_form.html'


    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing quizzes that belongs
        to the logged in user.
        '''
        return self.request.user.quizzes.all()

    def get_success_url(self):
        return reverse('students:projet_change', kwargs={'pk': self.object.pk})




#display detail

@login_required
def display_detail(request, slug):
    template_name = 'Projet/display_projet.html'
    post = get_object_or_404(Quiz, slug=slug)
    comments = post.comments.all()
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})





#Capteurs
def CapteurListView(request):
    capteur_list = Capteur.objects.all()
    case_filter = CapteurFilter(request.GET, queryset = capteur_list)
    template_name = 'technologies/technologies.html'
    return render(request, template_name, {'filter' : case_filter})







def test_update(request, pk):
    published_item = get_object_or_404(Quiz, pk=pk)
    published_item.save(update_fields=['is_published'])
    messages.success(request, 'Test number {} {} successfully'.format(pk, published_item.is_published))
    return redirect('test')




#Student




class StudentListView(ListView):
    template_name = 'classroom/students/user/info.html'
    def get_queryset(self):
        self.quiz = get_object_or_404(Student, pk=self.kwargs['pk'])
        return Student.objects.filter(pk = self.quiz.pk)












#ExpertListView
@method_decorator([login_required, student_required], name='dispatch')
class ExpertListView(ListView):
    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'Projet/collaboration_page.html'


    def get_queryset(self):
        quiz = get_object_or_404(Quiz, pk=self.kwargs['pk'])
        student_interests = quiz.subject.values_list('pk', flat=True)
        queryset = Student.objects.filter(expert=True, interests__in=student_interests).distinct()
        return queryset
   







# Les <============================> Collaborations  <============================>



        
#  Collaboration homa page       
@method_decorator([login_required, student_required], name='dispatch')
class CollobarationListView(ListView):
    model = Quiz
    template_name = 'Collabrations/home_page.html'




#  Collaboration potentielle collaboration       
@method_decorator([login_required, student_required], name='dispatch')
class PotentielleListView(ListView):
    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'Collabrations/potentielle.html'

    def get_queryset(self):
        student = self.request.user.student
        student_interests = student.interests.values_list('pk', flat=True)
        queryset = Quiz.objects.filter(subject__in=student_interests) 
        return queryset



#technologies recherches
def MesTechnologiesListView(request):
    capteur_list = Capteur.objects.all()
    case_filter = CapteurFilter(request.GET, queryset = capteur_list)
    template_name = 'technologies/technologies.html'
    return render(request, template_name, {'filter' : case_filter})




# Les <============================> Les Experts  <============================>

#  Expert  homa page       
@method_decorator([login_required, student_required], name='dispatch')
class ExpertsHomeListView(ListView):
    model = Quiz
    template_name = 'Expert/home_page.html'





#Expert
def ExpertsListView(request):
    case_list = Student.objects.all()
    case_filter = ExpertsFilter(request.GET, queryset = case_list)
    template_name = 'classroom/students/collaboration/experts_list.html'
    return render(request, template_name, {'filter' : case_filter})







#  Collaboration expertList      
@method_decorator([login_required, student_required], name='dispatch')
class ExpertPotentielleListView(ListView):
    model = ExpertListe
    context_object_name = 'quizzes'
    template_name = 'Expert/liste.html'

    def get_queryset(self):
        queryset = self.request.user.experts  \
            .select_related() 
        return queryset













#technologies recherches
def AnnuaireListView(request):
    exper_list = Student.objects.filter(expert=True)
    case_filter = ExpertsFilter(request.GET, queryset = exper_list)
    template_name = 'Expert/Annuaire.html'
    return render(request, template_name, {'filter' : case_filter})



def createxpert(request, pk):
    quiz = get_object_or_404(Student, pk=pk)
    student = request.user

    if student.experts.filter(pk=pk).exists():
       return render(request, 'Expert/confirmation_refuse.html')

    if request.method == 'POST':
            post=ExpertListe()
            post.owner= student
            post.student= quiz
            post.save()
            return render(request, 'Expert/confirmation.html')  

    else:
            return render(request,'Expert/confirmation_refuse.html')












@student_required
def take_Student(request, pk):
    quiz = get_object_or_404(Student, pk=pk)
    student = request.user

    if student.experts.filter(pk=pk).exists():
        return render(request, 'Expert/Annuaire.html')


    if request.method == 'POST':
        form = TakeQuizForm(question=question, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                student_answer = form.save(commit=False)
                student_answer.student = student
                student_answer.save()
                if student.get_unanswered_questions(quiz).exists():
                    return redirect('students:take_quiz', pk)
                else:
                    correct_answers = student.quiz_answers.filter(answer__question__quiz=quiz, answer__is_correct=True).count()
                    score = round((correct_answers / total_questions) * 100.0, 2)
                    TakenQuiz.objects.create(student=student, quiz=quiz, score=score)
                    if score < 50.0:
                        messages.warning(request, 'Better luck next time! Your score for the quiz %s was %s.' % (quiz.name, score))
                    else:
                        messages.success(request, 'Congratulations! You completed the quiz %s with success! You scored %s points.' % (quiz.name, score))
                    return redirect('students:quiz_list')
    else:
        form = TakeQuizForm(question=question)

    return render(request, 'classroom/students/take_quiz_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'progress': progress
    })




















# Les <============================> capteurs  <============================>

#  Collaboration homa page       
@method_decorator([login_required, student_required], name='dispatch')
class technologieListView(ListView):
    model = Quiz
    template_name = 'technologies/home_page.html'


#capteur_home

@method_decorator([login_required, student_required], name='dispatch')
class CapteursView(ListView):
    model = Capteur
    context_object_name = 'quizzes'
    template_name = 'technologies/MesTechnologies/home_page.html'


    def get_queryset(self):
        queryset = self.request.user.capteurs  \
            .select_related() 
        return queryset






# add sensore
@method_decorator([login_required, student_required], name='dispatch')
class CapteurCreateView(CreateView):
    model = Capteur
    form_class = CapteurForm
    template_name = 'capteurs/capteur_add.html'

    def form_valid(self, form):
        quiz = form.save(commit=False)
        quiz.owner = self.request.user
        quiz.save()
        form.save_m2m()
        messages.success(self.request, 'The projet was created with success!' )
        return redirect('students:capteur_home')


# Update sensore

@method_decorator([login_required, student_required], name='dispatch')
class CapteurUpdateView(UpdateView):
    model = Capteur
    fields =('nom_capteur', 'description_projet','subject', 'type_evt', 'domaine', 'technologie_utilisee', 'etendue','sensibilite','resolution','precision', 'rapidite','justesse','reproductibilite', 'temps_de_reponse','bande_passante','hysteresis', 'gamme_temperature','file_1', 'file_2', 'file_3','confidentalite',)
    context_object_name = 'quiz'
    template_name = 'capteurs/capteur_change_form.html'


    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing quizzes that belongs
        to the logged in user.
        '''
        return self.request.user.capteurs.all()

    def get_success_url(self):
        return reverse('students:capteur_change', kwargs={'pk': self.object.pk})



# Delete sensore

@method_decorator([login_required, student_required], name='dispatch')
class CapteurDeleteView(DeleteView):
    model = Capteur
    context_object_name = 'quiz'
    template_name = 'technologies/MesTechnologies/Supprimer.html'
    success_url = reverse_lazy('students:capteur_home')

    def delete(self, request, *args, **kwargs):
        quiz = self.get_object()
        messages.success(request, 'Le Capteur  %s a été supprimé avec succès ' % quiz.nom_capteur)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.capteurs.all()










@login_required
@student_required
def equipe_definition(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)


    if request.method == "POST":
        form = EquipeForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.quiz= quiz
            post.save()
            return redirect('students:equipe_change', quiz.pk)
    else:
        form = EquipeForm()
    return render(request, 'equipe/forms.html', {'form': form})




@method_decorator([login_required, student_required], name='dispatch')
class equipe_change(UpdateView):
    model = Equipe
    fields =('nom_1',)
    context_object_name = 'quiz'
    template_name = 'equipe/change_forms.html'


    def get_success_url(self):
        return reverse('students:equipe_change', kwargs={'pk': self.object.pk})



















    









@method_decorator([login_required, student_required], name='dispatch')
class QuizCreateView(CreateView):
    model = Quiz
    fields =('titre_projet', 'description_projet','subject', 'type_evt', 'nature_evt', 'grandeur_evt', 'envirennoment_evt','type_capteur', 'etendue','sensibilite','resolution', 'precision', 'rapidite', 'dimensions','finance','file_1', 'file_2', 'file_3','confidentalite',)
    template_name = 'classroom/students/quiz_add_form.html'

    def form_valid(self, form):
        quiz = form.save(commit=False)
        quiz.owner = self.request.user
        quiz.save()
        messages.success(self.request, 'The projet was created with success!')
        return redirect('students:lanceur_projet_home')





@method_decorator([login_required, student_required], name='dispatch')
class QuizDeleteView(DeleteView):
    model = Quiz
    context_object_name = 'quiz'
    template_name = 'classroom/students/quiz_delete_confirm.html'
    success_url = reverse_lazy('students:mes_projets')

    def delete(self, request, *args, **kwargs):
        quiz = self.get_object()
        messages.success(request, 'Le projet  %s a été supprimé avec succès ' % quiz.titre_projet)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.quizzes.all()


@method_decorator([login_required, student_required], name='dispatch')
class StudentInterestsView(UpdateView):
    model = Profile
    form_class = StudentInterestsForm
    template_name = 'classroom/students/interests_form.html'
    success_url = reverse_lazy('students:lanceur_projet_home')

    def get_object(self):
        return self.request.user.profile

    def form_valid(self, form):
        messages.success(self.request, 'Interests updated with success!')
        return super().form_valid(form)


@method_decorator([login_required, student_required], name='dispatch')
class QuizListView(ListView):
    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'classroom/students/quiz_list.html'

    def get_queryset(self):
        student = self.request.user.profile
        student_interests = student.interests.values_list('pk', flat=True)
        queryset = Quiz.objects.filter(subject__in=student_interests) 
        return queryset


@method_decorator([login_required, student_required], name='dispatch')
class StudentInterestsView(UpdateView):
    model = Profile
    form_class = StudentInterestsForm
    template_name = 'classroom/students/interests_form.html'
    success_url = reverse_lazy('students:quiz_list')

    def get_object(self):
        return self.request.user.profile

    def form_valid(self, form):
        messages.success(self.request, 'Interests updated with success!')
        return super().form_valid(form)


@method_decorator([login_required, student_required], name='dispatch')
class QuizMesView(ListView):
    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'classroom/students/projet_list.html'

    def get_queryset(self):
        queryset = self.request.user.quizzes \
            .select_related('subject') 
        return queryset










@method_decorator([login_required, student_required], name='dispatch')
class TakenQuizListView(ListView):
    model = TakenQuiz
    context_object_name = 'taken_quizzes'
    template_name = 'classroom/students/taken_quiz_list.html'

    def get_queryset(self):
        queryset = self.request.user.student.taken_quizzes \
            .select_related('quiz', 'quiz__subject') \
            .order_by('quiz__name')
        return queryset





@login_required
@student_required
def take_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    student = request.user.student

    if student.quizzes.filter(pk=pk).exists():
        return render(request, 'students/taken_quiz.html')

    total_questions = quiz.questions.count()
    unanswered_questions = student.get_unanswered_questions(quiz)
    total_unanswered_questions = unanswered_questions.count()
    progress = 100 - round(((total_unanswered_questions - 1) / total_questions) * 100)
    question = unanswered_questions.first()

    if request.method == 'POST':
        form = TakeQuizForm(question=question, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                student_answer = form.save(commit=False)
                student_answer.student = student
                student_answer.save()
                if student.get_unanswered_questions(quiz).exists():
                    return redirect('students:take_quiz', pk)
                else:
                    correct_answers = student.quiz_answers.filter(answer__question__quiz=quiz, answer__is_correct=True).count()
                    score = round((correct_answers / total_questions) * 100.0, 2)
                    TakenQuiz.objects.create(student=student, quiz=quiz, score=score)
                    if score < 50.0:
                        messages.warning(request, 'Better luck next time! Your score for the quiz %s was %s.' % (quiz.name, score))
                    else:
                        messages.success(request, 'Congratulations! You completed the quiz %s with success! You scored %s points.' % (quiz.name, score))
                    return redirect('students:quiz_list')
    else:
        form = TakeQuizForm(question=question)

    return render(request, 'classroom/students/take_quiz_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'progress': progress
    })




@login_required
def profile(request):
    if request.method == 'POST':
       
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.student)
        if p_form.is_valid():
           
       
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('students:first_page')

    else:
      
        p_form = ProfileUpdateForm(instance=request.user.student)

    context = {
    
        'p_form': p_form
    }

    return render(request, 'classroom/students/user/profile.html', context)





@login_required
def profile_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileCUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.student)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            form.save_m2m()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileCUpdateForm(instance=request.user.student)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'classroom/students/user/display_profile.html', context)




class ForumUserListView(ListView):
    template_name = 'classroom/students/forums/forum_by_user.html'
    def get_queryset(self):
        self.user = get_object_or_404(User, username = self.kwargs['username'])
        return Quiz.objects.filter(owner = self.user)



class ProfilUserListView(ListView):
    model = Quiz
    template_name = 'classroom/students/forums/profile_by_user.html'
    context_object_name  = "objForums"
    def get_queryset(self):
        self.user = get_object_or_404(User, username = self.kwargs['username'])
        return Profile.objects.filter(user = self.user)





def ForumListView(request):
    case_list = Quiz.objects.filter(confidentalite=False).order_by('-created_at')
    case_filter = CasesFilter(request.GET, queryset = case_list)
    template_name = 'classroom/students/forums/forum_list.html'
    return render(request, template_name, {'filter' : case_filter})





def forum_projet_detail(request, slug):
    template_name = 'classroom/students/forums/forum_post.html'
    post = get_object_or_404(Quiz, slug=slug)
    comments = post.comments.all()
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})







@login_required
@student_required
def Publi_projet(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    
    try:
           newSummary = Forum(post=quiz)

           newSummary.save()
    except quiz.DoesNotExist:
            raise Http404('Le projet does not exist')

    return render(request, 'classroom/students/home_page.html' )




