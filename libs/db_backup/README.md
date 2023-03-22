
### Automate MySQL backups

- This role is for managing automated backups from a database `host` machine to `gcp buckets.` It does this by deploying a backup script from the template directory to the db host.

#### Assumption
- Python3 installed
- Mysql server is running
- An instance of mysql database exists
  