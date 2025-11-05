#pragma once
void visitors_operations();
void visitors_operations(){
	printf("Launching visitor client program\n");
	printf("Welcome to Communication University of China\n");
	printf("Visitors can perform the following functions: 1. View campus forum (read-only) 2. Apply for account (only for freshmen and new staff)\n");
	int visitors_choice;
	scanf("%d", &visitors_choice);
	switch (visitors_choice) {
	case 1:
		display_forums();
		break;
	case 2:
		printf("Please enter relevant information for administrator review\n");
		printf("Please enter the student/employee ID from your admission/offer letter:");
		char newusername[10];
		scanf("%s", newusername);
		char newuser_password[10];
		printf("Please enter your real name:");
		scanf("%s", newuser_password);
		FILE* file;
		file = fopen("new_account_application.txt","a");
		fprintf(file, "%s %s\n", newusername, newuser_password);
		printf("Saved successfully. Please wait patiently for admin approval.\n");
		break;
	}


	printf("Please select the operation you want to perform:\n");
	
}
