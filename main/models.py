from django.db import models

# Create your models here.
class Dolzhnost(models.Model):
    titleDolzhnost=models.CharField('Должность', max_length=100, default='Разнорабочий')

    def __str__(self):
        return self.titleDolzhnost



class Otdels(models.Model):
     myotdel = models.CharField('Отделы', max_length=30, blank=True, default='Производственный')

     def __str__(self):
         return self.myotdel



class Programm(models.Model):
    name_of_programm=[
        ('Информационное вещание',(('Sobitia', 'События ОТВ'),('Acent', 'Акцент'),('News','Новости 4 канала'),('Stend', 'Стенд'),('Pogoda', 'Погода'))),
        ('Художественно-развлекательное вещание', (('VseGovoryat', 'Все говорят об этом'),('Navigator', 'Навигатор'),('UE','Утренний экспресс'))),
        ('No programm', 'Без привязки к программе')
    ]
    name_programm=models.CharField('Программы', max_length=75,  null=True, blank=True, default='Без программы')


    def __str__(self):
        return self.name_programm
    class Meta:
        verbose_name_plural='Программы'


class Peoples(models.Model):
    male='муж'
    female='жен'


    female_choices=[('мужской', male), ('женский', female)]
    name=models.CharField('Имя',max_length=20,blank=True)
    sename=models.CharField('Отчество', max_length=50, blank=True)
    familia=models.CharField('Фамилия',max_length=50,blank=True)
    female=models.CharField('Пол', max_length=10, choices=female_choices, default='муж')
    dateOfBirth=models.DateField('Дата рождения', blank=True, null=True)
    dateStartWork=models.DateField('Дата приема на работу',blank=True, null=True)
    dateFinishtWork=models.DateField('Дата увольнения',blank=True, null=True)
    create_at=models.DateTimeField('дата создания записи', auto_now_add=True)
    modify_at=models.DateTimeField('Дата редактирования записи',auto_now=True)
    photo=models.ImageField('Фото', upload_to='photos/%Y/%m/%d/', blank=True)
    dolzhnost = models.ForeignKey(Dolzhnost, on_delete=models.PROTECT, null=True, verbose_name='Должность')
    programma=models.ManyToManyField(Programm, through='Progconnect', through_fields=('peop', 'prog'), verbose_name='Программа')
    otdel_people=models.ForeignKey(Otdels, on_delete=models.PROTECT, null=True, verbose_name="Отдел")

#    otpusk=models.ForeignKey('Otpuska', on_delete=models.CASCADE, null=True, verbose_name='Фамилия сотрудника')

    def __str__(self):
        return self.familia

    class Meta:
        verbose_name_plural='Сотрудники'


class Progconnect(models.Model):
    prog=models.ForeignKey(Programm, on_delete=models.CASCADE)
    peop=models.ForeignKey(Peoples, on_delete=models.CASCADE)


class Otpuska(models.Model):

    typeOtpusk=[
                ('О', 'Очередной'),
                ('Х','Без сохранения оплаты'),
                ('Б','Больничный'),
                ('П','Прогул'),
                ]
#    person=models.CharField('Фамилия сотрудника', max_length=50, null=True)
    title_otpusk=models.CharField('Тип отпуска', max_length=50, choices=typeOtpusk, null=True )
    nachOtpusk=models.DateField('Начало отпуска',null=True)
    kolvoDney=models.IntegerField('Количество дней', null=True, blank=True )
    konecOtpusk=models.DateField('Конец отпуска', null=True)
    zayvlenie = models.ImageField('заявление(скан)', upload_to='zayvlenie/%m/%d/', blank=True, null=True)
    person=models.ForeignKey(Peoples, on_delete=models.CASCADE, null=True, verbose_name='Отпускник')

    def __str__(self):
        return self.title_otpusk


#
# class Describe(models.Model):
#     obosnovanie = models.CharField('Обоснование переработки', max_length=300, null=True, blank=False)
#
#     def __str__(self):
#         return self.obosnovanie


class Tabel(models.Model):
    typeWorkDay = [(8, 'Полная смена' ),
                  (4, 'Половина смены'),

                  (12, 'Переработка 0,5 смены'),
                  (16, 'Переработка 1 смена'),
                  (0, 'Не работал'),
                  ]

    dataTabel=models.DateField('Дата', null=True)
    workTime=models.IntegerField('Рабочий день', choices=typeWorkDay,  blank=True, null=True)
    primechanie=models.CharField('Примечание', max_length=300, null=True, blank=True)
    #obosnovanie=models.ForeignKey(Describe, on_delete=models.PROTECT, blank=False, null=True)
    man=models.ForeignKey(Peoples, on_delete=models.PROTECT, null=True, verbose_name='Сотрудник')
    def __int__(self):
        return self.workTime

    class Meta:
        verbose_name_plural='Трудодни'


class Proba(models.Model):
    name=models.CharField('name', max_length=20, null=True)
    sename=models.CharField('sename', max_length=20)
    age=models.IntegerField('age')
    e_mail=models.EmailField(null=True)
    data = models.DateField('Дата', null=True)
    def __int__(self):
        return self.sename