Linear hashing Assignment CS509 PG Software lab
Author		: Abhijith P Mahadevan
Entry Number	: 2021AIM1001
Language	: Python

General instructions

0. A dataset of the 60000 records will be created as data_set.txt when the code
   is run and will present in the directory. The data set will contain records
   and the fields are seperated by single space. only one record will be present
   in a line.
   
1. Run the python script in the terminal as python3 <filename>.py

2. Important : Please do remove all the files created in previous insert if any
   before inserting a new data set
   
3. Select option 1 to insert new datset.
   Enter the filename as <filename>.txt.
   The dataset should be single space seperated fields
   with one record per line
   
   An option will be provided for printing out the status of the LH file
   after every insert of a record in the dataset. 
   The next to split and the round number will be printed along with the
   contents of  the primary as well as the overflow buckets.
   
4. Select option 2 to search for a record.
   The entire record along with the location will be printed if present
   A "RECORD NOT FOUND" message will be printed if not present
   
5. Select option 3 for printing out the entire hash table

6. Exit option
   
