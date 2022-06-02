
# LinkedIn REST Unofficial API (python)

A simple unofficial LinkedIn python api providing basic LinkedIn functionality.
Programmatically find jobs and search for/connect with other users with python 'requests'.


## Setup

Login to LinkedIn in your browser and use a tool like the "Get cookies.txt" chrome addon to save a Netscape format cookie file. 
This file path will be referenced in instantiations of the LinkedInApi class.


## Usage/Examples

Initialization:
```python
import LinkedInApi from linkedin

api = LinkedInApi('cookies.txt')
```
Job Search: (returns a list of jobs)
```python
job = api.search_jobs('software engineer', location='Palo Alto', page=0)[0]

# {
#     'companyid': '112834',
#     'jobid': 3275182739,
#     'location': 'Palo Alto, CA',
#     'remote': False,
#     'salary': '$125k - $150k',
#     'time_posted': 1654113929000,
#     'title': 'Distributed Systems Engineer'
# }
```
People Search: (returns a list of people)
```python
person = api.search_people('CEO', companyid='112834', page=0)

# {
#     'link': 'https://www.linkedin.com/in/richard-hendricks-82872349',
#     'name': 'Richard Hendricks',
#     'title': 'Founder and CEO of Pied Piper',
#     'urnfsd': 'ACoAACBs9h4BHKvASi4DnsU4W9fn02mTs8wuk5nvJU',
#     'userid': 'richard-hendricks-82872349'
# }
```
Get User Info: (returns user info)
```python
info = api.get_user_info(person['userid'])

# {
#     'first_name': 'Richard',
#     'last_name': 'Hendricks',
#     'pfp100': 'https://media-exp1.licdn.com/dms/image/03AQHftDeZQftQHftMe/profile-displayphoto-shrink_100_100/0/1898320000009?e=144571200&v=beta&t=vF1EaA8FMkT_RTrIA-q_B7RZ-svj6Hgux0FbA',
#     'pfp200': 'https://media-exp1.licdn.com/dms/image/03AQHftDeZQftQHftMe/profile-displayphoto-shrink_200_200/0/1898320000009?e=144571200&v=beta&t=Jix-vbQlA8FMkT_RTrIA8QkA8FMkT_RTrIAuM',
#     'pfp400': 'https://media-exp1.licdn.com/dms/image/03AQHftDeZQftQHftMe/profile-displayphoto-shrink_400_400/0/1898320000009?e=144571200&v=beta&t=gR5SLOPyoc-j6Hgux0diiizHQPTjBm5xuwss6',
#     'pfp800': 'https://media-exp1.licdn.com/dms/image/03AQHftDeZQftQHftMe/profile-displayphoto-shrink_800_800/0/1898320000009?e=144571200&v=beta&t=FVxBXGaUkQKjBm5Pyoc-j6HguxeImMY89vKf0',
#     'student': False,
#     'title': 'Founder and CEO of Pied Piper',
#     'urnfsd': 'ACoAACBs9h4BHKvqBYilQKYA2502mTs8kfbqvJU'
# }
```
Connect with User:
```python
message = """
Richard, congratulations. 
It's your very close friend Jian-Yang, 
and I would like you to give me free shares of Pied Piper.
"""

api.connect_with_user(info['urnfsd'], message)
```



## Future Improvements

I plan to add further functionality to get_user_info() when/if I can find more endpoints.


