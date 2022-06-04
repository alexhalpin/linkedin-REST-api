import requests
import http.cookiejar as cookielib


class LinkedInApi:
    def __init__(self, cookiepath):
        """
            instantiate a linkedinapi object
            :param cookiepath: path to cookies.txt (netscape)
            :type cookiepath: string
        """
        cookies = cookielib.MozillaCookieJar(cookiepath)
        cookies.load()
        jsessionid = requests.utils.dict_from_cookiejar(cookies)['JSESSIONID'][1:-1]
        headers = {
              'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'
            , 'csrf-token': jsessionid  # this is JSESSIONID cookie
            , 'accept-encoding': 'gzip, deflate, br'
            , 'accept-language': 'en-US,en;q=0.9'
            , 'accept': 'application/vnd.linkedin.normalized+json+2.1'
            , 'referer': 'https://www.linkedin.com/jobs/search/?geoId=103644278&keywords=software&location=United%20States'
            , 'x-li-deco-include-micro-schema': 'true'
            , 'x-li-lang': 'en_US'
            # ,'x-li-page-instance': 'urn:li:page:d_flagship3_search_srp_jobs;z8Y2IPCvTn+64syUoMOoOg=='
            # ,'x-li-track': '{"clientVersion":"1.10.5161","mpVersion":"1.10.5161","osName":"web","timezoneOffset":-4,"timezone":"America/New_York","deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":1.25,"displayWidth":1920,"displayHeight":1080}'
            , 'x-restli-protocol-version': '2.0.0'
        }
        self.cookies = cookies
        self.headers = headers

    def get_request(self, url):
        """
            get request using linkedin cookies
            :param url: url
            :type url: string
        """
        return requests.get(url, headers=self.headers, cookies=self.cookies)

    def search_jobs(self, keywords, location='', page=0):
        """
            get a list of jobs from search terms
            :param location: location
            :type location: string
            :param keywords: search keywords
            :type keywords: string
            :param page: search results page
            :type page: int
            :rtype dictionary
        """
        base_url = """
        https://www.linkedin.com/voyager/api/search/hits?decorationId=com.linkedin.voyager.deco.jserp.WebJobSearchHitWithSalary-25&count=50&filters=List(locationFallback-%3E{location},resultType-%3EJOBS)&keywords={keywords}&q=jserpFilters&queryContext=List(primaryHitType-%3EJOBS,spellCorrectionEnabled-%3Etrue)&start={start}&topNRequestedFlavors=List(HIDDEN_GEM,IN_NETWORK,SCHOOL_RECRUIT,COMPANY_RECRUIT,SALARY,JOB_SEEKER_QUALIFIED,PRE_SCREENING_QUESTIONS,SKILL_ASSESSMENTS,ACTIVELY_HIRING_COMPANY,TOP_APPLICANT)"""
        formatted_url = base_url.format(location=location, keywords=keywords, start=page*50)
        res = requests.get(formatted_url, headers=self.headers, cookies=self.cookies)
        data = res.json()['included']

        job_list = []
        for job in data:

            if len(job['entityUrn']) != 42:
                continue

            j = {}
            j['title'] = job['title']
            j['jobid'] = job['jobPostingId']
            j['remote'] = job['workRemoteAllowed']
            j['location'] = job['formattedLocation']
            j['companyid'] = job['companyDetails']['company'][29:]
            j['salary'] = job['formattedSalaryDescription']
            j['time_posted'] = job['listedAt']

            job_list.append(j)

        return job_list

    def search_people(self, keywords='', company_id='', page=0):
        """
            get a list of people from search terms
            :param keywords: search keywords
            :type keywords: string
            :param company_id: optional company id
            :type company_id: string
            :param page: search results page
            :type page: int
            :rtype dictionary
        """
        base_url = """
        https://www.linkedin.com/voyager/api/search/dash/clusters?decorationId=com.linkedin.voyager.dash.deco.search.SearchClusterCollection-153&origin=GLOBAL_SEARCH_HEADER&q=all&query=(keywords:{keywords},flagshipSearchIntent:SEARCH_SRP,queryParameters:(currentCompany:List({company_id}),resultType:List(PEOPLE)),includeFiltersInResponse:false)&start={start}"""
        formatted_url = base_url.format(keywords=keywords, company_id=company_id, start=page*10)
        res = requests.get(formatted_url, headers=self.headers, cookies=self.cookies)
        res = res.json()
        data = res['included']

        person_list = []
        for person in data:

            if 'trackingUrn' not in person or person['trackingUrn'] == 'urn:li:member:headless':
                continue

            p = {}
            p['name'] = person['title']['text']
            p['urnfsd'] = person['image']['attributes'][0]['detailDataUnion']['profilePicture'][19:]
            p['link'] = person['navigationUrl'].split('?')[0]
            p['userid'] = person['navigationUrl'].split('?mini')[0][28:]

            if person['primarySubtitle'] is not None:
                p['title'] = person['primarySubtitle']['text']

            person_list.append(p)

        return person_list

    def get_user_info(self, userid):
        """
            get user information
            :param userid: user id (linkedin.com/in/{userid})
            :type userid: string
            :rtype dictionary
        """
        url = """
        https://www.linkedin.com/voyager/api/identity/dash/profiles?q=memberIdentity&memberIdentity={userid}"""
        formatted_url = url.format(userid=userid)
        res = requests.get(formatted_url, headers=self.headers, cookies=self.cookies)
        data = res.json()['included'][0]

        p = {}
        p['first_name'] = data['firstName']
        p['last_name'] = data['lastName']
        p['title'] = data['headline']
        p['student'] = data['student']
        p['urnfsd'] = data['entityUrn'][19:]

        email = data['emailAddress']
        if email is not None:
            p['emailAddress'] = email['emailAddress']

        profile_pic = data['profilePicture']
        if profile_pic is not None:
            pfp = profile_pic['displayImage']['artifacts']
            base = profile_pic['displayImage']['rootUrl']
            p['pfp100'] = base+pfp[0]['fileIdentifyingUrlPathSegment']
            p['pfp200'] = base+pfp[1]['fileIdentifyingUrlPathSegment']
            p['pfp400'] = base+pfp[2]['fileIdentifyingUrlPathSegment']
            p['pfp800'] = base+pfp[3]['fileIdentifyingUrlPathSegment']

        return p

    def connect_with_user(self, urnfsd, message=''):
        """
            connect with user
            :param urnfsd: urnfsd of user
            :type urnfsd: string
            :param message: message to send with connection request
            :type message: string
            :rtype dictionary
        """
        url = """
        https://www.linkedin.com/voyager/api/voyagerRelationshipsDashMemberRelationships?action=verifyQuotaAndCreate"""
        payload = {
            'inviteeProfileUrn': 'urn:li:fsd_profile:'+urnfsd,
        }
        if message != '':
            payload['customMessage'] = message
        return requests.post(url, headers=self.headers, cookies=self.cookies, json=payload)

    def get_company_info(self, companyid):
        """
            get company information
            :param companyid: company id (linkedin.com/in/{companyid}) (unlike userid this is a number)
            :type companyid: string
            :rtype dictionary
        """
        url = """
        https://www.linkedin.com/voyager/api/voyagerOrganizationDashCompanies/{companyid}"""
        formatted_url = url.format(companyid=companyid)
        res = requests.get(formatted_url, headers=self.headers, cookies=self.cookies)
        data = res.json()['data']

        c = {}
        c['name'] = data['name']
        c['url'] = data['url']

        return c