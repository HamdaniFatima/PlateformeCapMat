from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from classroom.models import (Answer,Equipe, Quiz, Capteur, Question, Student, StudentAnswer, TypeCapteur , Domaine, Subject, User, Profile, Comment)


# Subject
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'



#Type_Capteur
class TypeCapteurForm(forms.ModelForm):
    class Meta:
        model = TypeCapteur
        fields = '__all__'


#Domaine

class DomaineForm(forms.ModelForm):
    class Meta:
        model = Domaine
        fields = '__all__'



#StudentSignUpForm

class StudentSignUpForm(UserCreationForm):
    email= forms.EmailField()

    interests = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='Vos disciplines scientifiques ',
    )

    domaine = forms.ModelMultipleChoiceField(
        queryset=Domaine.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='Vos domaines d"applications ',
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']
       
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
      
        user.save()
        student = Student.objects.create(user=user)
        student.interests.add(*self.cleaned_data.get('interests'))
        student.domaine.add(*self.cleaned_data.get('domaine'))
        student.adresse_email =user.email
       
        return user









class EventForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.get('user',None)
        #self.user = kwargs.pop('user',None)
        super(EventForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        #self.helper.form_action = reverse_lazy('simpleuser')
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-success'))     

    class Meta:
        model = Quiz
        fields = ['subject', 'domaine', 'titre_projet', 'description_projet', 'type_evt']
        widgets ={
        'subject': forms.CheckboxSelectMultiple,
        }













class ProjetForm(forms.ModelForm):

    subject = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Mots Clés ',
    

    )
    

    class Meta:
          model = Quiz
          fields = ['titre_projet', 'description_projet','type_evt', 'domaine', 'subject','sensibilite', 'stabilite',  'selectivite', 'precision','gamme','format_sortie','temps_reponse','condition_ambiante', 'cout','poids', 'taille','nom_1', 'prenom_1', 'adresse_email_1', 'nom_2','prenom_2','adresse_email_2','adresse_email_3','nom_3',  'file_1', 'file_2', 'confidentalite']
         

   





class ProjetForm(forms.ModelForm):

    subject = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label = 'Disciplines scientifiques necessaires au projet ',
    )

    class Meta:
          model = Quiz
          fields = ['titre_projet', 'description_projet','type_evt', 'domaine', 'subject','sensibilite', 'stabilite',  'selectivite', 'precision','gamme','format_sortie','temps_reponse','condition_ambiante', 'cout','poids', 'taille','nom_1', 'prenom_1', 'adresse_email_1', 'nom_2','prenom_2','adresse_email_2','adresse_email_3','nom_3',  'file_1', 'file_2', 'confidentalite']
         



class CapteurForm(forms.ModelForm):

    subject = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
          model = Capteur
          fields = ['nom_capteur', 'description_projet','subject', 'type_evt', 'domaine', 'technologie_utilisee', 'etendue','sensibilite','resolution','precision', 'rapidite','justesse','reproductibilite', 'temps_de_reponse','bande_passante','hysteresis', 'gamme_temperature','file_1', 'file_2', 'file_3','confidentalite',]
         
      
       












class EquipeForm(forms.ModelForm):

    class Meta:
        model = Equipe
        fields = ['nom_1', 'prenom_1', 'adresse_email_1', 'nom_2','prenom_2']







































class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user



 




class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', )


class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise ValidationError('Mark at least one answer as correct.', code='no_correct_answer')


class TakeQuizForm(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset=Answer.objects.none(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None)

    class Meta:
        model = StudentAnswer
        fields = ('answer', )

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['answer'].queryset = question.answers.order_by('text')




class DateInput(forms.DateInput):
    input_type = 'date'




class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


        





class StudentInterestsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('interests', )
        widgets = {
            'interests': forms.CheckboxSelectMultiple
        }

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username']



class ProfileUpdateForm(forms.ModelForm):


    class Meta:
          model = Student
          fields = ['image','nom', 'prenom','adresse_email', 'interests', 'composante', 'fonction', 'domaine', 'expert']
         
  
class ProfileCUpdateForm(forms.ModelForm):


    class Meta:
          model = Student
          fields = ['image','nom', 'prenom','adresse_email','interests', 'composante', 'fonction', 'domaine', 'expert']        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

