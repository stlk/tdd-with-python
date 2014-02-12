
Running the Django dev server
---
python3 manage.py runserver

Running the unit tests
---
python3 manage.py test

DB migration
---
python3 manage.py syncdb

To run the functional tests
---
python3 manage.py test functional_tests

To run the unit tests
---
python3 manage.py test lists

SSH
---
ssh -i aws-linux.pem ubuntu@ec2-54-194-221-30.eu-west-1.compute.amazonaws.com

Deploy
---
fab deploy:host=ubuntu@lists-staging.rousek.name -i /home/stlk/.ssh/aws-linux.pem