from bs4 import BeautifulSoup
import requests
import re
import pandas as pd



### Use Request library to download the web pages
#1. Nova Scotia
#2. New Brunswick
#3. Newfoundland and Labrador
#4. Prince Edward Island
target_url = "https://www.jobbank.gc.ca/jobsearch/jobsearch?fn=2173&term=software+engineer&sort=M&fprov=NB&fprov=NL&fprov=NS&fprov=PE"

response = requests.get(target_url,auth=('madan.chakshu@gmail.com','System123#'))
# print(response. status_code)

page_content = response.text
# print(page_content[:1000])

with open('webpage.html', 'w') as f:
    f.write(page_content)

### Use Beautiful Soup to parse and extract the information

doc =  BeautifulSoup(page_content, 'html.parser')
# print(doc)
job_title_class = 'noctitle'
span_tag = doc.find_all('span', {'class': job_title_class})
# print(len(span_tag))
# print(span_tag)

business_class = 'business'
li_business_tag = doc.find_all('li', {'class': business_class})
# print(len(li_business_tag))
# print(li_business_tag)

location_class = 'location'
li_loc_tag = doc.find_all('li', {'class': location_class})
# print(len(li_loc_tag))
# aa = li_loc_tag[0].text.split()
# print(aa)

salary_class = 'salary'
li_sal_tag = doc.find_all('li', {'class': salary_class})
# print(len(li_sal_tag))
# print(li_sal_tag)

# topic_title_tag0 = span_tag[0]
# # print('https://www.jobbank.gc.ca'+topic_title_tag0.parent.parent['href'])
final_list =[]
job_title_list = []
business_list = []
location_of_job_list = []
salary_job_list = []
link_of_job_list = []
# # for job_tag, business_tag, loc_tag, sal_tag in span_tag, li_business_tag, li_loc_tag, li_sal_tag:
for job_tag, business_tag, loc_tag, sal_tag in zip(span_tag,li_business_tag,li_loc_tag, li_sal_tag):
    final_list.append([job_tag.text.strip(), business_tag.text.strip(), ' '.join([elm for elm in loc_tag.text.split()]), ' '.join([elm for elm in sal_tag.text.split()]), 'https://www.jobbank.gc.ca'+job_tag.parent.parent['href']])
    job_title_list.append(job_tag.text.strip())
    business_list.append(business_tag.text.strip())
    location_of_job_list.append(' '.join([elm for elm in loc_tag.text.split()]))
    salary_job_list.append(' '.join([elm for elm in sal_tag.text.split()]))
    link_of_job_list.append('https://www.jobbank.gc.ca'+job_tag.parent.parent['href'])

# print(job_title_list)
# print(business_list)
# print(location_of_job_list)
# print(salary_job_list)
# print(link_of_job_list)

topic_dic = {
    'TITLE': job_title_list,
    'COMPANY NAME': business_list,
    'LOCATION': location_of_job_list,
    'SALARY': salary_job_list,
    'URL': link_of_job_list
}

topic_df = pd.DataFrame(topic_dic)
# print(topic_df)

topic_df.to_csv('JOB_SEARCH_RESULT.csv', index=None)

print(topic_df[3])