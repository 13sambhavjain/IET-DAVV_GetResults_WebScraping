import requests
from bs4 import BeautifulSoup
import csv

# params = {
#             'rollno': '20C' + str(6000 + 154),
#             'typeOfStudent': 'Regular'
#         }
# r = requests.get(url, params=params)
# soup = BeautifulSoup(r.content, 'html.parser')
# s = soup.find('table')
# # content = s.find_all('b')
# lines = s.find_all('b')
# for line in lines:
#     print(line.text)
# print(lines[3].text)
# print(soup.prettify())
# print(content)
# url = 'http://results.ietdavv.edu.in/DisplayStudentResult'#?rollno=20C6126&typeOfStudent=Regular'
# res = []
# year_branch = '20C'
# semester = 6
# k = semester*1000
# c = 0
# d = 0
# for i in range(1,186):
#     try:
#         params = {
#             'rollno': year_brach + str(k + i),
#             'typeOfStudent': 'Regular'
#         }
#         r = requests.get(url,params=params)
#         soup = BeautifulSoup(r.content, 'html.parser')
#         s = soup.find('table')
#         lines = s.find_all('b')
#         lis = []
#         for line in lines[3:24]:
#             lis.append(line.text)
#         res.append(lis)
#         d += 1
#     except:
#         try:
#             params = {
#                 'rollno': '21C' + str(k + i),
#                 'typeOfStudent': 'Regular'
#             }
#             r = requests.get(url,params=params)
#             soup = BeautifulSoup(r.content, 'html.parser')
#             s = soup.find('table')
#             lines = s.find_all('b')
#             lis = []
#             for line in lines[3:24]:
#                 lis.append(line.text)
#             res.append(lis)
#             c += 1
#         except:
#             res.append(['error'])
# f = f'{year_branch}{semester}sem_results.csv'
# with open(f, 'w') as csvfile: 
#     # creating a csv writer object 
#     csvwriter = csv.writer(csvfile) 
#     fields = [
#         'EnrollmentNumber', 'RollNo', 'Name',
#         # 'Computer Graphics & Visualization Theory', 'Computer Graphics & Visualization Practical',
#         # 'Design and Analysis of Algorithm Theory', 'Design and Analysis of Algorithm Practical',
#         # 'Compiler Techniques Theory', 'Compiler Techniques ',
#         # 'Data Warehousing & Mining Theory', 'Data Warehousing & Mining Practical',
#         # 'Wireless and Mobile Networks Theory', 'Wireless and Mobile Networks Practical',
#         # 'Computer Graphics Lab Theory', 'Computer Graphics Lab Practical',
#         # 'Comprehensive Viva - Vi Theory', 'Comprehensive Viva - Vi Practical',
#         # 'Professional Development Theory', 'Professional Development Practical',
#         # 'Result', 'SGPA'
#     ]
#     # writing the fields 
#     csvwriter.writerow(fields) 
        
#     # writing the data rows 
#     csvwriter.writerows(res)
# print(c, d)


def get_results(semester: int, year_in_roll = 20, branch_in_roll = 'C', url = 'http://results.ietdavv.edu.in/DisplayStudentResult',start = 1, end = 186):
    
    #?rollno=20C6126&typeOfStudent=Regular'
    listOfAllResults = []
    year_branch_inRoll = str(year_in_roll) + branch_in_roll
    lateral_year_branch_inRoll = str(year_in_roll + 1) + branch_in_roll
    sem_inRoll = semester*1000
    normal_success = 0
    lateral_success = 0
    getSubjects = True
    fields = [
            'EnrollmentNumber', 'RollNo', 'Name'
    ]
    for i in range(start,end+1):
        rollNo = year_branch_inRoll + str(sem_inRoll + i)
        try:
            parameters_for_url = {
                'rollno': rollNo,
                'typeOfStudent': 'Regular'
            }
            response = requests.get(url, params=parameters_for_url)
            responseParser = BeautifulSoup(response.content, 'html.parser')
            PrimaryTag = responseParser.find('table')
            listOfAllSecondaryTags = PrimaryTag.find_all('b')
            listOfDetails = []
            for secondaryTag in listOfAllSecondaryTags[3:24]:
                listOfDetails.append(secondaryTag.text)
            listOfAllResults.append(listOfDetails)
            normal_success += 1
            if getSubjects:
                lines = PrimaryTag.find_all('table')[3].find_all('td')
                for line in lines[::4]:
                    fields.append(line.text + ' Theory')
                    fields.append(line.text + ' Practical')
                getSubjects = False
        except:
            rollNo = lateral_year_branch_inRoll + str(sem_inRoll + i)
            try:
                parameters_for_url = {
                    'rollno': rollNo,
                    'typeOfStudent': 'Regular'
                }
                response = requests.get(url,params=parameters_for_url)
                responseParser = BeautifulSoup(response.content, 'html.parser')
                PrimaryTag = responseParser.find('table')
                listOfAllSecondaryTags = PrimaryTag.find_all('b')
                listOfDetails = []
                for secondaryTag in listOfAllSecondaryTags[3:24]:
                    listOfDetails.append(secondaryTag.text)
                listOfAllResults.append(listOfDetails)
                lateral_success += 1
            except:
                listOfAllResults.append(['error for ', rollNo, '---------------------'])
    #create csv file
    fields.append('Result')
    fields.append('SGPA')
    
    file = f'{semester}sem_results.csv'
    with open(file, 'w') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
        # writing the fields 
        csvwriter.writerow(fields) 
            
        # writing the data rows 
        csvwriter.writerows(listOfAllResults)
    return (normal_success, lateral_success)

def try1():
    # params = {
    #     'rollno': '20C' + str(k + i),
    #     'typeOfStudent': 'Regular'
    # }
    r = requests.get('http://results.ietdavv.edu.in/DisplayStudentResult?rollno=20C6126&typeOfStudent=Regular')
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find('table')
    lines = s.find_all('table')[3].find_all('td')
    subjects = []
    for line in lines[::4]:
        subjects.append(line.text)
    # lines = s.find_all('table')[3].find_all('font')
    # subjects = []
    # for line in lines[4::2]:
    #     print(line.text)
# #             c += 1
def main():
    print(get_results(6))
    # try1()

if __name__ == '__main__':
    main()
