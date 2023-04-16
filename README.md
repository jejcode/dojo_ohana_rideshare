# Dojo Ohana (Belt Review)

Notes for edits:
- update redirects that redirect to /wall
- don't forget to link all controllers to the server.py
- edit the DB in user.py

Order of programming:
- / registration and login - DONe
- /rides/dashboard (route in rides) -DONE
- dashboard.html - DONE
    - functioning header ( + and logout) -DONE
    - two columns (requestd & booked, empty for now) -DONE
- /rides/new (route in rides) -DONE
- new.html
    - working header - DONE
    - form validation -DONE
- /rides/request (HIDDEN) -DONE
    - POST -DONE 
    - logged in access only -DONE
    - form validation -DONE
    - redirect to dashboard -DONE
- dashboard.html
    - create html cards for each request -DONE
    -working routes for delete and claim
- /rides/delete/ride_id (hidden)
- /rides/request/claim (hidden)
- /rides/ride_id (route to details page)
- details.html
    - simple one row database query
    - edit links
    - delete link (/rides/delete/ride_id)
- /edit/ride_id
- edit.html
    - simplfied form
    - validate form
- SENSEI BONUS: MESSAGING
    - update details.html
    - /message/send (hidden)
    - redirect to same page
