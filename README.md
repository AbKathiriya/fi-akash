# fi-akash
Here I have added some random python scripts which I devloped in my free time. Most of them are for web scrapping.

### Instructions to run new_user.py script

1. Run this command to get help:

    `python new_user.py --help`
	
    >  usage: new_user.py [-h] {insert,delete} ...	
	
		Google apps Insert/Delete operation	
		positional arguments:
		
		{insert,delete}  Help for insert and delete user
		insert         Insert user help
		delete         Delete user help
	
2. Run this command to get help for inserting a new user

     `python new_user.py insert --help`

	>  usage: new_user.py insert [-h] fname lname email passw mobileno

		positional arguments:

		fname       Firstname of the user
		lname       Lastname of the user
		email       Primary email of the user
		passw       Password of the user
		mobileno    Mobile number of the user

2. Run this command to get help for deleting any user

    `python new_user.py insert --help`
	
    > usage: new_user.py delete [-h] email
	
		positional arguments:
		
		email       Primary email of the user

3. Sample commands to run this script
    *  `python new_user.py insert test_fname test_lname test-1@brainxs.me test@123`
    *  `python new_user.py delete test-1@brainxs.me`
