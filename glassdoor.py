# setting up the environment
import matplotlib.pyplot as plt
import numpy as np
from urllib.request import urlopen
import re #regex will be needed to extract the txt data

# given a float number, converts to a string with dollar sign
# ex: num2dollar(60000) --> returns '$60,000'
def num2dollar(num):
    num = str(int(num))
    dollar = ''
    count = 0
    for i in range(len(num) - 1, 0, -1):
        count += 1
        digit = num[i]
        dollar = digit + dollar
        if count % 3 == 0:
            dollar = ',' + dollar
    return '$' + num[0] + dollar

# regular expressions to find the strings
jobRegex = re.compile(r'#\d+(.*)')
salaryRegex = re.compile(r'\$(.*)')
ratingRegex = re.compile(r'(\d\.?\d?)/5')

# total number of jobs
numberOfJobs = 50

# data is stored in GlassDoorData.txt
tempTxt = urlopen('https://raw.githubusercontent.com/htutk/glassdoorAnalysis/master/GlassDoorData.txt')
tempTxt = tempTxt.readlines()

txt = []
for line in tempTxt:
    txt.append(line.decode('ascii'))  #readlines return binary-string values

# Initializing lists
jobs, salaries, ratings, jobOpenings = [], [], [], []

# retrieving data
count = 0
while count <= len(txt):
    jobMo = jobRegex.search(txt[count])
    jobs.append(jobMo.group(1))

    salaryMo = salaryRegex.search(txt[count+1])
    salary = salaryMo.group(1)
    salary = ''.join(salary.split(','))
    salaries.append(float(salary))

    ratingMo = ratingRegex.search(txt[count+2])
    ratings.append(float(ratingMo.group(1)))

    jobOpening = txt[count+3].rstrip()
    jobOpening = ''.join(jobOpening.split(','))
    jobOpenings.append(int(jobOpening))

    count += 5  # go to the next fifth line (every job has five lines each)

# mean values
avgSalary = sum(salaries)/numberOfJobs
avgRating = sum(ratings)/numberOfJobs
avgJobOpening = sum(jobOpenings)/numberOfJobs

# xTicks parameters for salary
minSalary = 40000
maxSalary = 160000
salaryInterval = 20000

# xTicks2 parameters for ratings
minRating = 3.25
maxRating = 5
ratingInterval = 0.25

xPos = np.arange(0, numberOfJobs)

plt.figure(1)
plt.barh(xPos, list(reversed(salaries)))  # to make the top-ranked job at the top
plt.yticks(xPos, list(reversed(jobs)))

ax = plt.twinx()
ax.plot([avgSalary for i in range(numberOfJobs)], xPos, color='r', label='average salary')
ax.yaxis.set_visible(False)     # set the copied yaxis (which shows 0 - 50) invisible

plt.xlim([minSalary, maxSalary])
# xTicks is for salaries
xTicks = sorted(np.append(np.arange(minSalary, maxSalary, salaryInterval), avgSalary))
plt.xticks(xTicks, [num2dollar(x) for x in xTicks])
plt.xlabel('Salary')
plt.ylabel('Ranked jobs in order')
plt.title('Top ranked jobs and their salaries')
plt.legend()

plt.figure(2)
plt.barh(xPos, list(reversed(ratings)))
plt.yticks(xPos, list(reversed(jobs)))

ax2 = plt.twinx()
ax2.plot([avgRating for i in range(numberOfJobs)], xPos, color='r', label='average rating')
ax2.yaxis.set_visible(False)

# xTicks2 is for ratings
xTicks2 = sorted(np.append(np.arange(minRating, maxRating, ratingInterval), avgRating))
xTicks2 = [round(xTicks2[i],2) for i in range(len(xTicks2))]

plt.xlabel('Ratings')
plt.ylabel('Ranked jobs in order')
plt.xticks(xTicks2)
plt.xlim([minRating, maxRating])
plt.title('Top ranked jobs and their ratings')
plt.legend()

# store the jobs and their salaries/ratings as dictionaries
salaryDict = {}
ratingDict = {}

# sorted outcomes
jobs_sorted_by_salary = []
salaries_sorted = []
ratings_sorted = []

for job in jobs:
    salaryDict[job] = salaries[jobs.index(job)]

# array reference is faster this way
for job in jobs:
    ratingDict[job] = ratings[jobs.index(job)]

# sorting dictionaries by their items values
salaryDict_sorted = list(sorted(salaryDict.items(), key=lambda kv: kv[1]))
ratingDict_sorted = list(sorted(ratingDict.items(), key=lambda kv: kv[1]))

# store the sorted values in lists
# pair = (job, salary/job)
for pair in salaryDict_sorted:
    jobs_sorted_by_salary.append(pair[0])
    salaries_sorted.append(pair[1])

for pair in ratingDict_sorted:
    ratings_sorted.append(pair[1])


plt.figure(3)
plt.barh(xPos, salaries_sorted)
plt.yticks(xPos, jobs_sorted_by_salary)

ax3 = plt.twinx()
ax3.plot([avgSalary for i in range(numberOfJobs)], xPos, color='r', label='average salary')
ax3.yaxis.set_visible(False)

plt.xlim([minSalary, maxSalary])
plt.xticks(xTicks, [num2dollar(x) for x in xTicks])
plt.xlabel('Salary')
plt.ylabel('Ranked jobs by salaries')
plt.title('Jobs ranked by salaries')
plt.legend()

plt.figure(4)
plt.barh(xPos, ratings_sorted)
plt.yticks(xPos, jobs_sorted_by_salary)

ax4 = plt.twinx()
ax4.plot([avgRating for i in range(numberOfJobs)], xPos, color='r', label='average rating')
ax4.yaxis.set_visible(False)

plt.xlabel('Ratings')
plt.ylabel('Ranked jobs by ratings')
plt.xticks(xTicks2)
plt.xlim([minRating, maxRating])
plt.title('Jobs ranked by ratings')
plt.legend()

plt.figure(5)
plt.scatter(list(reversed(salaries)), xPos, s=(np.array(jobOpenings)/avgJobOpening) * 100, alpha=0.8)
plt.yticks(xPos, list(reversed(jobs)))
plt.xticks(xTicks, [num2dollar(x) for x in xTicks]) # this is inverted

ax5 = plt.twinx()
ax5.plot([avgSalary for i in range(numberOfJobs)], xPos, color='r', label='average salary', alpha=0.8)
ax5.yaxis.set_visible(False)

plt.ylabel('Top jobs ranked in order (left to right)')
plt.xlabel('Salary')
plt.title('Top ranked jobs and their salaries (scaled by job openings)')
plt.legend()
plt.show()
