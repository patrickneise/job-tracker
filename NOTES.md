Jobs
- Job can have one or more interviews (One-to-Many)
- Job can one or more notes
- Job can one or more contacts
- # TODO: cascade delete to interviews, contacts, notes

```
GET /jobs
GET /jobs/{job_id}
POST /jobs
PUT /jobs/{job_id}
DELETE /jobs/{job_id}
```

Interviews
- Interviews are specific to a Job
- Interviews can have one or more Notes
- Interviews can have one or more Contacts that may be shared with a Job
- # TODO: cascade deletes to contacts, notes
```
POST /jobs/{job_id}/interviews
GET /jobs/{job_id}/interviews
GET /jobs/{job_id}/interviews/{interview_id}
PUT /jobs/{job_id}/interviews/{interview_id}
DELETE /jobs/{job_id}/interviews/{interview_id}
```

# TODO: separate routes to 1) independently manage contacts and 2) CRUD individual contacts
Independent Contact Management
? Add boolean for company specific or global
- Create New Contact
- Update Contact
- Get Contact(s)
- Delete Contact
  - remove from Jobs and Interviews
  - remove Contact
  - # TODO: cascade delete to notes
Parent Contact Management
- Add contact to parent
  - Create new contact
  - Add to Parent
- Remove contact from parent
  - Remove from parent
  - Delete orphaned Contact (?? what if global, e.g. recruiter)
- Read parent contacts


Contacts
- Contacts are specific to a Job and/or an Interview
- Contacts can have one or more Notes

Notes
- Notes are exclusive to the parent entity


Contacts
- multiple jobs could share a contact (e.g. a recruiter)
- for a jobs contacts, one or more of them may be associated with an interview


adding contact to job:
- require job_id and contact data
- get or create contact
- add job_id, contact_id to JobContact joining table

adding contact to interview:
- require interview_id and contact data
- get or create contact
- add interview_id, contact_id to InterviewContact joining table


```json
{
  "company": "Netflix",
  "title": "CTO",
  "description": "CTO at Netflix",
  "posting": "https://www.netflix.com/jobs/1",
  "website": "https://www.netflix.com"
}
```

```json
{
  "company": "GitHub",
  "title": "VP of Eng",
  "description": "VP of Eng at GitHub",
  "posting": "https://www.github.com/jobs/1",
  "website": "https://www.github.com"
}
```

```json
{
  "name": "HR Rep",
  "email": "hr@netflix.com",
  "phone": "410-555-2683",
  "linkedin": "https://www.linkedin.com/in/hrrep"
}
```

```json
{
  "name": "Recruiter Smith",
  "email": "smith@recruiters.com",
  "phone": "410-555-8547",
  "linkedin": "https://www.linkedin.com/in/recruiter_smith"
}
```
