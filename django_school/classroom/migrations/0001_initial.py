# Generated by Django 3.0 on 2020-04-19 10:11

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_student', models.BooleanField(default=False)),
                ('is_teacher', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Domaine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='TypeCapteur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('image', models.ImageField(default='default.jpg', null=True, upload_to='media/', verbose_name='Figure associated with the product ')),
                ('nom', models.CharField(blank=True, max_length=270, null=True, verbose_name='Nom : ')),
                ('prenom', models.CharField(blank=True, max_length=270, null=True, verbose_name='Prénom : ')),
                ('adresse_email', models.EmailField(blank=True, max_length=100, null=True, verbose_name='Adresse email : ')),
                ('composante', models.CharField(blank=True, max_length=100, null=True, verbose_name='Composante : ')),
                ('fonction', models.CharField(blank=True, max_length=270, null=True, verbose_name='Fonction : ')),
                ('expert', models.BooleanField(default=False, verbose_name='Je souhaite participer à des projet ')),
                ('domaine', models.ManyToManyField(related_name='domaines_expert', to='classroom.Domaine', verbose_name='Domaines de Compétences  ')),
                ('interests', models.ManyToManyField(related_name='interested_student', to='classroom.Subject', verbose_name='Mots Clés  ')),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('titre_projet', models.CharField(max_length=100000, verbose_name='Titre du projet ')),
                ('description_projet', models.TextField(max_length=100000, null=True, verbose_name='Description du projet  ')),
                ('sensibilite', models.CharField(blank=True, max_length=270, null=True, verbose_name='Sensibilité ')),
                ('stabilite', models.CharField(blank=True, max_length=270, null=True, verbose_name='Stabilité  ')),
                ('selectivite', models.CharField(blank=True, max_length=270, null=True, verbose_name='Sélectivité ')),
                ('precision', models.CharField(blank=True, max_length=270, null=True, verbose_name='Precision')),
                ('gamme', models.CharField(blank=True, max_length=270, null=True, verbose_name='Gamme  ')),
                ('format_sortie', models.CharField(blank=True, max_length=100, null=True, verbose_name='Format de sortie ')),
                ('temps_reponse', models.CharField(blank=True, max_length=270, null=True, verbose_name='Temps de réponse ')),
                ('condition_ambiante', models.CharField(blank=True, max_length=270, null=True, verbose_name='Conditions ambiantes ')),
                ('cout', models.CharField(blank=True, max_length=270, null=True, verbose_name='Coût ')),
                ('poids', models.CharField(blank=True, max_length=270, null=True, verbose_name='Dimensions ')),
                ('taille', models.CharField(blank=True, max_length=270, null=True, verbose_name='taille ')),
                ('file_1', models.FileField(blank=True, null=True, upload_to='images/', verbose_name='Télécharger field 2 ')),
                ('file_2', models.FileField(blank=True, null=True, upload_to='images/', verbose_name='Télécharger field 3 ')),
                ('confidentalite', models.BooleanField(default=False, verbose_name='Je souhaite que mon projet reste confidentiel ')),
                ('finance', models.CharField(blank=True, max_length=270, null=True, verbose_name='Finanacement : ')),
                ('nom_1', models.CharField(blank=True, max_length=270, null=True, verbose_name='Nom : ')),
                ('prenom_1', models.CharField(blank=True, max_length=270, null=True, verbose_name='Prénom : ')),
                ('adresse_email_1', models.EmailField(blank=True, max_length=100, null=True, verbose_name='Adresse email : ')),
                ('nom_2', models.CharField(blank=True, max_length=270, null=True, verbose_name='Nom : ')),
                ('prenom_2', models.CharField(blank=True, max_length=270, null=True, verbose_name='Prénom : ')),
                ('adresse_email_2', models.EmailField(blank=True, max_length=100, null=True, verbose_name='Adresse email : ')),
                ('nom_3', models.CharField(blank=True, max_length=270, null=True, verbose_name='Nom : ')),
                ('prenom_3', models.CharField(blank=True, max_length=270, null=True, verbose_name='Prénom : ')),
                ('adresse_email_3', models.EmailField(blank=True, max_length=100, null=True, verbose_name='Adresse email : ')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('slug', models.SlugField(max_length=140, unique=True)),
                ('content', models.TextField()),
                ('domaine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='domaines_projet', to='classroom.Domaine', verbose_name="Domaines d'application  ")),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quizzes', to=settings.AUTH_USER_MODEL)),
                ('subject', models.ManyToManyField(related_name='projets', to='classroom.Subject', verbose_name='Mots Clés  ')),
                ('type_evt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type_projets', to='classroom.TypeCapteur', verbose_name="Type de l'événement à détecter  ")),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, verbose_name='Question')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='classroom.Quiz')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default.jpg', null=True, upload_to='media/', verbose_name='Figure associated with the product ')),
                ('nom', models.CharField(blank=True, max_length=270, null=True, verbose_name='Nom : ')),
                ('prenom', models.CharField(blank=True, max_length=270, null=True, verbose_name='Prénom : ')),
                ('institution', models.CharField(blank=True, max_length=100, null=True, verbose_name='Institution : ')),
                ('composante', models.CharField(blank=True, max_length=100, null=True, verbose_name='Composante : ')),
                ('adresse_email', models.EmailField(blank=True, max_length=100, null=True, verbose_name='Adresse email : ')),
                ('discipline', models.CharField(blank=True, choices=[('aéronautique', 'Aéronautique'), ('automobile', 'Automobile'), ('son', 'Son'), ('industrie_agroalimentaire', 'Industrie Agroalimentaire'), ('industrie_alimentaire', 'Industrie Alimentaire'), ('metallurgie', 'Métallurgie'), ('production', 'Production énergie'), ('medical', 'Médical')], default='Sélectionner', max_length=100, null=True, verbose_name="Domaine d'activité  :")),
                ('fonction', models.CharField(blank=True, max_length=270, null=True, verbose_name='Fonction : ')),
                ('competances', models.CharField(blank=True, choices=[('aéronautique', 'Aéronautique'), ('automobile', 'Automobile'), ('son', 'Son'), ('industrie_agroalimentaire', 'Industrie Agroalimentaire'), ('industrie_alimentaire', 'Industrie Alimentaire'), ('metallurgie', 'Métallurgie'), ('production', 'Production énergie'), ('medical', 'Médical')], default='Sélectionner', max_length=100, null=True, verbose_name=' Compétences :')),
                ('description', models.CharField(blank=True, max_length=100000, null=True, verbose_name='Présentation  ')),
                ('adresse', models.CharField(blank=True, max_length=100000, null=True, verbose_name='Adresse ')),
                ('numero_telephone', models.CharField(blank=True, max_length=100000, null=True, verbose_name='Adresse ')),
                ('mots_cles', models.CharField(blank=True, max_length=270, null=True, verbose_name='Mots clés : ')),
                ('file_2', models.FileField(blank=True, null=True, upload_to='media/', verbose_name='Télecharger un de vos travaux ')),
                ('file_3', models.FileField(blank=True, null=True, upload_to='media/', verbose_name='Télecharger un de vos travaux ')),
                ('file_4', models.FileField(blank=True, null=True, upload_to='media/', verbose_name='Télecharger un de vos travaux ')),
                ('location', models.CharField(blank=True, max_length=30)),
                ('birthdate', models.DateField(blank=True, null=True, verbose_name='Votre date de naissance ')),
                ('interests', models.ManyToManyField(related_name='interested_profile', to='classroom.Subject')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='The publication date')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cases_public', to='classroom.Quiz')),
            ],
        ),
        migrations.CreateModel(
            name='Equipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='gourpe1', max_length=270, verbose_name='Nom : ')),
                ('nom_1', models.CharField(blank=True, max_length=270, null=True, verbose_name='Nom : ')),
                ('prenom_1', models.CharField(blank=True, max_length=270, null=True, verbose_name='Prénom : ')),
                ('adresse_email_1', models.EmailField(blank=True, max_length=100, null=True, verbose_name='Adresse email : ')),
                ('nom_2', models.CharField(blank=True, max_length=270, null=True, verbose_name='Nom : ')),
                ('prenom_2', models.CharField(blank=True, max_length=270, null=True, verbose_name='Prénom : ')),
                ('adresse_email_2', models.EmailField(blank=True, max_length=100, null=True, verbose_name='Adresse email : ')),
                ('nom_3', models.CharField(blank=True, max_length=270, null=True, verbose_name='Nom : ')),
                ('prenom_3', models.CharField(blank=True, max_length=270, null=True, verbose_name='Prénom : ')),
                ('adresse_email_3', models.EmailField(blank=True, max_length=100, null=True, verbose_name='Adresse email : ')),
                ('quiz', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='equipes', to='classroom.Quiz')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('email', models.EmailField(max_length=254)),
                ('body', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='classroom.Quiz')),
            ],
            options={
                'ordering': ['created_on'],
            },
        ),
        migrations.CreateModel(
            name='Capteur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_capteur', models.CharField(blank=True, max_length=270, null=True, verbose_name='Nom du capteur ')),
                ('type_capteur', models.CharField(blank=True, max_length=270, null=True, verbose_name='Type du capteur  ')),
                ('description_projet', models.TextField(blank=True, max_length=100000, null=True, verbose_name='Description du capteur ')),
                ('technologie_utilisee', models.CharField(blank=True, max_length=270, null=True, verbose_name='Technologie utilisée')),
                ('etendue', models.CharField(blank=True, max_length=270, null=True, verbose_name='Etendue de mesure  ')),
                ('sensibilite', models.CharField(blank=True, max_length=270, null=True, verbose_name='Sensibilité ')),
                ('resolution', models.CharField(blank=True, max_length=270, null=True, verbose_name='Résolution ')),
                ('precision', models.CharField(blank=True, max_length=270, null=True, verbose_name='Précision  ')),
                ('rapidite', models.CharField(blank=True, max_length=270, null=True, verbose_name='Rapidité ')),
                ('justesse', models.CharField(blank=True, max_length=270, null=True, verbose_name='Justesse  ')),
                ('reproductibilite', models.CharField(blank=True, max_length=270, null=True, verbose_name='Reproductibilité ')),
                ('temps_de_reponse', models.CharField(blank=True, max_length=270, null=True, verbose_name='Temps de réponse   ')),
                ('bande_passante', models.CharField(blank=True, max_length=270, null=True, verbose_name='Bande passante   ')),
                ('hysteresis', models.CharField(blank=True, max_length=270, null=True, verbose_name='Hystérésis ')),
                ('gamme_temperature', models.CharField(blank=True, max_length=270, null=True, verbose_name="Gamme de température d'utilisation ")),
                ('file_1', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Figure associée au produit ')),
                ('file_2', models.FileField(blank=True, null=True, upload_to='images/', verbose_name='Télécharger field 2 ')),
                ('file_3', models.FileField(blank=True, null=True, upload_to='images/', verbose_name='Télécharger field 3 ')),
                ('confidentalite', models.BooleanField(default=False, verbose_name='Je souhaite que mon projet reste confidentiel ')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('domaine', models.ManyToManyField(related_name='domaines_capteur', to='classroom.Domaine', verbose_name="Domaines d'application  ")),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='capteurs', to=settings.AUTH_USER_MODEL)),
                ('subject', models.ManyToManyField(related_name='capteurs', to='classroom.Subject', verbose_name='Mots Clés  ')),
                ('type_evt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type_capteurs', to='classroom.TypeCapteur')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, verbose_name='Answer')),
                ('is_correct', models.BooleanField(default=False, verbose_name='Correct answer')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='classroom.Question')),
            ],
        ),
        migrations.CreateModel(
            name='TakenQuiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taken_quizzes', to='classroom.Quiz')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taken_quizzes', to='classroom.Student')),
            ],
        ),
        migrations.CreateModel(
            name='StudentAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='classroom.Answer')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_answers', to='classroom.Student')),
            ],
        ),
    ]
