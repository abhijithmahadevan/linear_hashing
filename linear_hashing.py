# Author        : Abhijith P Mahadevan 
# Entry Number   :(2021AIM1001 IIT Ropar)
# Code          : Linear Hashing Assignment

# Importing all the necessary libraries
import random
import string
import os

# Linear hashing parameters
NEXT_TO_SPLIT = 0
ROUND_NUMBER = 1
ROUND_LIMIT = 2**ROUND_NUMBER - 1
TOTAL_BUCKETS = ROUND_LIMIT
BUCKET_SIZE = 0

SMALL = 1

class record:
    transac_id : int
    transac_amount: int
    customer_name: str
    category : int

def generate_dataset():
    # This function is used to create dataset containg 60000 records in a .txt file
    data_set = open('data_set.txt','w+')
    for i in range(1,60001):
        transac_id = i
        transac_amount = random.randint(1,80000)
        customer_name = ''.join(random.choices(string.ascii_uppercase, k = 3))
        category = random.randint(0,1500)
        record = "%d %d %s %d\n" %(transac_id,transac_amount,customer_name,category)
        data_set.write(record)
    data_set.seek(0)
    data_set.close()
    print("Dataset created.")

def get_hash_address(key_value, power):
    # This function returns the hash address
    return (key_value % 2**power)

def insert_key(data):
    # This function is used to insert the records into the buckets
    key_value = data.transac_id
    bucket_number = get_hash_address(key_value, ROUND_NUMBER)
    if (bucket_number < NEXT_TO_SPLIT and ROUND_NUMBER > 1):
        bucket_number = get_hash_address(key_value, ROUND_NUMBER + 1)
        add_to_bucket(data, bucket_number)
    add_to_bucket(data,bucket_number)

def add_to_bucket(data,rehash = False):
    global ROUND_NUMBER
    global NEXT_TO_SPLIT
    global SMALL

    # Calculating the bucket address
    key_value = data.transac_id
    if (rehash == True):
        bucket_number = get_hash_address(key_value,ROUND_NUMBER+1)

    else:
        bucket_number = get_hash_address(key_value, ROUND_NUMBER)
        if (bucket_number < NEXT_TO_SPLIT):
            bucket_number = get_hash_address(key_value, ROUND_NUMBER + 1)
        if (SMALL == 1):
            print("\nRECORD %d INSERTED\n******************" %key_value)
    
    # Adding to bucket
    record_to_write = "%d %d %s %d\n" %(data.transac_id, data.transac_amount ,data.customer_name, data.category)
    bucket_name = "%s.txt" % bucket_number
    main_bucket_number = str(bucket_number)
    content_length = get_BUCKET_SIZE(bucket_name)
    if (content_length < BUCKET_SIZE):
        # No overflow. Write directly
        bucket = open(bucket_name,'a+')
        bucket.write(record_to_write)
        bucket.close()
    else:
        # Overflow has occured.
        # Find the overflow bucket to write to.
        i = 1
        while(content_length >= BUCKET_SIZE):
            bucket_name = main_bucket_number+"_OF"+str(i)+".txt"
            content_length = get_BUCKET_SIZE(bucket_name)
            i = i + 1
        # Writing to overflow bucket
        bucket = open(bucket_name,'a+')
        bucket.write(record_to_write)
        bucket.close()

        if(rehash == False):
            split()
            rehashing(NEXT_TO_SPLIT)
            NEXT_TO_SPLIT = NEXT_TO_SPLIT + 1
            if( NEXT_TO_SPLIT == 2**ROUND_NUMBER):
                NEXT_TO_SPLIT = 0
                ROUND_NUMBER = ROUND_NUMBER + 1
    if (rehash == False and SMALL == 1):
        visualization()
        print("\nNext to split : %d" %NEXT_TO_SPLIT, end = " ")
        print("Current round :%d" %ROUND_NUMBER)
            
def get_BUCKET_SIZE(bucket_name):
    # This function returns the number of records currently
    # present in the bucket
    bucket = open(bucket_name,'a+')
    bucket.seek(0,0)
    bucket_content = bucket.readlines()
    content_length = len(bucket_content)
    bucket.close()
    return content_length

def get_number_of_OFbuckets(main_bucket):
    # This function returns the number of overflow
    # buckets of a primary bucket
    i = 1
    count = 0
    while(True):
        path =str(main_bucket)+"_OF"+str(i)+".txt"
        if(os.path.isfile(path)):
            count = count + 1
            i = i + 1
        else:
            break
    return count

def rehashing(NEXT_TO_SPLIT):
    # Rehashing the content of split buckets
    global ROUND_NUMBER
    # Get number of overflow buckets of next_split
    count = get_number_of_OFbuckets(NEXT_TO_SPLIT)
    # Get contents of the main bucket
    temp_file = open(str(NEXT_TO_SPLIT)+".txt", 'r+') #Check access mode here
    hash_content = temp_file.readlines()
    temp_file.truncate(0)
    temp_file.close()

    # Get the contents of the all the overflow buckets
    for j in range(1,count+1):
        of_bucket_name = str(NEXT_TO_SPLIT)+"_OF"+str(j)+".txt"
        temp_file = open(of_bucket_name,'r') #Check access mode here
        hash_content.extend(temp_file.readlines())
        temp_file.close()
        os.remove(of_bucket_name) # delete the overflow bucket

    # Now we have all the contents of the overflow bucket and the main bucket in hash_content
    # Use add_to_bucket to add the elements back to the hash table
    for each_record in hash_content:
        data_fields = each_record.split(" ")
        record_to_pass = record()
        record_to_pass.transac_id = int(data_fields[0])
        record_to_pass.transac_amount = int(data_fields[1])
        record_to_pass.customer_name = str(data_fields[2])
        record_to_pass.category = int(data_fields[3])
        add_to_bucket(record_to_pass,rehash = True)
        

def split():
    # Adding new bucket
    global TOTAL_BUCKETS
    TOTAL_BUCKETS = TOTAL_BUCKETS + 1
    new_bucket_name = str(TOTAL_BUCKETS) + ".txt"
    new_bucket = open(new_bucket_name,'w+')
    new_bucket.close()

def search_for_key(key_to_search):
    # This function is used to search for a key
    # Get hash address of the key
    key_to_search = int(key_to_search)
    key_address = get_hash_address(key_to_search,ROUND_NUMBER)

    # Check if it is below or above the next pointer
    # If below the next pointer; Search in main bucket and the overflow buckets
    # If above the next pointer ; find address using round + 1 power 
    if (key_address < NEXT_TO_SPLIT):
        key_address = get_hash_address(key_to_search,ROUND_NUMBER + 1)
    count = get_number_of_OFbuckets(key_address)

    # Get contents of the main bucket
    temp_file = open(str(key_address)+".txt", 'r+') #Check access mode here
    hash_content = temp_file.readlines()
    temp_file.close()

    # Get the contents of the all the overflow buckets
    for j in range(1,count+1):
        of_bucket_name = str(key_address)+"_OF"+str(j)+".txt"
        temp_file = open(of_bucket_name,'r') #Check access mode here
        hash_content.extend(temp_file.readlines())
        temp_file.close()

    # Search for record begins here
    flag=0
    for each_line in hash_content: 
        if(each_line.split()[0] == str(key_to_search)):
            flag = 1
            print("The record is : ",end = " ")
            print(each_line,end = "")
            break
    if (flag == 1):
        print("RECORD FOUND AT %d" %key_address)
    else:
        print("Record not found.")

def visualization():
    global TOTAL_BUCKETS
    for bucket_no in range(0,TOTAL_BUCKETS + 1):
        # Get contents of the main bucket
        temp_file = open(str(bucket_no)+".txt", 'r+') #Check access mode here
        hash_content = temp_file.readlines()
        temp_file.close()
        print("\nBucket %s \n" %bucket_no, end ="")
        for line in hash_content:
            print(line,end="")
        
    # Get the contents of the all the overflow buckets
        count = get_number_of_OFbuckets(bucket_no)
        for j in range(1,count+1):
            of_bucket_name = str(bucket_no)+"_OF"+str(j)+".txt"
            print_name = str(bucket_no)+" Overflow "+str(j)
            temp_file = open(of_bucket_name,'r+') #Check access mode here
            hash_content=(temp_file.readlines())
            temp_file.close()
            print("\nBucket %s \n" %print_name, end = "")
            for line in hash_content:
                print(line,end="")


def insert_data(file_path):
    global SMALL
    # Read line from dataset and wrap it in th record
    with open(file_path) as file_data:
        for each_line in file_data:
            line_contents = each_line.split()
            data.transac_id = int(line_contents[0])
            data.transac_amount = int(line_contents[1])
            data.customer_name = str(line_contents[2])
            data.category = int(line_contents[3])
            add_to_bucket(data,rehash = False)

#Execution begins here
generate_dataset()
# Create a record template
data = record()

# Create two initial buckets
temp_file = open("0.txt", 'w+')
temp_file.close()
temp_file = open("1.txt", 'w+')
temp_file.close()

# Menu begins
print("Please remove all the file created in the previous insert before inserting a new dataset\n")
print("Linear Hashing")
while(True):
    print("\nSelect an option:")
    print("1. Insert dataset\n2. Search an element\n3. Print LH table\n4. Exit")
    print("\nEnter your option\t:",end =" ")
    option = input()
    if(option == '1'):
        # Insert the data set in to the hash file
        print("Type the file name\t:",end =" ")
        file_path = input()
        print("Enter the bucket size\t:",end =" ")
        BUCKET_SIZE =int(input())
        print("Print the status of the LH file after insert\n1. for Yes\n2. for No.")
        r = input()
        if (r == '1'):
            SMALL = 1
        elif(r == '2'):
            SMALL = 0
        insert_data(file_path)
        print("\nHASH TABLE CREATED SUCCESSFULLY")
    elif(option == '2'):
        # Search operation
        print("Enter the search key \t:",end =" ")
        key_to_search = input()
        search_for_key(key_to_search)
    elif(option == '3'):
        # Visualization operation
        visualization()
    elif(option == '4'):
        # Exit menu
        break
