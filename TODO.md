* User bower for managing assets (foundation js should not be in js folder)
* Only use foundation components that are really needed
* Store results in database
* Add more tests for the API
* Handle when not all fields are present (eg description on retail jobs)


Before making public:
* Screen reader check
* Automated accessibility check
* HTML validator on all pages
* Check if location has latlng
* Check is location has postcode

Future:
* Get better at spotting full addresses (currently looking for full UK postcode)
* make python 3
* Add contract type check

Done:
* API
* Finish json-ld parser
* implement tests all for json-ld
* implement all tests for rdfa
* Add dev instructions to readme
* line width on results page
* Footer on large screens is a mess
* Make rdfa work
* Make json-ld work
* Include parsed data in results
* If not jobPosting, then cant check anything else (eg http://www.tesco-careers.com/JobDetails/134102.aspx)
* Write copy for salary results
* Write copy for location information results
* Write copy for employment type results
* Handle invalid URL
* Add feedback link to results page
* Check if salary contains numbers ('you could improve this advert by...')
* Add location check
* Readability score should use description only, not entire document
* Add a gender check
* Parse title and job description
* Check for open licence on jobs data
* Heroku
* Travis
* 404 page
* About page v1
* Add link to github
* CSS rules for non mobile browsers
* Add acknowledgements
* Link to opendiversity
* Link to diversity charter
* Create a package for genderdecoder
* Add salary check
* Write copy for jobposting results
* Write copy for licensing results
* Write copy for gender-coded langua
* merge data and reportge results
* Write copy for readability results
* API
* check why this has a low reading score! http://www.w4mpjobs.org/JobDetails.aspx?jobid=56341