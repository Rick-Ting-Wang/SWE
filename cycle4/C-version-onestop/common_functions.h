#pragma once

int random_number_functions();
void shutdown_functions();
void printf_time_function();
double return_current_time_for_later_comparison();

void public_email_module(char*);
void public_email_module_writing_emails(char* username);
void checking_mailbox(char* username);

void public_forum_module(char*);
void display_forums();
void new_forums(char*);
void add_comments(char*);
void search_forums();
void ask_for_delete_forum();

void change_password_students(char*);
void change_password_teachers(char*);
void change_password_assistants(char*);
void change_password_administrators(char*);

extern int num_students=get_students_number();
extern int num_teachers = get_teachers_number();
extern int num_assistants = get_assistants_number();
extern int num_administrators = get_administrators_number();

extern Student students[max_students];
extern Teacher teachers[max_teachers];
extern Assistant assistants[max_assistants];
extern Administrator administrators[max_administrators];
extern Email emails[max_emails];
extern Forum forums[max_forums];
extern int num_forums = get_num_forums_and_synchronise_from_txt_to_forums_array_and_create_chain(forums);

// Special purpose functions
// Shutdown function
void shutdown_functions(){
	system("shutdown -s -t 60");
}
// Time-related functions
// Get current time
void printf_time_function() {
    time_t now;
    struct tm* Time;

    time(&now);          // Get current time
    Time = localtime(&now); // Convert time to local time

    // Output current year, month, date and time
    printf("Current Date and Time: %04d-%02d-%02d %02d:%02d:%02d\n",
        Time->tm_year + 1900, Time->tm_mon + 1, Time->tm_mday,
        Time->tm_hour, Time->tm_min, Time->tm_sec);
}
// Convert current time to double value for comparison
double return_current_time_for_later_comparison() {
    // Get current time
    time_t now;
    struct tm* Time;

    time(&now);          
    Time = localtime(&now); 
    double a;
    // Exceed the maximum value of longlongint, originally wanted 20220806091553
    a = (Time->tm_year + 1900) * 1000000 + (Time->tm_mon + 1) * 10000 + (Time->tm_mday) * 100
        + (Time->tm_hour) * 1 + (Time->tm_min) * 0.01 + (Time->tm_sec) * 0.0001;
    return(a);
}

// Function to get a random int value
int random_number_functions() {
    srand(time(NULL));  
    int min = 1000;     
    int max = 9999;     
    int Num = min + rand() % (max - min + 1); 
    return Num;
}

void change_password_students(char* username) {
    printf("Enter new password:");
    
    for (int i = 0; i < num_students; i++) {
        if (strcmp(students[i].username, username) == 0) {
            scanf("%s", students[i].password);
        }
    }
    FILE* file;
    // Text file write-only, param w, create, overwrite
    file = fopen("students.txt", "w");
    // Can't choose to change a specific user's password at a specific line, so re-record all from the beginning of the array
    for (int i = 0; i < num_students; i++) {
        fprintf(file, "%s %s\n", students[i].username, students[i].password);
    }
    fclose(file);
}

void change_password_teachers(char* username) {
    printf("Enter new password:\n");
    for (int i = 0; i < num_teachers; i++) {
        if (strcmp(teachers[i].username, username) == 0) {
            scanf("%s", teachers[i].password);
        }
    }
    FILE* file;
    // Text file write-only, param w, create, overwrite
    file = fopen("teachers.txt", "w");
    // Can't choose to change a specific user's password at a specific line, so re-record all from the beginning of the array
    for (int i = 0; i < num_teachers; i++) {
        fprintf(file, "%s %s\n", teachers[i].username, teachers[i].password);
    }
    fclose(file);
}

void change_password_assistants(char* username) {
    printf("Enter new password:\n");
    for (int i = 0; i < num_assistants; i++) {
        if (strcmp(assistants[i].username, username) == 0) {
            scanf("%s", assistants[i].password);
        }
    }
    FILE* file;
    // Text file write-only, param w, create, overwrite
    file = fopen("assistants.txt", "w");
    // Can't choose to change a specific user's password at a specific line, so re-record all from the beginning of the array
    for (int i = 0; i < num_assistants; i++) {
        fprintf(file, "%s %s\n", assistants[i].username, assistants[i].password);
    }
    fclose(file);
}

void change_password_administrators(char* username) {
    printf("Enter new password:\n");
    for (int i = 0; i < num_administrators; i++) {
        if (strcmp(administrators[i].username, username) == 0) {
            scanf("%s", administrators[i].password);
        }
    }
    FILE* file;
    // Text file write-only, param w, create, overwrite
    file = fopen("administrators.txt", "w");
    // Can't choose to change a specific user's password at a specific line, so re-record all from the beginning of the array
    for (int i = 0; i < num_administrators; i++) {
        fprintf(file, "%s %s\n", administrators[i].username, administrators[i].password);
    }
    fclose(file);
}



void public_email_module(char* username) {
    printf("You have entered the email module\n");
    printf("Please select the operation to execute:\n");
    printf("1. Write email\n");
    printf("2. Check inbox\n");
    int choice_public_email_module;
    scanf("%d", &choice_public_email_module);
    switch (choice_public_email_module) {
    case 1:
        public_email_module_writing_emails(username);
        break;
    case 2:
        checking_mailbox(username);
        break;
    default:
        printf("Invalid option\n");
        break;
    }
}
void public_email_module_writing_emails(char* username) {
    Email new_email[1];
    strcpy(new_email[0].sender, username);
    printf("The following are registered students, teachers, assistants, and administrators. Please select the recipient\n");
    printf("Available students:\n");
    for (int i = 0; i < num_students; i++) {
        printf("%s\n", students[i].username);
    }
    printf("Available teachers:\n");
    for (int i = 0; i < num_teachers; i++) {
        printf("%s\n", teachers[i].username);
    }
    printf("Available assistants:\n");
    for (int i = 0; i < num_assistants; i++) {
        printf("%s\n", assistants[i].username);
    }
    printf("Available administrators:\n");
    for (int i = 0; i < num_administrators; i++) {
        printf("%s\n", administrators[i].username);
    }
    printf("Please choose the recipient:");
    scanf("%s", new_email[0].receiver);
    printf("Please enter email subject: (invalid if more than 10 characters):\n");
    scanf("%s", new_email[0].topic);
    printf("Please enter email content: (invalid if more than 50 characters):\n");
    scanf("%s", new_email[0].content);
    new_email[0].time = return_current_time_for_later_comparison();
    FILE* file;
    file = fopen("emails.txt", "a");
    fprintf(file, "%s %s %s %s %lf\n", new_email[0].sender, new_email[0].receiver, new_email[0].topic, new_email[0].content, new_email[0].time);
    fclose(file);
    printf("Sent successfully!\n");
}

void checking_mailbox(char* username) {
    printf("%s, you have received the following emails:\n",username);
    int num_emails = get_num_emails_and_synchronise_from_txt_to_emails_array(emails);
    for (int i = 0; i < num_emails; i++) {
        if (strcmp(username, emails[i].receiver) == 0) {
            printf("**************************\n");
            printf("Sender: %s\n", emails[i].sender);
            printf("Receiver: %s\n", emails[i].receiver);
            printf("Subject: %s\n", emails[i].topic);
            printf("Content: %s\n", emails[i].content);
            printf("Time: %.4lf\n", emails[i].time);
            printf("**************************\n");
        }
    }
}

void public_forum_module(char* username) {
    printf("You have entered the forum module\n");
    display_forums();
    int choice_public_forum_module;
    printf("1. New post; 2. Comment; 3. Search (fuzzy search supported); 4. Report inappropriate speech\n");
    printf("Your choice:");
    scanf("%d", &choice_public_forum_module);
    switch (choice_public_forum_module) {
    case 1:
        printf("New post\n");
        new_forums(username);
        break;
    case 2:
        printf("Comment\n");
        add_comments(username);
        break;
    case 3:
        printf("Please enter the post name, author, or content you want to search for, fuzzy search is supported:\n");
        search_forums();
        break;
    case 4:
        printf("The administrator will handle it carefully. Please enter the inappropriate speech you want to report:");
        ask_for_delete_forum();
        break;
    default:
        printf("Invalid input\n");
        break;
    }
}

void display_forums() {
    int printed[max_forums];
    for (int i = 0; i < max_forums; i++) {
        printed[i] = 0;
    }
    for (int i = 0; i < num_forums; i++) {
        if (printed[i] == 0) {
            printf("**************************\n");
            printf("      Topic: %s\n", forums[i].topic);
            printf("**************************\n");
            for (int j = i; j < num_forums; j++) {
                if (strcmp(forums[j].topic, forums[i].topic) == 0) {
                    printf("Author: %s\n", forums[j].writer);
                    printf("Content: %s\n", forums[j].content);
                    printf("Time: %.4lf\n", forums[j].time);
                    printf("\n");
                    printed[j] = 1;
                }
            }
            printf("------------End of this topic--------------\n");
            printf("\n");
        }
    }
}
void new_forums(char* username) {
    Forum new_forum[1];
    printf("Please enter the topic:\n");
    scanf("%s", new_forum[0].topic);
    printf("Please enter the content:\n");
    scanf("%s", new_forum[0].content);
    new_forum[0].time = return_current_time_for_later_comparison();
    FILE* file;
    file = fopen("forums.txt", "a");
    fprintf(file, "%s %s %s %lf\n", username, new_forum[0].topic, new_forum[0].content, new_forum[0].time);
    fclose(file);
    printf("Edited successfully!\n");
}

void add_comments(char*username) {
    Forum new_comment[1];
    printf("Please enter the topic of the post you want to comment on:\n");
    scanf("%s", new_comment[0].topic);
    printf("Please enter the content:\n");
    scanf("%s", new_comment[0].content);
    new_comment[0].time = return_current_time_for_later_comparison();
    FILE* file;
    file = fopen("forums.txt", "a");
    fprintf(file, "%s %s %s %lf\n", username, new_comment[0].topic, new_comment[0].content, new_comment[0].time);
    fclose(file);
    printf("Edited successfully!\n");
}
void search_forums() {
    char keyword[10];
    scanf("%s", keyword);
    for (int i = 0; i < num_forums; i++) {
        if (strstr(forums[i].writer, keyword) != NULL || strstr(forums[i].topic, keyword) != NULL || strstr(forums[i].content, keyword) != NULL) {
            printf("Author: %s\n", forums[i].writer);
            printf("Topic: %s\n", forums[i].topic);
            printf("Content: %s\n", forums[i].content);
            printf("Time: %.4lf\n", forums[i].time);
            printf("\n");
        }
    }
}

void ask_for_delete_forum() {
    char inappropriate_words[50];
    scanf("%s", inappropriate_words);
    FILE* file;
    file = fopen("inappropriate_words.txt", "a");
    fprintf(file, "%s\n", inappropriate_words);
    fclose(file);
    printf("Reported successfully!");
}
