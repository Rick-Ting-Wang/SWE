#pragma once
void administrators_operations();
char* administrators_login();
extern Administrator administrators[];


void administrators_operations() {
    printf("Launching administrator-side program\n");
    char* username = NULL;
    username = administrators_login();
    printf("Welcome to the CUC One-Stop Service Platform\n");
    printf("You have logged in as %s\n", username);
    int choice;
    {
        do {
            printf("Please select a module:\n");
            printf("1. Change password\n");
            printf("2. Campus email\n");
            printf("3. CUC Walnut Forest Forum\n");
            printf("4. Handle inappropriate forum speech\n");
            printf("5. Exit\n");
            printf("6. View new account applications\n");
            printf("7. Add new student account\n");
            printf("8. Add new teacher account\n");
            printf("9. Add new teaching assistant account\n");
            printf("10. Add new administrator account\n");

            scanf("%d", &choice);

            switch (choice) {
            case 1:
                printf("%s, you are about to change your password\n", username);
                printf("After changing, please restart the computer for it to take effect\n");
                change_password_administrators(username);
                break;
            case 2:
                printf("%s, you have entered the email module\n", username);
                public_email_module(username);
                break;
            case 3:
                printf("%s, you have entered the forum module\n", username);
                public_forum_module(username);
                break;
            case 4:
                printf("%s, you will handle inappropriate speech\n", username);
                FILE* file;
                file = fopen("inappropriate_words.txt", "r");
                char inappropriate_words[100][100];
                for (int i = 0; i < 1000; i++) {
                    
                    while (fscanf(file, "%s", inappropriate_words[i]) == 1) {                        
                        int inappropriate_words_existed = 0;
                        for (int j = 0; j < num_forums; j++) {                            
                            if (strcmp(forums[j].content, inappropriate_words[i]) == 0) {
                                inappropriate_words_existed = 1;
                                break;
                            }
                        }                       
                        if (inappropriate_words_existed) {
                            printf("%s\n",inappropriate_words[i]);
                        }
                     
                    }
                }
                printf("How many of the above remarks do you think are against the CUC spirit?\n");
                int inappropriate_words_that_defies_CUC_spirit;
                scanf("%d", &inappropriate_words_that_defies_CUC_spirit);

                for (int i = 1; i <= inappropriate_words_that_defies_CUC_spirit; i++) {
                    printf("Please input the No.%d inappropriate remark violating CUC spirit\n",i);
                    char words[100];
                    scanf("%s", words);
                    int forums_to_delete = -1;
                    for (int j = 0; j < num_forums; j++) {
                        
                        if (strcmp(forums[j].content, words) == 0) {
                            forums_to_delete = j;
                            break;
                        }
                    }
                        if (forums_to_delete != -1) {
                            for (int i = forums_to_delete; i < num_forums - 1; i++) {
                                forums[i] = forums[i + 1];
                            }
                            num_forums--;
                          
                           

                            FILE* file = fopen("forums.txt", "w");


                            for (int i = 0; i < num_forums; i++) {
                                fprintf(file, "%s %s %s %lf\n", forums[i].writer,
                                    forums[i].topic,
                                    forums[i].content,
                                    forums[i].time);
                                
                            }
                            fclose(file);

                            printf("The inappropriate remark \"%s\" and its author/time/topic have been deleted\n",words);
                        }
                        else {
                            printf("The inappropriate remark \"%s\" was not found\n", words);
                        }
                    }
                FILE* file_words;
                file_words = fopen("inappropriate_words.txt", "w");
                fclose(file_words);
            break;

            case 5:
                printf("Thank you for using! Goodbye.\n");
                break;
            case 6:
                FILE * applicationfile;
                applicationfile = fopen("new_account_application.txt", "r");
                char line[100];
                // Actually, the four types of account structures are the same
                Student new_account[1000];
                for (int i = 0; i < 1000; i++) {
                    while (fscanf(applicationfile, "%s %s", new_account[i].username, new_account[i].password)==2) {
                        int username_existed = 0;
                        for (int j = 0; j < num_students; j++) {
                            if (strcmp(new_account[i].username, students[j].username) == 0) {
                                username_existed = 1;
                                break;
                            }
                        }
                        for (int j = 0; j < num_students; j++) {
                            if (strcmp(new_account[i].username, students[j].username) == 0) {
                                username_existed = 1;
                                break;
                            }
                        }
                        for (int j = 0; j < num_students; j++) {
                            if (strcmp(new_account[i].username, students[j].username) == 0) {
                                username_existed = 1;
                                break;
                            }
                        }
                        for (int j = 0; j < num_students; j++) {
                            if (strcmp(new_account[i].username, students[j].username) == 0) {
                                username_existed = 1;
                                break;
                            }
                        }
                        if (!username_existed) {
                            printf("%s %s\n", new_account[i].username, new_account[i].password);
                        }
                    }
                }
                printf("Are there any account applications to approve? If yes, please enter 7-10, representing adding new student, teacher, assistant, or administrator accounts respectively.\n");
                FILE* file_accounts;
                file_accounts = fopen("new_account_application.txt", "w");
                fclose(file_accounts);

                break;
            case 7:
                add_new_student();
                break;
            case 8:
                add_new_teacher();
                break;
            case 9:
                add_new_assistant();
                break;
            case 10:
                add_new_administrator();
                break;

            default:
                printf("Invalid selection, please enter again.\n");
            }
        } while (choice != 5);
    }
}


// Login function
char* administrators_login() {
    printf("Please log in, the computer will shut down after three failed attempts:\n");
    int attempts = 0;
    int correct = 0;
    int num_administrators = get_administrators_number();

    while (attempts < 3) {
        char input_username[50];
        char input_password[50];
        int input_verify_code;

        int verify_code = random_number_functions();
        printf("Verification code: %d\n", verify_code);

        printf("Please enter your username: ");
        scanf("%s", input_username);
        printf("Please enter your password: ");
        scanf("%s", input_password);
        printf("Please enter the verification code: ");
        scanf("%d", &input_verify_code);

        for (int i = 0; i < num_administrators; i++) {
            if (strcmp(input_username, administrators[i].username) == 0 &&
                strcmp(input_password, administrators[i].password) == 0 &&
                input_verify_code == verify_code) {
                correct = 1;
                break;
            }
        }

        if (correct) {
            printf("Login successful!\n");
            return(input_username);

        }
        else {
            attempts++;
            printf("Login failed, remaining attempts: %d. Reminder: if attempts are used up, the computer will shut down.\n", 3 - attempts);
        }
    }

    printf("Don't try to brute force the password. With the verification code and three chances, it's hard for you to guess. Shutting down now, bye.\n");
    shutdown_functions();
}
