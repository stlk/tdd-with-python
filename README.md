
Running the Django dev server
---
python3 manage.py runserver

Running the functional tests
---
python3 functional_tests.py

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



ssh -i aws-linux.pem ubuntu@ec2-54-194-221-30.eu-west-1.compute.amazonaws.com


fab deploy:host=ubuntu@lists-staging.rousek.name -i /home/josef/Documents/aws-linux.pem