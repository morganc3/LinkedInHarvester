# LinkedInHarvester
Scrapes names from LinkedIn companies and creates a list of email addresses from them.


# How to use
Usage: python harvest.py COMPANY_ID DOMAIN COOKIE_FILE
  
 The company ID will be the value you see when you browse to the company's employees in LinkedIn, example shown below:
 
 First, click here on the company page to see the employees:
 
 ![alt text](https://raw.githubusercontent.com/morganc3/LinkedInHarvester/master/employees_link.png) 
 
 ![alt text](https://raw.githubusercontent.com/morganc3/LinkedInHarvester/master/company_id.png)
 
 
 The domain will be the domain you would like the generated email addresses to have.
 
 There are two cookies that matter for LinkedIn requests. One is a csrf token, and one is a session identifier. 
  The csrf token cookie is called "JSESSIONID" and will have a value similar to the following: "ajax:239842398432".
  The session identifier cookie is called "li_at" and will have a long string value. 
  Prior to running harvest.py, place these two cookie values in a text file in the following format:
  ![alt text](https://raw.githubusercontent.com/morganc3/LinkedInHarvester/master/cookie_example.png)
    
  Keep in mind there should be a newline after both cookie values!
      
  
