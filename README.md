# awe-blog
A simple blog application with user accounts, login/logout, blog post management, comments and likes.
Built using Google App Engine utilizing python and jinja2

## Working and Output
This app creates a blog framework with following functionalities
- User Registration
- User Login
- Create/edit/delete new blogs
- Like/Unlike posts
- Create/edit/delete comments
- Cookie usage to identify user authentication
- Hashed Password storage

## Requirements
- Python 2.7 Environment
- Google Cloud Platform account(for cloud deployment)
- gcloud SDK(Google App Engine)
- Jinja2
- Bootstrap

## Files & folders
- blog.py : This is the python file that runs the app
- index.yaml : Contains the index created for datastore(these are automatically created)
- app.yaml : App configuration (eg: Specifies folders for templates and use of jinja2 framework)
- static folder : This and its subfolders contains all static files used in project(css,js etc)
- templates folder : Contains all the templates that are used for this project(used through jinja2)

## Usage
- Clone/download the repo to your local machine
- For running on local machine, cd in to the repo folder and run
``` dev_appserver.py . ```
- For deploying in to google cloud platform use following command
``` gcloud app deploy ```
	- Usually index.yaml files are skipped on using above command. In case you are
	  getting error based on index in cloud platform use following command
	  ``` gcloud app deploy --project your-project-name index.yaml ```
  - This is because some indexes are required by gcloud to perform certain datastore
    operations. In your local machine, these indexes are automatically created and can be found at
    index.yaml .You can deploy this file along with app so that the index will be built in the cloud
