# __cu_timetable_tools__

### The problem as I see it

I have a had a brief look at the timetable display for curtin in eStudent, it is super inconvenient to log in through oasis __AND THEN__ into eStudent __AND THEN__ go to My Classes __AND THEN__ select the appropriate dates to view what you __ACTUALLY__ have on at uni this week.

### The solution I would like

I would like to create a script that will pull all of the my class information from eStudent and then be able to set this up in google calendar as a seperate calendar (So that it can be turned on and off, otherwise it will make my calendar super cluttered)

## Things I have noticed / How it can be done

### Getting the timetable information from within eStudent

- I have noticed that if you expand the table above the graphical timetable you can have access to all of the information such as times, room numbers and whether or not that class is on ina given week. This should be relatively easy to extract (When I learn how to use beautiful soup or some other such package!)

- __cssTtableSspNavActvNm__
    - Appears to contain the label for the __type of class__, i.e. "Laboratory" , "Tutorial" etc.

- __cssTtableSspNavMasterSpkInfo3__
    - Appears to indicate the __name of the unit__, i.e. "Foundations of Digital Design"

- __cssTtableNavMainWhen__
    - Contains two sections underneath that describe the __when__
        - cssTtableNavMainLabel
            - Contains the label
            - This is in the form "Time: "
        - cssTtableNavMainContent
            - Contains the content
            - This is the time in the form "Tuesday 9:00 am-10:00 am"

- __cssTtableNavMainWhere__
    - Contains two sections underneath that describe the __where__
        - cssTtableNavMainLabel
            - Contains the label
            - This is in the form "Location: "
        - cssTtableNavMainContent
            - Contains the content
            - This is the time in the form "Bentley Campus 405 201"

### Logging into OASIS
![Alt text](/images/oasis_login.png?raw=true "Oasis Login")

Investigating the login fields
- Username:
![Alt text](/images/oasis_username.png?raw=true "Oasis Login")
name = "UserName"
value = ""
- Password:
![Alt text](/images/oasis_password.png?raw=true "Oasis Login")
name = "Password"
