from datetime import datetime, date, timedelta
from django.core.exceptions import ObjectDoesNotExist, NON_FIELD_ERRORS
from django.urls import reverse

from django.views.generic.base import TemplateView
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect
from .models import Peoples, Otpuska, Dolzhnost, Tabel, Proba,  Otdels, Programm, Progconnect
from .forms import UserForm, OtpuskForm, Search, EditForm, ZayavaForm, DateForm, TabelForm, CreateWorkDayForm, manForm, CreateTabelNewDay, DeleteTabelDay_Form, ProbaForm
from django.forms import modelformset_factory, inlineformset_factory
from django.db.models import Q
from django.core.exceptions import NON_FIELD_ERRORS
import calendar


# Create your views here.


def index(request): #надо взять выборку отпусков в период с текущий месяц-1 до текущий месяц+1, и найти их хозяев.
    #надо сделать выбор месяца или период по датам

    userform = UserForm()
    people = Peoples.objects.all()
    data_form = DateForm(request.POST)
    DateToDay = datetime.now()
    MonthB=DateToDay.month
    print("MonthB:", MonthB)

    BirthPeople=Peoples.objects.filter(dateOfBirth__day=str(DateToDay.day), dateOfBirth__month=str(DateToDay.month))
    print("BP:", BirthPeople)
    if request.method == "POST":
        data_form = DateForm(request.POST)
        if data_form.is_valid():
            dd=request.POST.get('date')
            DateToDay=datetime.strptime(dd, "%Y-%m")
        else:
            return HttpResponse('Данные не корректны')

    q = (Q(konecOtpusk__month=DateToDay.month) | Q(konecOtpusk__month=DateToDay.month + 1)) & \
        (Q(nachOtpusk__month=DateToDay.month - 1) | Q(nachOtpusk__month=DateToDay.month))
    otpusk_person = Otpuska.objects.filter(q)


    for t in otpusk_person: #просто распечатка выборки
        delta=t.konecOtpusk - t.nachOtpusk
        print("DELTA:", delta)
        print("otpusk_person:", t.person, t.nachOtpusk.day)


    lengthmonth = calendar.monthrange(DateToDay.year, DateToDay.month)
    daymonth = []
    weekend = []
    for ii in range(1, lengthmonth[1] + 1):
        daymonth.append(ii)
        holiday = calendar.weekday(DateToDay.year, DateToDay.month, ii)
        if holiday == 5 or holiday == 6:
            weekend.append(ii)

    perKalendar = {name.person: {iii: 'lightgreen' for iii in range(1, lengthmonth[1] + 1)} for name in otpusk_person}

    for name in otpusk_person:

        for xx in range(1, lengthmonth[1] + 1):
            holiday = calendar.weekday(DateToDay.year, DateToDay.month, xx)
            if (holiday == 5 or holiday == 6):
                perKalendar[name.person][xx] = 'red'

        for name in otpusk_person:

            for xx in range(1, lengthmonth[1] + 1):
                xxx = datetime.date(datetime.strptime(str(DateToDay.year) + '-' + str(DateToDay.month) + '-' + str(xx), '%Y-%m-%d'))
                if name.nachOtpusk <= xxx < name.konecOtpusk and name.title_otpusk == 'Б':
                    perKalendar[name.person][xx] = {'yellow': 'Б'}
                if name.nachOtpusk <= xxx < name.konecOtpusk and name.title_otpusk == 'О':
                    perKalendar[name.person][xx] = {'yellow': 'О'}
                if name.nachOtpusk <= xxx < name.konecOtpusk and name.title_otpusk == 'Х':
                    perKalendar[name.person][xx] = {'yellow': 'X'}
                if name.nachOtpusk <= xxx < name.konecOtpusk and name.title_otpusk == 'П':
                    perKalendar[name.person][xx] = {'yellow': 'П'}

    #dateForm=selectDate(request.POST)


    context = {
        'title_site': 'Главная страница',
        'today': DateToDay,
        'people': people,
        'item': True,
        'daymonth': daymonth,
        'weekend': weekend,
        'otpusk': otpusk_person,
        'Kalendar': perKalendar,
        'dateform': data_form,
        'BirthPeople': BirthPeople,
    }

    return render(request, 'main/index.html', context)


def createcard(request):
    if (request.method == "POST"):
        uform = UserForm(request.POST, request.FILES)
        uform.save()
        fam = request.POST.get("familia")
        people = Peoples.objects.filter(familia=fam)
        print(people)
        context = {
            'peoples': people,
        }
        return redirect('index')
    #  return render(request, 'main/preview.html', context)
    else:
        userform = UserForm()

    context = {
        'form': userform,
    }
    return render(request, 'main/createcard.html', context)


#       newSotrudnik=Peoples()
#       newSotrudnik.name=request.POST.get("form_name")
#      newSotrudnik.familia=request.POST.get("form_familia")
#      newSotrudnik.save()
#      return HttpResponseRedirect('/')
#   context = { 'form': userform }
#  return render(request, 'main/createotpusk.html', context)

def search(request):
    d = datetime.now()
    if request.method == "GET":
        getzapros = request.GET.get("preview")
        print("GETTTT", getzapros)
        if getzapros != None:
            id_people = Peoples.objects.get(id=getzapros)
            print(id_people.dolzhnost)
            otpusk_person_form = ZayavaForm(request.POST, request.FILES)
            searchSotrudnikOtpusk = Otpuska.objects.filter(person_id=id_people.id)

            if searchSotrudnikOtpusk.exists():
                context = {
                    'cartochka': id_people,
                    'id_otpusknik': id_people.id,
                    'otpusk': searchSotrudnikOtpusk,
                    'zayavaform': otpusk_person_form,
                }
                contextPlus = drawKalendar(id_people.id, d)  # вызываем функцию и дополняем словарь context
                context.update(contextPlus)
                contextMonth = creatMonth(d)
                context.update(contextMonth)
            else:
                context = {
                    'cartochka': id_people,
                    'id_otpusknik': id_people.id,


                }

            #return render(request, 'main/preview.html', context)
            return HttpResponseRedirect('/preview/' + str(id_people.id))

    if request.method == "POST":

        searchOnFamilia = request.POST.get("search_familia")
        searchOnName = request.POST.get("search_name")
        searchSotrudnik = Peoples.objects.filter(familia=searchOnFamilia, name=searchOnName)


        if searchSotrudnik.exists():
            flag = '1'
            #        print("index", index)
            #        print(searchSotrudnik)
            context = {
                'cartochka': searchSotrudnik,
                'flag': flag,

            }

            #   return HttpResponseRedirect('/')
            return render(request, 'main/search.html', context)

        else:
            return HttpResponse('<h1>НИЧЕГО НЕ НАЙДЕНО</h1>')
    else:

        searchform = Search()
        context = {'searchform': searchform,
                   'flag': '0'}
        return render(request, 'main/search.html', context)


def preview(request, id):
    d=datetime.now()
    id_people = Peoples.objects.get(id=id)
#    pr=Programm.objects


#    print
#    for programm in peop_set.all(): print('ID_PEOPLE',programm)
    #    people=Peoples.objects.get(familia=id_people.familia, name=id_people.name)
    otpusk_person = Otpuska.objects.filter(person_id=id)
    otpusk_empty = Otpuska.objects.filter(zayvlenie='')

    dateform = DateForm(request.POST)
    if (request.method == "POST"):
        if dateform.is_valid():
            return HttpResponse('<h1>Выберете месяц</h1>')
        else:
            enterdate = request.POST.get("date")
            d = datetime.strptime(enterdate, "%Y-%m")
            # print("DATE:", type(d), d)
   # for t in otpusk_person:


    context = {
        'cartochka': id_people,
        'otpusk': otpusk_person,
        'id_otpusknik': id_people.id,
        'formEnterDate': dateform,

        }
    contextPlus = drawKalendar(id,d)                                      #вызываем функцию и дополняем словарь context
    context.update(contextPlus)
    contextMonth= creatMonth(d)
    context.update(contextMonth)
    searchtabel=persontabel(id)     #попытка передать табель сотрудника

    context.update(searchtabel)

    return render(request, 'main/preview.html', context)


def createotpusk(request, id_man):
    id_people = Peoples.objects.get(id=id_man)
    otpuskform = OtpuskForm()

    context={}
    d=datetime.now()


    if (request.method == "POST"):
        form2 = OtpuskForm(request.POST)


        if form2.is_valid():
        #    form2_clean = form2.cleaned_data['kolvoDney']
            new = Otpuska()
            new.title_otpusk = request.POST.get("title_otpusk")
            new.nachOtpusk = request.POST.get("nachOtpusk")
            new.kolvoDney = request.POST.get("kolvoDney")
            # преобразовываем str в datetime и в int, складываем и получаем дату окончания отпуска
            new.konecOtpusk = datetime.strptime(new.nachOtpusk, '%Y-%m-%d') + timedelta(days=int(new.kolvoDney))
            new.zayvlenie = request.FILES.get("zayvlenie")
            contextPlus = drawKalendar(id_people.id, datetime.strptime(new.nachOtpusk, '%Y-%m-%d'))  # вызываем функцию и дополняем словарь context
            context.update(contextPlus)

            SovpadeniaIsAble = 0
            SovpadenieList=[]



            for day in range(0, int(new.kolvoDney)):
                nextday = datetime.strptime(new.nachOtpusk, '%Y-%m-%d') + timedelta(days=day)
                qq = Q(person__dolzhnost=id_people.dolzhnost) & Q(person__programma=id_people.programma) & Q(nachOtpusk__lte=nextday) & \
                     Q(konecOtpusk__gt=nextday) & (Q(title_otpusk='О') | Q(title_otpusk='Х'))
                addKollegsOtpusk=Otpuska.objects.filter(qq)

                if addKollegsOtpusk.count()>0:
                    for add in addKollegsOtpusk:
                        SovpadenieList.append(add)
                        SovpadeniaIsAble = SovpadeniaIsAble + 1

                SovpadenieList = list(set(SovpadenieList))

                for name in SovpadenieList:
                    contextPlus = drawKalendar(name.person.id, nextday)  # вызываем функцию и дополняем словарь context
                    context['Kalendar'].update(contextPlus['Kalendar'])



            data = {
                'title_otpusk': new.title_otpusk,
                'nachOtpusk': new.nachOtpusk,
                'kolvoDney': new.kolvoDney,
                'zayvlenie': new.zayvlenie
            }

            otpuskform=OtpuskForm(data, initial=data)
            context_other = {
 #               'daymonth': daymonth,
#                'weekend': weekend,
                'otpuskform': otpuskform,
#                'Kalendar': perKalendar,
                'id_people': id_people,
                'today':datetime.strptime(new.nachOtpusk, '%Y-%m-%d'),
                'message':'Совпадение!!!'
            }

            for day in range(0, int(new.kolvoDney)):
                nextday_date_datetime=datetime.strptime(new.nachOtpusk, '%Y-%m-%d')+timedelta(days=day)
                nextday_date_str=nextday_date_datetime.strftime("%d")
                nextday_date=int(nextday_date_str)          #nextday.strftime("%d") - из datetime переводим в string?  а затем в int

                context['Kalendar'][id_people][nextday_date] ={'lightblue': '?'}
            # print('CONTEXT:', context['Kalendar'][id_people])
            # print('SovpadeniaIsAble:', SovpadeniaIsAble)
            context.update(context_other)

            if SovpadeniaIsAble>0:
                return render(request, 'main/createotpusk.html', context)
            #    return HttpResponseRedirect('/createotpusk/'+ str(id_people.id), context)
            else:
                print('Zapis v BAZU!')
# получаем строчку из базы ЛЮДИ с id=id_man , т.е. тот id который передали через GET, внутри кого мы находимся
                peoples_select = Peoples.objects.get(id=id_people.id)
                peoples_select.otpuska_set.add(new, bulk=False)
#                new.save()
#                all_otpuska = peoples_select.otpuska_set.all()
                newnew = Otpuska.objects.last()
                for i in range(int(newnew.kolvoDney)):
                    ddd = newnew.nachOtpusk + timedelta(days=i)
                    writetabel(ddd, id_people)

                return HttpResponseRedirect('/')  # переход на главную страницу
        else:
            print("Form2 not valid:")
     #   return HttpResponseRedirect('/tabel/')


    context = {
        'otpuskform': otpuskform,
        'id_people': id_people,

    }

    return render(request, 'main/createotpusk.html', context)



def _get_forms(request, formcls, prefix):
    dataa = request.POST if prefix in request.POST else None
    return formcls(dataa, prefix=prefix)



class CreateOtpuskView(TemplateView):
     template_name = 'main/createotpusk.html'
#         # методом переопределяем context
     def get_context_data(self, **kwargs):
         id_people = Peoples.objects.get(id=self.kwargs['id_man'])
         data = {
             'title_otpusk': 'О',

         }
         context=super(CreateOtpuskView, self).get_context_data(**kwargs)
         context['aform'] = OtpuskForm(initial=data, prefix='aform_pre')
         context['id_people']=id_people
         return context

     def post(self, request, *args, **kwargs):
         context = {}
        # context['otpuskform'] = OtpuskForm(prefix='aform_pre')
         #aform = _get_forms(request, OtpuskForm, 'aform_pre')
         aform=OtpuskForm(request.POST, prefix='aform_pre')
         context['aform']=aform
         id_people = Peoples.objects.get(id=self.kwargs['id_man'])

         if aform.is_bound and aform.is_valid():
             new = Otpuska()
             new.title_otpusk = aform["title_otpusk"].value()
             new.nachOtpusk = aform["nachOtpusk"].value()
             new.kolvoDney = aform["kolvoDney"].value()
             # преобразовываем str в datetime и в int, складываем и получаем дату окончания отпуска
             new.konecOtpusk = datetime.strptime(new.nachOtpusk, '%Y-%m-%d') + timedelta(days=int(new.kolvoDney))
             new.zayvlenie = aform['zayvlenie'].value()

             nachOtpusk_date=datetime.strptime(new.nachOtpusk, '%Y-%m-%d') #преобразуем new.nachOtpusk  в datetime

             contextPlus = drawKalendar(id_people.id, nachOtpusk_date)  # вызываем функцию и дополняем словарь context
             context.update(contextPlus)
             SovpadeniaIsAble = 0
             SovpadenieList = []
             for day in range(0, int(new.kolvoDney)):
                 allProgPerson=id_people.programma.all() #получаем все программы сотрудника, которому создаем отпуск из объекта id_people
                 for everyProgPerson in allProgPerson: #перебираем каждую программу и сверяем ее с остальными сотрудниками
                    nextday = nachOtpusk_date + timedelta(days=day)
                    qq = Q(person__dolzhnost=id_people.dolzhnost) & Q(person__programma__name_programm=everyProgPerson.name_programm) & Q(nachOtpusk__lte=nextday) & \
                    Q(konecOtpusk__gt=nextday) & (Q(title_otpusk='О') | Q(title_otpusk='Х'))

                    addKollegsOtpusk = Otpuska.objects.filter(qq) # поиск сотрудников по совпадению: должность, программа, период отпуска и по типу отпуска (рассматривается только отпуск ОЧЕРЕДНОЙ и БЕЗ СОДЕРЖАНИЯ)
                    if addKollegsOtpusk.count() > 0: # если записи были обнаружены, то создаем список из этих записей и далее оставляем только уникальные записи
                         for add in addKollegsOtpusk:
                             SovpadenieList.append(add)
                             SovpadeniaIsAble = SovpadeniaIsAble + 1

                 SovpadenieList = list(set(SovpadenieList))
                 for name in SovpadenieList:
                     if nextday.month==nachOtpusk_date.month: #если дата(месяц) очередного дня отпуска совпадает с месяцем желаемого начала отпуска, тогда рисуем календарь
                        contextPlus = drawKalendar(name.person.id, nextday)  # вызываем функцию и дополняем словарь context
                        context['Kalendar'].update(contextPlus['Kalendar'])


             context_other = {
              #  'otpuskform': otpuskform,
                'id_people': id_people,
                'today': nachOtpusk_date,
                'message': 'Совпадение!!!'
             }
             # qqq=Q(nachOtpusk__lte=nachOtpusk_date) & Q(konecOtpusk__gt=nachOtpusk_date)
             # is_otpusk= Otpuska.objects.filter(qqq)
             # if is_otpusk.count()>0:
             #     context_other['message']='У Вас такой отпуск уже есть!'
             for day in range(0, int(new.kolvoDney)):
                 nextday_date_datetime = nachOtpusk_date + timedelta(days=day) #перебираем даты отпуска

                 if nextday_date_datetime.month == nachOtpusk_date.month: # если рассматриваемый месяц равен месяцу начала отпуска, то рисуем календарь
                     nextday_date_str = nextday_date_datetime.strftime("%d")
                     nextday_date = int(nextday_date_str)  # nextday.strftime("%d") - из datetime переводим в string?  а затем в int
                     context['Kalendar'][id_people][nextday_date] = {'lightblue': '?'}

            # print('SovpadeniaIsAble:', SovpadeniaIsAble)
             context.update(context_other)
             print('CONTEXT:', context)
             if SovpadeniaIsAble > 0:
                 return render(request, 'main/createotpusk.html', context)
                 #return HttpResponseRedirect (reverse('createotpusk', kwargs={'id_man':id_people.id}))
                 #return HttpResponseRedirect('/createotpusk/'+ str(id_people.id), context)
             else:
                 print('Zapis v BAZU!')
                # получаем строчку из базы ЛЮДИ с id=id_man , т.е. тот id который передали через GET, внутри кого мы находимся
                 peoples_select = Peoples.objects.get(id=id_people.id)
                 peoples_select.otpuska_set.add(new, bulk=False)
                #                new.save()
                #                all_otpuska = peoples_select.otpuska_set.all()
                 newnew = Otpuska.objects.last()
                 for i in range(int(newnew.kolvoDney)):
                     ddd = newnew.nachOtpusk + timedelta(days=i)
                     writetabel(ddd, id_people)

                 return HttpResponseRedirect('/')  # переход на главную страницу
         else:
             #return render(request, 'main/createotpusk.html', context)
             return HttpResponse('<h1>Че-то не то</h1>')







def createworkday(request, id_man, data_work_id, data_work, data_day, data_month, data_year):
    id_people = Peoples.objects.get(id=id_man)
    dateOfWork = datetime.strptime(data_year + '-' + data_month + '-' + data_day, "%Y-%m-%d")
#    if data_work == 'О' or data_work == 'Б' or data_work == 'П' or data_work == 'Х':
#        id_otpusk_of_man = Otpuska.objects.get(id=data_work_id)
#        init_data_otpusk = {'title_otpusk': data_work, 'nachOtpusk': id_otpusk_of_man.nachOtpusk,
 #                           'kolvoDney': id_otpusk_of_man.kolvoDney}
 #       init_data_workday = {'dataTabel': dateOfWork}
 #   else:
 #       init_data_otpusk={'nachOtpusk':dateOfWork}
    try:
        tabel = Tabel.objects.get(man_id=id_people.id, dataTabel=dateOfWork)
    except ObjectDoesNotExist:
        Tabel.objects.create(man_id=id_people.id, dataTabel=dateOfWork)
        tabel = Tabel.objects.get(man_id=id_people.id, dataTabel=dateOfWork)
    init_data_workday={'dataTabel':dateOfWork, 'workTime':data_work, 'primechanie':tabel.primechanie}


    if (request.method == "POST"):
        form1 = CreateWorkDayForm(request.POST)
#        form2 = OtpuskForm(request.POST)
        if form1.is_valid():
            # обработка формы workdayForm
            CreateSmenaDate = request.POST.get("dataTabel")
            CreateSmena = request.POST.get("workTime")
            prim=request.POST.get("primechanie")
            tabel.workTime=CreateSmena
            tabel.primechanie=prim
            tabel.save()



 #       if form2.is_valid():
        #    form2_clean = form2.cleaned_data['kolvoDney']

 #           print("Form2 valid:")
 #           new = Otpuska()
 #           new.title_otpusk = request.POST.get("title_otpusk")
  #          new.nachOtpusk = request.POST.get("nachOtpusk")
 #          new.kolvoDney = request.POST.get("kolvoDney")
 #           # преобразовываем str в datetime и в int, складываем и получаем дату окончания отпуска
 #          new.konecOtpusk = datetime.strptime(new.nachOtpusk, '%Y-%m-%d') + timedelta(days=int(new.kolvoDney))
 #           new.zayvlenie = request.FILES.get("zayvlenie")

            # получаем строчку из базы ЛЮДИ с id=id_man , т.е. тот id который передали через GET, внутри кого мы находимся
 #           peoples_select = Peoples.objects.get(id=id_people.id)
 #           peoples_select.otpuska_set.add(new, bulk=False)
 #           all_otpuska = peoples_select.otpuska_set.all()

 #           print("ERR:", form2.cleaned_data['kolvoDney'])





 #       return HttpResponseRedirect('/preview/' + str(id_people.id))
        return HttpResponseRedirect('/tabel/')

    #        return HttpResponse("<h2>OK</h2>")
    #       ot=Otpuska.objects.get_or_create(person__familia=id_people.familia)
    #       ot.save()
    #       print("person ", ot.person)
    #       print("person_id ", ot.person_id)

    #       ot.title_otpusk=request.POST.get("title_otpusk")
    #       ot.nachOtpusk=request.POST.get("nachOtpusk")
    #       ot.kolvoDney=request.POST.get("kolvoDney")

    else:
#        otpuskform = OtpuskForm(init_data_otpusk, initial=init_data_otpusk)
        workdayForm = CreateWorkDayForm(init_data_workday, initial=init_data_workday)
        #    print(otpuskform)
        context = {
#            'otpuskform': otpuskform,
            'id_people': id_people,
            'workdayform': workdayForm
        }

    return render(request, 'main/createworkday.html', context)
#    return render(request, 'main/preview.html', context)
#   return HttpResponse("<h2>OK</h2>")



def edit(request, id):
    id_people = Peoples.objects.get(id=id)
#    d = type(id_people.dateOfBirth)
#    print(d)
    data = {
        'name': id_people.name,
        'familia': id_people.familia,
        'sename': id_people.sename,
        'dolzhnost': id_people.dolzhnost,
        'otdel_people':id_people.otdel_people,
        'female': id_people.female,
        'dateOfBirth': id_people.dateOfBirth,
        'photo': id_people.photo,
        'id': id_people.id,
        'programma': id_people.programma.all()
    }
    editform = EditForm(data, initial=data)
    print('photo', id_people.programma.all())
    if (request.method == "POST"):
#        uform = EditForm(request.POST, request.FILES)
        editform = EditForm(request.POST, initial=data)

        if editform.is_valid():
            allprog=Programm.objects.all()
            aaa=request.POST['programma']
            req_form=editform['programma'].value()
            lst_id_allprog = []
            lst_req_form=[]
            lst_remove=[]
            for i in allprog:
                lst_id_allprog.append(i.id)
            for x in req_form:
                lst_req_form.append(int(x))
            for j in lst_id_allprog:
                if j not in lst_req_form:
                    lst_remove.append(j)

            print("REMOVE_LST:", lst_remove)

            if editform.has_changed():
                id_people.name = request.POST.get("name")
                id_people.familia = request.POST.get("familia")
                id_people.sename = request.POST.get("sename")
                #        id_people.female=request.POST.get("female")
                id_people.dateOfBirth = request.POST.get("dateOfBirth")
                id_people.dolzhnost = Dolzhnost.objects.get(id=request.POST.get("dolzhnost"))

                id_people.otdel_people=Otdels.objects.get(id=request.POST.get("otdel_people"))



                for j in lst_req_form:
                    id_people.programma.add(Programm.objects.get(id=j))
                for k in lst_remove:
                    id_people.programma.remove(Programm.objects.get(id=k))

                #            id_people.photo = request.FILES.get("photo")


            id_people.save()
        #       print(uform["photo"])
        context = {
            'cartochka': id_people,
            'id_otpusknik': id_people.id,
        }
        #return render(request, 'main/preview.html', context)
        return HttpResponseRedirect('/preview/' + str(id_people.id))
    else:

        context = {
            'form': editform,
            'photo': id_people.photo,
            'people': id_people,
             }
        return render(request, 'main/edit.html', context)


def delete(request, id):
    id_people = Peoples.objects.get(id=id)
    print(id_people.name)
    id_people.delete()
    print(id_people.id)
    return HttpResponseRedirect('/')


def proba(request):
    PFormSet=inlineformset_factory(Dolzhnost, Peoples, form=EditForm)
    pp=ProbaForm()
    people = Peoples.objects.all()
    dateform = DateForm(request.POST)
    formset=PFormSet()
    if request.method == "POST":
        ppp=request.POST.get("programma")
        print("PPP:", ppp)
        enterDate=request.POST.get("date")
        print('dateform:', enterDate)
        d = datetime.strptime(enterDate, '%Y-%m-%d')
    else:
        d = datetime.now()
    #d = date(2022,4,10)

    q = Q (konecOtpusk__month=d.month+1) | Q(nachOtpusk__month=d.month-1) | Q(nachOtpusk__month=d.month)
    otpusk_person = Otpuska.objects.filter(q)


    for t in otpusk_person:
        print("otpusk_person:", t.person, t.nachOtpusk.day)
    lengthmonth = calendar.monthrange(d.year, d.month)

    daymonth = []
    weekend = []
    for ii in range(1, lengthmonth[1] + 1):
        daymonth.append(ii)
        holiday = calendar.weekday(d.year, d.month, ii)
        if holiday == 5 or holiday == 6:
            weekend.append(ii)

 #   Kalendar = {'x1': {'aa':11, 'bb':22, 'cc':33}, 'x2':{'dd':44, 'ee':55, 'ff':66}}

    perKalendar={name.person:{iii:'lightgreen' for iii in range(1, lengthmonth[1]+1)} for name in otpusk_person}
    for name in otpusk_person:
        for xx in range(1, lengthmonth[1] + 1):

          #  if (perKalendar[name.person].values() != {'yellow': 'Б'} | perKalendar[name.person][xx] != {'yellow': 'О'} | perKalendar[name.person][xx] != {'yellow': 'X'}):
            holiday = calendar.weekday(d.year, d.month, xx)
            if (holiday == 5 or holiday == 6):
                perKalendar[name.person][xx] = 'red'

            #print('perKalendar', perKalendar[name.person].values())
#    print('Kalendar: ', perKalendar)
    #Kalend = []

    for name in otpusk_person:
      # Kalend.append(name.person)
#        calDict = {iii: 'lightgreen' for iii in range(1, lengthmonth[1] + 1)}

#        print('TypeOtpusk: ', name)
        for xx in range(1, lengthmonth[1] + 1):
#        for xx in range(name.nachOtpusk.day, name.konecOtpusk.day):
            xxx = datetime.date(datetime.strptime(str(d.year) + '-' + str(d.month) + '-' + str(xx), '%Y-%m-%d'))
            if name.nachOtpusk <= xxx < name.konecOtpusk and name.title_otpusk == 'Больничный':
                perKalendar[name.person][xx] = {'yellow':'Б'}
            if name.nachOtpusk <= xxx < name.konecOtpusk and name.title_otpusk == 'Очередной':
                perKalendar[name.person][xx] = {'yellow': 'О'}
            if name.nachOtpusk <= xxx < name.konecOtpusk and name.title_otpusk == 'Без сохранения оплаты':
                perKalendar[name.person][xx] = {'yellow': 'X'}


        #Kalend.append(name.person)
        #Kalend.append(calDict)
#    print('Kalendar: ', perKalendar)

    #   datetime.strptime(new.nachOtpusk, '%Y-%m-%d') #строка в datetime

    context = {
        'people': people,
        'item': True,
        'daymonth': daymonth,
        'weekend': weekend,
        'today': datetime.now(),
        'otpusk': otpusk_person,
        'dateform': dateform,
        'Kalendar': perKalendar,
        'formset': formset,
        'pp':pp
    }

    return render(request, 'main/proba.html', context)


def editOtpusk(request, id_otpusk, title_otpusk):
    d = datetime.now()
    id_otpusk_of_man = Otpuska.objects.get(id=id_otpusk)
    id_people=Peoples.objects.get(id=id_otpusk_of_man.person_id)

    data = {
    'title_otpusk':title_otpusk,
    'nachOtpusk':id_otpusk_of_man.nachOtpusk,
    'kolvoDney' : id_otpusk_of_man.kolvoDney,
    'zayvlenie': id_otpusk_of_man.zayvlenie
    }
#    print('Data:' , data)
    otpuskform = OtpuskForm(data, initial=data)
    #print('OTPUSKFORM', otpuskform)
    if (request.method == "POST"):
        edit_otpusk_form = OtpuskForm(request.POST, request.FILES,  initial=data)
#        edit_otpusk_form = OtpuskForm(request.POST, initial=data)
        if edit_otpusk_form.has_changed():
            print('Change_data:', edit_otpusk_form.changed_data)
            print("id_otpusk_of_man:", type(id_otpusk_of_man.nachOtpusk))
            id_otpusk_of_man.title_otpusk = request.POST.get("title_otpusk")
            id_otpusk_of_man.nachOtpusk = request.POST.get("nachOtpusk")
            id_otpusk_of_man.kolvoDney = request.POST.get("kolvoDney")
            id_otpusk_of_man.konecOtpusk=datetime.strptime(id_otpusk_of_man.nachOtpusk, '%Y-%m-%d')+timedelta(days=int(id_otpusk_of_man.kolvoDney))
            id_otpusk_of_man.zayvlenie = request.FILES.get("zayvlenie")
            listChangeField=edit_otpusk_form.changed_data
            listChangeField.append('konecOtpusk')
       #     print('ListChangeField:', listChangeField)
            id_otpusk_of_man.save(update_fields=listChangeField) #change_data - список измененных пользователем полей, update_field - последовательность полей, которые сохранятся


        for i in range(int(id_otpusk_of_man.kolvoDney)):

 #           print('IIII:', id_otpusk_of_man.nachOtpusk+timedelta(days=i))
 #       for i in range(id_otpusk_of_man.nachOtpusk.day, id_otpusk_of_man.konecOtpusk.day):
 #           print('IIII:', type(id_otpusk_of_man.nachOtpusk+datetime(i, d.month, d.year)))

            ddd=datetime.strptime(id_otpusk_of_man.nachOtpusk, '%Y-%m-%d')+timedelta(days=i)

            writetabel(datetime.date(ddd), id_people)

        contextPlus=drawKalendar(id_otpusk_of_man.person_id, d)

        context={
            'cartochka': id_people,
            'id_otpusknik': id_people.id,
#            'otpusk': Otpuska.objects.filter(person_id=id_people.id),
            }
        contextMonth = creatMonth(d)
        context.update(contextMonth)
        context.update(contextPlus)
        return HttpResponseRedirect('/tabel/')
#        return render(request, 'main/preview.html', context)
    else:
        context={
        'form':otpuskform,
        'photo': id_people.photo,
        'people': id_people
        }

    return render(request, 'main/editOtpusk.html', context)


def creatMonth(d):
#    d = datetime.now()  # создаем список из чисел месяца и список из выходных сб и вс
    daymonth = []
    weekend = []
    lengthmonth = calendar.monthrange(d.year, d.month)
    for ii in range(1, lengthmonth[1] + 1):
        daymonth.append(ii)
        holiday = calendar.weekday(d.year, d.month, ii)
        if holiday == 5 or holiday == 6:
            weekend.append(ii)
    contextMonth={
        'daymonth': daymonth,
        'weekend': weekend,
        'today': datetime.now(),
    }
    return contextMonth


def drawKalendar(id, d):               #принимаем id сотрудника
 #   d = datetime.now()
    lengthmonth = calendar.monthrange(d.year, d.month)
    id_people = Peoples.objects.get(id=id)          # ищем сотрудника по id
    otpusk_person = Otpuska.objects.filter(person_id=id_people.id)       # по фимилии сотрудника выбираем все его отпуска

    # создаем словарь , в котором каждому сотруднику соответствует числа месяца , где указаны возможные отпуска и рабдни

    perKalendar = {name.person: {iii: 'lightgreen' for iii in range(1, lengthmonth[1] + 1)} for name in otpusk_person}
    for name in otpusk_person:
        for xx in range(1, lengthmonth[1] + 1):
            holiday = calendar.weekday(d.year, d.month, xx)
            if (holiday == 5 or holiday == 6):
                perKalendar[name.person][xx] = 'red'

    for name in otpusk_person:
        for xx in range(1, lengthmonth[1] + 1):
            xxx = datetime.date(datetime.strptime(str(d.year) + '-' + str(d.month) + '-' + str(xx), '%Y-%m-%d'))
            if name.nachOtpusk <= xxx < name.konecOtpusk and name.title_otpusk == 'Б':
                perKalendar[name.person][xx] = {'yellow': 'Б'}
            if name.nachOtpusk <= xxx < name.konecOtpusk and name.title_otpusk == 'О':
                perKalendar[name.person][xx] = {'yellow': 'О'}
            if name.nachOtpusk <= xxx < name.konecOtpusk and name.title_otpusk == 'Х':
                perKalendar[name.person][xx] = {'yellow': 'X'}
            if name.nachOtpusk <= xxx < name.konecOtpusk and name.title_otpusk == 'П':
                perKalendar[name.person][xx] = {'yellow': 'П'}
#    print('perKalendar:', perKalendar.keys())

    contextPlus={
        'otpusk': otpusk_person,
        'Kalendar': perKalendar,
    }
    return contextPlus


def del_Otpusk(request, id_otpusk):
    d = datetime.now()
    id_otpusk_of_man = Otpuska.objects.get(id=id_otpusk)
    id_otpusk_of_man.delete()
    id_people = Peoples.objects.get(id=id_otpusk_of_man.person_id)
 #   otpusk = Otpuska.objects.filter(person__familia=id_people.familia)
#    contextPlus = drawKalendar(id_people.id,d)  # вызываем функцию и дополняем словарь context
#    context.update(contextPlus)
#    contextMonth = creatMonth(d)
#    context.update(contextMonth)
    return HttpResponseRedirect('/preview/' + str(id_people.id))

def uploadDoc(request, id_otpusk):
    id_otpusk_of_man = Otpuska.objects.get(id=id_otpusk)
    id_people = Peoples.objects.get(id=id_otpusk_of_man.person_id)


    if (request.method == "POST"):

        id_otpusk_of_man.zayvlenie = request.FILES.get("zayvlenie")
        id_otpusk_of_man.save()
        contextPlus = drawKalendar(id_otpusk_of_man.person_id)
#        print('contextPlus:', contextPlus)
        context = {
            'cartochka': id_people,
            'id_otpusknik': id_people.id,
            #            'otpusk': Otpuska.objects.filter(person_id=id_people.id),
        }
        contextMonth = creatMonth()
        context.update(contextMonth)
        context.update(contextPlus)
        return render(request, 'main/preview.html', context)
    else:
        zayvaform = ZayavaForm()
    context = {
        'zayavaform': zayvaform,
        'photo': id_people.photo,
        'people': id_people
    }

    return render(request, 'main/preview.html', context)

def watchfoto(request, id_otpusk, id_man):
    id_otpusk_of_man = Otpuska.objects.get(id=id_otpusk)
    id_people=Peoples.objects.get(id=id_otpusk_of_man.person_id)
 #   print('watchfoto:', id_otpusk_of_man)
    context={
        'otpusk':id_otpusk_of_man,
    }
    return render(request, 'main/watchfoto.html', context )




def writetabel(view_date, personn):
    otpusk = Otpuska.objects.filter(person_id=personn.id, nachOtpusk__lte=view_date, konecOtpusk__gt=view_date)
    if not otpusk.exists():
        try:
            tabell = Tabel.objects.get(man_id=personn.id, dataTabel=view_date)
        except ObjectDoesNotExist:
            tabell = None
        if tabell != None:
            Tabel.objects.update_or_create(man_id=personn.id, dataTabel=view_date,
                                           defaults={'workTime': tabell.workTime})
        else:
            Tabel.objects.update_or_create(man_id=personn.id, dataTabel=view_date,
                                           defaults={'workTime': '8'})
    else:
        for otp in otpusk:
            if view_date>=otp.nachOtpusk and view_date<otp.konecOtpusk:

                try:
                    tabell = Tabel.objects.get(man_id=personn.id, dataTabel=view_date)
                    tabell.delete()
                except ObjectDoesNotExist:
                    pass
            else:
                try:
                    tabell = Tabel.objects.get(man_id=personn.id, dataTabel=view_date)
                except ObjectDoesNotExist:
                    tabell.workTime='8'
                    tabell.save()


 #               tabel=Tabel.objects.get(man_id=person.id, dataTabel=view_date)
 #               tabel.workTime='8'
 #              tabel.save()






def persontabel(per_id):
    d = datetime.now()
    allPeople = Peoples.objects.filter(id=per_id)
    call_tabel = viewtabel(d, allPeople)
    context = {

    }
    context.update(call_tabel)
    return context



def tabel(request):
    d = datetime.now()
#    d = datetime(2022, 7, 1)
    d_true=d

#   for j in range(6,23):
#        d=datetime(2022,6,j)


    date_d=date(d)
    print('datetime:', date_d)
    allPeople = Peoples.objects.all()
    dateform = DateForm()
    createTabelDay=CreateTabelNewDay(date_d, initial=date_d)
    if(request.method =="POST"):
        viewAtherMonth=DateForm(request.POST, prefix='viewAtherMonth')
        if viewAtherMonth.is_valid():
            print("viewAtherMonth:", viewAtherMonth)
            enterdate = request.POST.get("date")
            d = datetime.strptime(enterdate, "%Y-%m-%d")
            print("DATE:", type(d), d)


        createTabelDay = CreateTabelNewDay(request.POST, prefix='CreateTabelNewDay_form')
        if createTabelDay.is_valid():
            print("createTabelDay:", createTabelDay )

            createEnterDay=request.POST.get("tabelDateWork")
            createEnterDay_date = datetime.strptime(createEnterDay, "%Y-%m-%d")
            for person in allPeople:
                writetabel(createEnterDay_date.date(), person)
        else:
            return HttpResponse('<h1>Че-то не то</h1>')


    holiday = calendar.weekday(d.year, d.month, d.day)

    if(holiday!=5 and holiday!=6 and d_true==d):
        if not (Tabel.objects.filter(dataTabel=d).exists()):
            for person in allPeople:

                writetabel(d.date(), person)
    call_tabel=viewtabel(d, allPeople)
    context={
        'formEnterDate':dateform,
        'emptyWork':0,
        'createTabelDay':createTabelDay
    }
    context.update(call_tabel)

    return render(request, 'main/tabel.html', context)



def viewtabel(view_date, allPeople):

    lengthmonth = calendar.monthrange(view_date.year, view_date.month)

    tabeldata=[]
    contextMonth = creatMonth(view_date)
    for ppl in allPeople:
        tabelReady=Tabel.objects.order_by('dataTabel').filter(man_id=ppl.id, dataTabel__month=view_date.month, dataTabel__year=view_date.year)
        otpusktabel = Otpuska.objects.filter(person_id=ppl.id)
# создаем месяц по дням
        wd_dict = {"{:02d}".format(dm): {'id':' '} for dm in range(1, lengthmonth[1] + 1)}
        chasi_sum = 0
        dni_sum=0
#из объекта tabelready берем сотрудника, в ячейку каждого числа вписываем значение соответствующее дате рабочего дня
        for sotr_work_day in tabelReady:
            wd_dict[datetime.strftime(sotr_work_day.dataTabel, '%d')]={sotr_work_day.id:sotr_work_day.workTime}

            if(type(sotr_work_day.workTime)==int):
                chasi_sum+=sotr_work_day.workTime
                if sotr_work_day.workTime != 0:
                    dni_sum=dni_sum+1

#из объекта otpusktabel берем данные по отпускам и если дата view_date попадает на какой-либо отпуск, то вписываем в словарь
#вид отпуска в соответсвии с датой

        for chislo in range(1, lengthmonth[1] + 1):
            chislo_d=date(view_date.year, view_date.month, chislo)

            for otp in otpusktabel:
 #               if (view_date.date() >= otp.nachOtpusk and view_date.date() <= otp.konecOtpusk):
 #                   wd_dict[datetime.strftime(view_date, '%d')] = otp.title_otpusk
                if (chislo_d >= otp.nachOtpusk and chislo_d < otp.konecOtpusk):
                    wd_dict[datetime.strftime(chislo_d, '%d')] = {otp.id:otp.title_otpusk}



        ddd={'id':ppl.id, 'familia':ppl.familia, 'name':ppl.name, 'dolzhnost':ppl.dolzhnost, 'kalendar':wd_dict,'dni_sum':dni_sum, 'chasi_sum':chasi_sum}
        tabeldata.append(ddd)

    context_tabel={
        'tabel': 'ТАБЕЛЬ',
        'view_date':view_date,

#        'peoples':allPeople,
       'lengthmonth':lengthmonth,
        'tabeldata':tabeldata,
        }

    context_tabel.update(contextMonth)
#    print("allPeople:", context_tabel)
    return context_tabel


def tabeledit(request, id, data_work, data_day, data_month, data_year):
    day_of_tabel=datetime.strptime(data_year+'-'+data_month+'-'+data_day, '%Y-%m-%d')
    allPeople = Peoples.objects.all()
    data = {'worktime': data_work}
    tabeleditForm = TabelForm(data, initial=data)
    tabelreplace = Tabel.objects.get(man_id=id, workTime=data_work, dataTabel=day_of_tabel)

    if (request.method == "POST"):
#        dateform = DateForm(request.POST)

        if(request.POST.get('deleteWork')):
 #           print('Boolen:', request.POST.get('deleteWork'))
            tabelreplace.delete()
        else:
            tabelreplace.workTime = request.POST.get('confirmWork')
            tabelreplace.save()

        call_tabel = viewtabel(day_of_tabel, allPeople)
 #       print("FORM:", dateform)
        context={}
#        context = {'formEnterDate': dateform, }                  #вот тут косяк!!!!
        context.update(call_tabel)
 #       return render(request, 'main/tabel.html', context)
        return HttpResponseRedirect('/tabel/')
    else:
        context = {
            'tabeleditForm': tabeleditForm,
                   }

    return render(request, 'main/tabeledit.html', context)




def probaa(request):
#    man=manForm(request.POST)
    p=Proba.objects.all()
    if request.method=="POST":
        print("REQUEST:", request)
        d=DateForm(request.POST)
#        man = manForm(request.POST)
#        print("VALIDman:", man.is_valid())
#        print("man CLEANED_DATA:", man.cleaned_data)
        print("VALIDdata:", d.is_valid())
        print("date CLEANED_DATA:", d.cleaned_data)
#        n=request.POST.get("name")
#        s=request.POST.get("sename")
#        a=request.POST.get("age")
#        p.create(name=n, sename=s, age=a)
#        print('PROBA:', p)
        context = {
#            'form': man
        }
        return redirect('probaa')
    else:
        context={
#        'form': manForm,
        'dateform': DateForm
    }
    return render(request, 'main/probaa.html', context)


def probatabel(request):
    context={


    }
    return render (request, 'main/tabel2.html', context)




# метод принимает POST запросы

def _get_form(request, formcls, prefix):
    data = request.POST if prefix in request.POST else None
    return formcls(data, prefix=prefix)

class TabelView(TemplateView):
    template_name = 'main/tabel.html'

    # def get(self, request, *args, **kwargs):
    #     d = datetime.now()
    #     data = {
    #         'tabelDateWork': d.date(),
    #     }
    #     createTabelDayForm=CreateTabelNewDay(initial=data, prefix='bform_pre')
    #     EnterDateForm=DateForm(prefix='aform_pre')
    #     context={
    #         'formEnterDate': EnterDateForm ,
    #         'createTabelDay': createTabelDayForm,
    #     }
    #     allPeople = Peoples.objects.all()
    #     call_tabel = viewtabel(d, allPeople)
    #     context.update(call_tabel)
    #     return self.render_to_response(context)



        # методом переопределяем context
    def get_context_data(self, **kwargs):
#        print("KWARGS:", **kwargs)
        context=super(TabelView, self).get_context_data(**kwargs)
#получаем таблицу с данными табеля
        d = datetime.now()
        data={
            'tabelDateWork':d.date(),
        }
        allPeople = Peoples.objects.all()
        call_tabel = viewtabel(d, allPeople)
        context.update(call_tabel)

#добавляем в словарь данные форм
        context['allPeople']=allPeople
        context['formEnterDate']=DateForm(prefix='aform_pre')
        context['createTabelDay']=CreateTabelNewDay(initial=data, prefix='bform_pre')
        context['deleteTabelDay']=DeleteTabelDay_Form(initial=data, prefix='cform_pre')

#        print("CONTEXT:", context['createTabelDay'])
        return context


    def post(self, request, *args, **kwargs):
        context = super(TabelView, self).get_context_data(**kwargs)

        allPeople = Peoples.objects.all()
        d = datetime.now()
        #    d = datetime(2022, 7, 1)
        d_true = d

        aform = _get_form(request, DateForm, 'aform_pre')
        bform = _get_form(request, CreateTabelNewDay, 'bform_pre')
        cform = _get_form(request, DeleteTabelDay_Form, 'cform_pre')
        if aform.is_bound and aform.is_valid():
            d = datetime.strptime(aform['date'].value(), "%Y-%m")

        elif bform.is_bound and bform.is_valid():
            createEnterDay_date = datetime.strptime(bform['tabelDateWork'].value(), "%Y-%m-%d")
            for person in allPeople:
                writetabel(createEnterDay_date.date(), person)
        elif cform.is_bound and cform.is_valid():
            deleteEnterDay_date = datetime.strptime(cform['deltabelDateWork'].value(), "%Y-%m-%d")
            allworkdays = Tabel.objects.filter(dataTabel=deleteEnterDay_date)
            for person_day in allworkdays:
                person_day.delete()
        else:
            return HttpResponse('<h1>Че-то не то</h1>')
            # Process bform and render response
        call_tabel = viewtabel(d, allPeople)
        context = {
            'formEnterDate': aform,
            'emptyWork': 0,
            'createTabelDay': bform,
            'deleteTabelDay':cform
        }
        context.update(call_tabel)

        return self.render_to_response(context)

