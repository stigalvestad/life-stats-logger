# life-stats-logger
Track different kinds of events, let user log it when it occur, then display them in order to give insight to how often they occur.

## Dev environment
Virtualenv for python has been setup in:

    /home/stig/code/python-virtualenv/lifestatslogger

This was used to create the environment (one time):

    virtualenv --python $(which python3.6) /home/stig/code/python-virtualenv/lifestatslogger
    
To activate environment:

    source /home/stig/code/python-virtualenv/lifestatslogger/bin/activate
    
    
### Managing dependencies
If a new import is required:

- add the import
- install it with pip inside the virtual environment
- finally add it to the requirements file with command below


    pip freeze > requirements.txt

The requirements-file will be used by chalice to include the required files when 
uploading the deployment package to AWS.    
    

# Design plan
Implement API in python, using chalice. Thus we use AWS lambda functions for API. 
Data is stored in a time-series oriented store, for example AWS Timestream (currently only preview)
Or we can try with AWS DynamoDB

Suggested schema (sql-inspired)
* user: id, name, isDeleted, createdAt, createdBy
* usergroup: id, name, isDeleted, createdAt, createdBy
* usergroupmember: userId, usergroupId, isDeleted, createdAt, createdBy
* metric: id, name, usergroupId, type, isDeleted, createdAt, createdBy
* event: id, metricId, userId, time, duration, 

Maybe need to rethink, in order to use DynamoDB, to ensure it can be queried ok.

# API 
## user
POST /user {id, name} creates a user

## usergroup
POST /usergroup {id, name} creates a user group
POST /usergroup/{usergroup-id}/user/{user-id} adds a user to a usergroup

## metric
metric: something we want to keep an eye on,
POST /metric: {id, name, usergroup, type: period | occurrence} creates a metric

## event
POST /event: {metric, user, time, [duration]} create an instance of a metric. duration is required if metric is type=period

GET /event?start=x&stop=y: gets events between start and stop, start inclusive, end exclusive
GET /event/{metric} get events for that specific metric within start and stop, 

# Client App


Simple web page which lets user add events. 
