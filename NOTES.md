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
