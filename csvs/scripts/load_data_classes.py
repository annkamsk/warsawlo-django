import csv
import re

from search.models import PublicSchool, HighSchoolClass, ExtendedSubject, Statistics, Language


def load():
    with open('csvs/Punkty 2018_2019 -  .csv', newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        row_number = 0
        for row in csv_reader:
            row_number += 1
            if row_number > 4 and row[1] == 'LO' and 'Branżowa' not in row[2]:
                name = row[2].strip()
                school = PublicSchool.objects.get(school_name=name)
                print(school.school_name + ':')
                hss = HighSchoolClass()
                hss.school = school.id
                class_name = row[3]
                # first part of name eg. 1A humanistyczna
                hss.name = re.sub('[\\[]', '', re.findall(r'.+\[', class_name)[0]).strip()
                # 2018-2019
                hss.year = range(2018, 2020)

                # class has only one type that is written in brackets eg. [O]
                hss.type = re.sub('[\\[\\]]', '', re.findall(r'\[.+\]', class_name)[0])
                hss.save()
                # subjects are placed between the type and list of languages eg. [O] mat-fiz (ang,niem)
                subjects = re.sub('[\\]\\(]', '', re.findall(r'\].+\(', class_name)[0]).strip().split('-')

                for s in subjects:
                    subject = ExtendedSubject()
                    subject.name = s
                    subject.high_school_class = hss
                    subject.save()

                # stats
                st = Statistics()
                st.high_school_class = hss
                stats = {'min': row[4].strip(), 'avg': row[5].strip(), 'max': row[6].strip()}
                for (k, v) in stats.items():
                    if 'laur' in v.lower():
                        stats[k] = Statistics.LAUREAT
                    elif '**' in v:
                        st.with_competency_test = True
                        stats[k] = re.sub('\\*', '', v)
                    elif '*' in v:
                        st.only_sports_test = True
                        stats[k] = re.sub('\\*', '', v)

                st.points_min = stats['min']
                st.points_avg = stats['avg']
                st.points_max = stats['max']
                st.save()

                # languages are placed in brackets eg. (ang*-niem*,fran*), sometimes it's not the first bracket
                # before the '-' are first foreign language choices, after are second foreign language choices
                # '*' by first foreign language means choice of level P or R
                # '*' by second foreign language means choice of level 0 or P
                brackets = re.findall(r'\([\w,\\*-]+\)', class_name)
                languages = re.sub('[\\(\\)]', '', brackets[len(brackets) - 1]).strip().split('-')
                first = languages[0].split(',')
                second = languages[1].split(',')
                languages = []
                for l in first:
                    lang = Language()
                    lang.name = re.sub('\\*', '', l)
                    lang.nr = 1
                    lang.high_school_class = hss
                    if 'Dwujęzycznymi' in name and st.with_competency_test:
                        lang.is_bilingual = True
                    elif '*' in l:
                        lang.multiple_levels = True
                    languages.append(lang)

                for l in second:
                    lang2 = Language()
                    lang2.name = re.sub('\\*', '', l)
                    lang2.nr = 2
                    lang2.high_school_class = hss
                    if '*' in l:
                        lang2.multiple_levels = True
                    languages.append(lang2)
                for l in languages:
                    l.save()





