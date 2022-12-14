# Generated by Django 4.0.2 on 2022-08-17 17:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dolzhnost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titleDolzhnost', models.CharField(default='Разнорабочий', max_length=100, verbose_name='Должность')),
            ],
        ),
        migrations.CreateModel(
            name='Otdels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('myotdel', models.CharField(blank=True, default='Производственный', max_length=30, verbose_name='Отделы')),
            ],
        ),
        migrations.CreateModel(
            name='Proba',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, null=True, verbose_name='name')),
                ('sename', models.CharField(max_length=20, verbose_name='sename')),
                ('age', models.IntegerField(verbose_name='age')),
                ('e_mail', models.EmailField(max_length=254, null=True)),
                ('data', models.DateField(null=True, verbose_name='Дата')),
            ],
        ),
        migrations.CreateModel(
            name='Programm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_programm', models.CharField(blank=True, default='Без программы', max_length=75, null=True, verbose_name='Программы')),
            ],
            options={
                'verbose_name_plural': 'Программы',
            },
        ),
        migrations.AlterModelOptions(
            name='peoples',
            options={'verbose_name_plural': 'Сотрудники'},
        ),
        migrations.AlterField(
            model_name='peoples',
            name='dateFinishtWork',
            field=models.DateField(blank=True, null=True, verbose_name='Дата увольнения'),
        ),
        migrations.AlterField(
            model_name='peoples',
            name='dateOfBirth',
            field=models.DateField(blank=True, null=True, verbose_name='Дата рождения'),
        ),
        migrations.AlterField(
            model_name='peoples',
            name='dateStartWork',
            field=models.DateField(blank=True, null=True, verbose_name='Дата приема на работу'),
        ),
        migrations.AlterField(
            model_name='peoples',
            name='familia',
            field=models.CharField(blank=True, max_length=50, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='peoples',
            name='name',
            field=models.CharField(blank=True, max_length=20, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='peoples',
            name='photo',
            field=models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/', verbose_name='Фото'),
        ),
        migrations.CreateModel(
            name='Tabel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataTabel', models.DateField(null=True, verbose_name='Дата')),
                ('workTime', models.IntegerField(blank=True, choices=[(8, 'Полная смена'), (4, 'Половина смены'), (12, 'Переработка 0,5 смены'), (16, 'Переработка 1 смена'), (0, 'Не работал')], null=True, verbose_name='Рабочий день')),
                ('primechanie', models.CharField(blank=True, max_length=300, null=True, verbose_name='Примечание')),
                ('man', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='main.peoples', verbose_name='Сотрудник')),
            ],
            options={
                'verbose_name_plural': 'Трудодни',
            },
        ),
        migrations.CreateModel(
            name='Progconnect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('peop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.peoples')),
                ('prog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.programm')),
            ],
        ),
        migrations.CreateModel(
            name='Otpuska',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_otpusk', models.CharField(choices=[('О', 'Очередной'), ('Х', 'Без сохранения оплаты'), ('Б', 'Больничный'), ('П', 'Прогул')], max_length=50, null=True, verbose_name='Тип отпуска')),
                ('nachOtpusk', models.DateField(null=True, verbose_name='Начало отпуска')),
                ('kolvoDney', models.IntegerField(blank=True, null=True, verbose_name='Количество дней')),
                ('konecOtpusk', models.DateField(null=True, verbose_name='Конец отпуска')),
                ('zayvlenie', models.ImageField(blank=True, null=True, upload_to='zayvlenie/%m/%d/', verbose_name='заявление(скан)')),
                ('person', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.peoples', verbose_name='Отпускник')),
            ],
        ),
        migrations.AddField(
            model_name='peoples',
            name='dolzhnost',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='main.dolzhnost', verbose_name='Должность'),
        ),
        migrations.AddField(
            model_name='peoples',
            name='otdel_people',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='main.otdels', verbose_name='Отдел'),
        ),
        migrations.AddField(
            model_name='peoples',
            name='programma',
            field=models.ManyToManyField(through='main.Progconnect', to='main.Programm', verbose_name='Программа'),
        ),
    ]
