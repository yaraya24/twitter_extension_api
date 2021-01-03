# Twitter - Extension (Scheduler)



## About 

A web application using the Flask framework that emulates twitter and it's character limited blogging and social media service. Currently, the application has the feature to:

- Create an account
- Log in and out securely
- View all the tweets
- Post a tweet with hashtags, a schedule time and comment
- Follow and unfollow other users
- Edit your account details
- Edit and delete your tweets and comments if authorised
- REST API endpoints to access and interact with the data and application

## Getting Started

#### Requirements

* Python3
* Database (Postgres)
* Python-Pip
* Python-Venv

#### Installation:

```bash
git clone https://github.com/yaraya24/twitter_extension_api.git
cd twitter_extension_api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=main.py


```

#### Database Requirements:

If this application is to be cloned and operated locally, you will be required to create a Postgres database and configure the application accordingly. 

If using Postgresql, the DB URI will require the username, password, port number, hostname and database name.

***eg. postgresql+psycopg2://admin:admin@localhost:5432/twitter_api***

Once created, update the configuration files with in the .env file.

Finally, create the database from the migrations folder by

```
flask db upgrade
```



##### Populating the Database:

For testing purposes, you can populate a database using 

```
flask db_commands seed
```

##### Running the Web Application:

Once the database and all the configuration files have been set up, a development version of the web application can be run using

```
flask run
```



#### API instructions:

##### Logging in:

You can login to the application if you have an account by making a POST request to the endpoint http://localhost:/api/login and providing your username and password in JSON format.

```
{
	"username":"admin",
	"password":"admin"
}
```

A JWT token will be provided as the response which you can then add to the authentication header in all subsequent requests.

##### Available endpoints:

All tweets: */api/tweets/all*

A specific tweet: */api/tweets/{tweet id}*

All users: */api/users/all*

A specific user: */api/users/{user id}*

All comments: */api/comments/all*

Posting a tweet: */api/post_tweet*

```
Posting a tweet

{
	tweet_text = 'the tweet text body',
	schedule_time = 'YYYY-MM-DD' (optional)
}
```

Deleting a tweet: */api/delete_tweet/{tweet_id}*

Access to all the data: */api/all_data*

Statistics on the data: */api/statistics*

### Analyzing Privacy and Security in the system:

Privacy and security within an information system is of paramount importance and the system that has been designed reflects this. There is an obligation, both in legally and ethically, that user data is both protected from malicious attacks and system design failures that leak private information. Though there is an obvious link between obligations of privacy and security, the two problems are handled differently within this system.

##### Privacy:

When users access the system, they are providing sensitive and personal information and expect that the information being provided is kept away from unauthorized people. The Twitter-Extension application endeavors to do this by authenticating all users if they are accessing sensitive information. The Flask Login and Flask_JWT frameworks accomplish this by requiring users to provide their credentials when accessing certain pages. Furthermore, when editing user information or editing a tweet, not only does the user have to be logged in, it is solely the authorized user that can access that information (The user that created the tweet/comment). 

Furthermore, validation checks within the creation of an account ensures that the system cannot mistake a user for another user to leak private information. All users are uniquely identified with a user id and all emails and username have to be unique. The validations persist even when a user edit's their profile.

In the context of this Twitter Extension application, the information that would be considered 'sensitive' would be a user's email address and a scheduled tweet. For obvious reasons, a user that has scheduled a tweet doesn't want that tweet to be revealed to any unauthorized users until it is published. In order to protect this, only users who are logged in and  looking at their solely their profile can view the scheduled tweets.

Lastly, comprehensive testing will minimize the risk of privacy breaches. Utilizing frameworks and implementing secure system design will not be effective if bugs persist within the application. By implementing comprehensive tests, we can ensure that the system runs the way it is intended.

##### Security:

In the same vein as privacy, the security of the information system is incredibly important and utilising system design techniques and Python frameworks, I have attempted to mitigate the risks. 

Firstly, when using relational databases like Postgres, there is a risk of SQL injections being used to attack the system. With SQL injections, if the data is not validated and sanitized, a malicious attacker is able to access the database and all the sensitive information within it including passwords and emails. Utilising an Object Relational-Mapper like SQL Alchemy mitigates against this by abstracting away from RAW SQL and allowing the ORM to compose SQL. As the system is never actually interpreting SQL, a malicious attacker should not be able to inject malicious SQL queries. However, as with all security, nothing is 100% secure and so utilising system design principles, we need to sanitize user data to ensure it isn't malicious. This has been done with validation checks to ensure that the data being provided is what the system expects and thus safe.

The use and safe storage of passwords is also key to ensuring the system is secure from attackers. Requiring users to have passwords that have a minimum complexity assists with the security of the entire system as it is much more difficult to gain access to even one user's account. [This is not implemented in this application for the time being to allow Coder Academy to easily access and test the site]. Furthermore, in the instance that the database is hacked, long and complicated passwords would be very difficult to crack as opposed to simpler ones. The storage of passwords is also important and this system doesn't store the password in plain text, rather it hashes the password upon creation and stores that in the database. System administrators aren't able to access the plain text password as the system is designed to generate an error if a password is requested.

Lastly, as this application has API endpoints, authenticating a user requires the user to provide their username and password in JSON format. This application utilises HTTP which means that the information being sent isn't encrypted. The optimal solution is to implement HTTPS which requires an SSL certificate to be issued. As that cannot be achieved at this time, a compromise is to use JSON Web Tokens (JWTs) to minimize the amount of times a user provides their username and password as they can just provide the token once they have authenticated themselves at least once.



### Professional, Ethical, and Legal Obligations:

##### Professional:

As a developer and the designer of the system, I have a professional obligation that the code has sufficient testing and that unintended bugs have been minimized. In addition to this, ensuring that system can handle the intended amount of traffic (depends on the system requirements) and that this is also tested with load testing applications. There is also a professional duty to ensure that the code is clear and follows PEP8 style guidelines with sufficient notes to allow future development and editing of the code. Similar to this, detailed documentation is also required outlining how to use the system and an explanation of how the system was designed. There is also a duty to ensure that all contributors are appropriately referenced along with expected professional expectations like completing a project in time.

##### Ethical:

When creating an extension to twitter (a character length restricted blogging application) it may seem like ethical obligations do not exist. However, all applications have ethical obligations to their customers (users), stakeholders and the wider community. In the case of this application, there is an ethical obligation that the content be moderated. Whether it be by automated or manual methods, there is an obligation that the content being posted not be illegal, dangerous or otherwise harmful in any way. Having clear guidelines that users have to adhere to can make this easier, especially if the guidelines are clear and specific to minimise the amount of offenders. Lastly, ensuring that all contributors are acting ethically and are not accessing private or sensitive data, implementing backdoors or other malicious code. Testing and constant reviews can mitigate against this, especially if the code can be open-source to allow the public to view for themselves the code.

##### Legal:

Legal obligations of a blogging application include adhering to the privacy act and as explained previously, the importance of adhering to privacy cannot be understated. The legal ramifications include massive fines that can reach up to $10 million dollars in Australia alone. In addition to this, the blogging application cannot be posting and displaying illegal content 

