from django.urls import include, path

from .views import classroom, students, teachers

urlpatterns = [
    path('', classroom.home, name='home'),
    path('mots_cles/add/', students.SubjectCreateView.as_view(), name='subject_add'),
    path('domaine/add/', students.DomaineCreateView.as_view(), name='domaine_add'),
    path('type/add/', students.TypeCapteurCreateView.as_view(), name='type_add'),
    path('flyer/', students.FlyerView.as_view(), name='flyer'),
    path('profile_detail/<int:pk>/', students.StudentListView.as_view(), name='student_profile'), 

    path('CapMat/', include(([
        path('Projet/', students.HomeView.as_view(), name='lanceur_projet_home'),
        path('collobortion_page/<int:pk>/', students.ExpertListView.as_view(), name='collaboration_page'),
        #Mesprojets
        path('Projets/', students.MesProjetsView.as_view(), name='mes_projets'),
        #mettre à jour
        path('projet/<int:pk>/', students.QuizUpdateView.as_view(), name='projet_change'),

       #detail projet
        path('projet/detail/<slug:slug>', students.display_detail, name='projet_detail'),





#Partie  2

        #collaboration
          path('collaborations/Accueil', students.CollobarationListView.as_view(), name='collaborations'),
        #collaboration_potentielle
          path('collaborations/potentielles', students.PotentielleListView.as_view(), name='list_potentielle'),



#Partie  3
        #technologies
        path('technologies/Accueil', students.technologieListView.as_view(), name='technologies'),
        #La banque de technologies
        path('Technologies/Accueil/MesTechnologies', students.MesTechnologiesListView, name='MesTechnologies_list'),

        #Capteurs
        path('Capteurs/', students.CapteursView.as_view(), name='capteur_home'),
        path('capteur/ajouter/', students.CapteurCreateView.as_view(), name='capteur_add'),
        path('capteur/<int:pk>/modifier', students.CapteurUpdateView.as_view(), name='capteur_change'),
        path('capteur/<int:pk>/supprimer/', students.CapteurDeleteView.as_view(), name='capteur_delete'),



#Partie  4
     #Experts
        path('Experts/', students.ExpertsHomeListView.as_view(), name='expert_home'),
        path('Experts/<int:pk>/confirmation', students.createxpert, name='expert_confirmation'),
        path('Experts/Annuaire', students.AnnuaireListView, name='Annuaire'),
        path('Experts/Liste', students.ExpertPotentielleListView.as_view(), name='liste'),













          path('profile/', students.profile, name='profile'),
          path('visualiser', students.profile_view, name='visualiser_profile'), 
          






          
        path('equipe/projet/<int:pk>/', students.equipe_definition, name='equipe_projet'),
        path('equipe/projet/change/<int:pk>/', students.equipe_change.as_view(), name='equipe_change'),

        path('First_page', students.first_page.as_view(), name='first_page'),
   

        path('projet/add/', students.QuizCreateView.as_view(), name='projet_add'),
       
        path('projet/<int:pk>/delete/', students.QuizDeleteView.as_view(), name='projet_delete'),
        path('projet/detail/<slug:slug>', students.display_detail, name='projet_detail'),



        path('forum', students.ForumListView, name='forum_list'),
        path('forum/par/<username>/', students.ForumUserListView.as_view(), name='forum-by'),
        path('forum/par/profile/<username>/', students.ProfilUserListView.as_view(), name='forum_by_profile'),
        path('forum/projet/detail/<slug:slug>', students.forum_projet_detail, name='forum_detail'),

        


      
      
        
        #subject 
        
        
      
        #Recherche 

        path('Expert', students.ExpertsListView, name='experts_list'),
        path('Capteur', students.CapteurListView, name='capteurs_list'),
 
        

        
        
        
        
        
        path('partager/<int:pk>/', students.Publi_projet, name='publi_projet'),




        path('interests/', students.StudentInterestsView.as_view(), name='student_interests'),
       
       
        path('', students.QuizListView.as_view(), name='quiz_list'),
    
      
        path('Mes_projet/', students.QuizMesView.as_view(), name='projet_list'),

  
        
        path('taken/', students.TakenQuizListView.as_view(), name='taken_quiz_list'),
        path('quiz/<int:pk>/', students.take_quiz, name='take_quiz'),
    ], 'classroom'), namespace='students')),

    path('teachers/', include(([
        path('', teachers.QuizListView.as_view(), name='quiz_change_list'),
        path('quiz/add/', teachers.QuizCreateView.as_view(), name='quiz_add'),
        path('quiz/<int:pk>/', teachers.QuizUpdateView.as_view(), name='quiz_change'),
        path('quiz/<int:pk>/delete/', teachers.QuizDeleteView.as_view(), name='quiz_delete'),
        path('quiz/<int:pk>/results/', teachers.QuizResultsView.as_view(), name='quiz_results'),
        path('quiz/<int:pk>/question/add/', teachers.question_add, name='question_add'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/', teachers.question_change, name='question_change'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', teachers.QuestionDeleteView.as_view(), name='question_delete'),
    ], 'classroom'), namespace='teachers')),
]
