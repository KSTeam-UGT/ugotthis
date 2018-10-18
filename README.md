# U Got This
Group Project/Presentation

## OVERVIEW
We believe in believing in ourselves. And we believe in you! Sometimes all we need is a little push in the right direction to quantum leap into the next level of our lives. We can do this by filling our spaces with positivity, motivation and resources to help us get there. What better place to start than with our site, yougotthis.com. Start by completing your personal profile and we’ll provide resources that can help you achieve your goal whether it’s to beat procrastination, stay focused and more. We believe you got this!

## GOALS
1. Collaborate successfully on our project by using the tools we have available to us through the course and the skills we’ve learned in the past few weeks.
2. Launch a minimum viable product that provides ease of use and a pleasant UI for an optimal end user experience.

## MILESTONES

### Team Members and Roles:
Handling the fun task of beautifying our product by ensuring the UI is easy on the eyes we have Maria and Kasheena as our Front End/Design Team. Keeping everything pieced together on the back end is Steve, our Back End Engineer with support from Ginger. Lastly, Product Managing and API/Data Engineering is Ginger with support from Steve.

### Software Concept And Goal:
Our site, yougotthis.com, will leverage the following APIs:
Universal Inspirational Quotes API
Site can send a daily inspirational quote directly to your inbox using…
Mailgun
Used for purposes of mailing resources
YouTube
To send a motivational video
Open Library
Find the right book on personal improvement
For programming we’ll use HTML and CSS, Django and Python.

### Potential Challenges:
While the APIs are available, we would need to make sure we can map to the profile created by the end user and not just provide results at random.

### User Stories:
1. As a person interested in self improvement, I can create a profile and have self improvement resources sent directly to me or kept on my user profile.
2. As an end user of the site, I am able to log in and see my profile, make changes to my profile and save these changes.
3. As an end user of the site, I can specify what type of resources are sent to me.
4. As a recipient of self help resources, I can mark a self help tool as a favorite in my profile to access later

For workflow please refer to the shared doc sent in the HW channel.

## October 17 Milestone 2

### Proof Of Concept

1. What need are we fulfilling? Why would people get out of using our site? According a Forbes article titled "Motivation Matters", 40% of high school students are chronically disengaged from school. An article by medium.com called "8 Reasons You Lack Motivation" says "Motivation is like a campfire. You need 3 components to reap its full rewards: the matches that get the fire started, the wood that keeps the fire going and the heat to roast your marshmallows." ugotthis.com is the spark that lights those matches by matching our users with personalized motivational materials
2. What are these users looking for? How do we deliver the final product? We don't want to overcomplicate the process. Keep the signup process simple and  straight to the point. Make the UI easy to navigate. Make sure the content they subscribe for matches their needs. We anticipate an official launch our MVP by October 27th. The product will be  structured using HTML and CSS on the front end, Python and Django on the back end along with APIs to pull the materials needed.
3. Are we prepared to handle any challenges that come with launching a product like this? Yes! Our team has huddled together a few times to go over testing of the APIs, assigning roles to best deliver this product and our success measurements criteria has been defined and agreed upon. We're quick to huddle back together any time we come across an issue and work through it to solution.

#### An example:

```python
# The Open Library API lets us pull book recommendations under the Self Help subject:
import requests
import pprint

ppjson = pprint.PrettyPrinter(indent=2)

response_subject = requests.get(
    'https://openlibrary.org/subjects/self-help.json'
)
data_subject = response_subject.json()

search_string = 'music'
works_by_subject = data_subject['works']
works_by_subject_results = []
for work in works_by_subject:
    for item in work['subject']:
        if search_string in item:
            works_by_subject_results.append(work['key'])
            print('https://openlibrary.org' + work['key'])

open('works_by_subject_results.txt', 'w+').write(str(works_by_subject_results))


# The YouTube API lets us link to motivational videos:
video_search_string = 'something'
response_video = requests.get(
    'https://www.googleapis.com/youtube/v3/search?'
    'part=snippet&maxResults=50&q=' + video_search_string +
    '&key={API_KEY}'
)
data_video = response_video.json()
videos_by_search_string = data_video['items']
videos_results = []
for video in videos_by_search_string:
    videos_results.append(video['id']['videoId'])
    print('https://www.youtube.com/watch?v=' + video['id']['videoId'])
```


### Acceptance Criteria
As a person interested in self improvement, I can use ugotthis.com to
create a profile and have self improvement resources sent directly to me or kept on my
user profile:

* User navigates to ugotthis.com
* User sees ugotthis.com landing page
* User can login if they already a member, sign up for U Got This by clicking a link or let us know they forgot their username and password
* User clicks sign up for U Got This
* User is brought to ugotthis.com/signup_page
* User sees fields to enter in a username, email and password
* User answers their profile creation questions:
  * Choose from the following categories you want to appear in your feed
    * focus/modivation/goal orientation
    * uplifting, inspirational, happiness
    * body positivity, health, strength
    * peace, calm, meditation, grattitude, zen
* User can select the frequency of their motivational notifications:
  * Daily
  * Weekly
  * Bi-Weekly
* User clicks the Submit button at the bottom to complete the registration process
* User sees a confirmation page thanking them for signing up
* User receives confirmation email
