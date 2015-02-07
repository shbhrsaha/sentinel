
sentinel
===
Automatically enrolls Princeton students into courses when space opens up on the registrar's enrollment listings.

[![Video Demo](https://raw.githubusercontent.com/shbhrsaha/sentinel/master/video_preview.png)](https://www.youtube.com/watch?v=upAtFzAW_8c)

Usage
---
Princeton University NetID and password are required to use Sentinel. Python dependencies are Splinter for stateful web browsing and BeautifulSoup for webpage parsing. By default, Splinter instantiates an instance of Firefox web browser.

1) Add the courses you'd like to enroll in to the "Course Queue" in SCORE
2) Fill in the "User Input" section of the script with your security details and the courses you want to enroll in
3) Run: python sentinel.py 
4) Leave your computer running and Sentinel will email you when you're enrolled!

Course Signup
---
Like most universities, Princeton has a rather competitive system for signing up for courses. At the end of each semester, there is a week when students log on to an online system in order of descending seniority with the hopes that the courses they want to take haven't yet reached maximum capacity. The online course registration system is called SCORE and is similar to systems at other colleges.

In the event that a course fills up, most students then log on to [Princeton Pounce](http://pounce.tigerapps.org/), a service that sends a text/email notification when space opens up in a course. The shortcoming with Princeton Pounce is that after receiving a notification, students rush to again log on to SCORE and officially enroll in the course.

For the Fall 2013 semester, I was disappointed to get into just two of the five courses I wanted. I turned to Python for a solution.

Sentinel is a Python script that, like Princeton Pounce, watches for opportunities in course enrollment, but then also automatically enrolls you in the course by logging onto SCORE faster than other students can by themselves. This script is super-useful to keep running on your computer during the course enrollment period and the first week of the semester, when many students drop courses. With some modification, Sentinel can enroll you in all your courses at the beginning of the course enrollment period as well.
