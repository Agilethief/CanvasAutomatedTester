# Goals:

A tool that can be ran daily.
Will cycle through different canvas courses based on their index

It will need to be able to run headless and safely handle issues.

It will need to output a report, excel preferable that anyone can view.

## Bonus

It will post the findings in a MS Teams message with a link to the file on SharePoint

---

## Tests

### Link checking

It will check all links on every page, including assessment pages and confirm if they work.
There will be a black list for links that will be skipped. This is to handle Govt. department internal links that will work for participants but not us.

### Word checking

There will be a list of bad words that must not be found and if found, must be reported.

### Image checking

Images must be checked to confirm they can load in as a participant.
This will require testing each page as a participant to ensure they load correctly.

### Configuration checking

- All assignments must be set to build on last attempt
- Marking must be set to manually posted.
- more?
