# Bed Management System
As the management system is not a system for external users but an internal system for back-office administration for doctors and administrators. 

Users do not need to register but only need to add user accounts and passwords directly to the database in the back-office and use them.

## Requirement/How to use

1. Install Python3.7

2. Install MySQL5.7/8.0

3. Install environment: `pip install -r requirements.txt`

4. Create database: 

   * MySQL5.7:

     ```
     create database hospital_bed;
     grant all on *.* to 'hospital_bed'@'%' identified by '123456';
     use hospital_bed
     source hospital_bed.sql
     ```

   * MySQL8.0:

     ```
     create database hospital_bed;
     create user 'hospital_bed'@'%' identified by '123456';
     grant all on *.* to 'hospital_bed'@'%';
     use hospital_bed
     source hospital_bed.sql
     ```

   If something is wrong in import data, please try to import data manually by database management software like Navicat and MySQLWorkbench.

5. Run server: `python manage.py runserver 0.0.0.0:8000`

   If there is an error called: *'str' object has no attribute 'decode'* , please edit `..\Python37\Lib\site-packages\django\db\backends\mysql\operations.py` line 146: `query = query.encode().decode(errors='replace')`

6. Access with a browser to `http://127.0.0.1:8000`

7. Initial username/password: 

   * Admin: Peter/123456

   * Doctor: Chen/123456
   * Nurse: Lily/123456

## Unit test

After installing environment and database, use `python manage.py test unit_tests` to run and test whether system works well.