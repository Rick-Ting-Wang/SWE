
#pragma once
void teachers_operations();
char* teachers_login();
extern Teacher teachers[];
extern Course courses[];
extern int num_courses;
extern int** students_course_score;


void teachers_operations() {
    printf("Starting the teacher terminal program\n");
    num_courses = get_num_courses_and_synchronise_from_txt_to_courses_array_and_create_chain(courses);
    num_students = get_students_number();
    char* username = NULL;
    username = teachers_login();
    printf("Welcome to the Communication University of China One-stop Service Platform\n");
    printf("You are logged in as %s\n", username);
    int choice;
    {
        printf("Please select a module:\n");
        printf("1. Change password\n");
        printf("2. Campus email\n");
        printf("3. CUC Walnut Forest Forum\n");
        printf("4. Grade students\n");
        printf("5. Exit\n");
        printf("6. View teaching courses\n");
        
        do {
            scanf("%d", &choice);
            switch (choice) {
            case 1:
                printf("%s, you are about to change your password\n", username);
                printf("The change will take effect after restarting the computer\n");
                change_password_teachers(username);
                break;
            case 2:
                printf("%s, you have entered the email module\n", username);
                public_email_module(username);
                break;
            case 3:
                printf("%s, you have entered the forum module\n", username);
                public_forum_module(username);
                break;

            case 5:

                printf("Thank you for using! Goodbye.\n");
                break;
            default:
                printf("Invalid selection, please try again.\n");
            case 4:
                printf("Executing grading operation:\n");
                int teacher_courses;
                teacher_courses = 0;
                
                for (int i = 0; i < num_courses; i++) {
                    
                    if (strcmp(username, courses[i].teacher) == 0) {
                        teacher_courses++;
                        printf("%d %s %s %s %d\n", i, courses[i].course_code, courses[i].course_name, courses[i].teacher, courses[i].course_credit);

                    }
                }
                printf("The system detected that you are teaching %d courses\n", teacher_courses);
                printf("Please select the index number of the course you want to grade:\n");
                int course_teacher_choose;
                scanf("%d", &course_teacher_choose);
                
                for (int i = 0; i < num_students; i++) {
                    if (students_course_score[i][course_teacher_choose] == -1) {
                        printf("%s's score in course %s is", students[i].username, courses[course_teacher_choose].course_name);
                        scanf("%d", &students_course_score[i][course_teacher_choose]);
                    }
                   
                }
                FILE* file;
                file = fopen("students_course_score.txt", "w");


                for (int i = 0; i < num_students; i++) {
                    for (int j = 0; j < num_courses; j++) {
                        fprintf(file, "%d ", students_course_score[i][j]);
                    }
                    fprintf(file, "\n");
                }

                fclose(file);


                break;



            case 6:
            {
                int teacher_courses;
                teacher_courses = 0;

                for (int i = 0; i < num_courses; i++) {

                    if (strcmp(username, courses[i].teacher) == 0) {
                        teacher_courses++;
                        printf("%d %s %s %s %d\n", i, courses[i].course_code, courses[i].course_name, courses[i].teacher, courses[i].course_credit);

                    }
                }
                printf("The system detected that you are teaching %d courses\n", teacher_courses);


                break;
            }
            }
        } while (choice != 5);
    }
}
// Login function
char* teachers_login() {
    printf("Please log in. If you enter incorrectly three times, the system will shut down:\n");
    int attempts = 0;
    int correct = 0;
    int num_teachers = get_teachers_number();

    while (attempts < 3) {
        char input_username[50];
        char input_password[50];
        int input_verify_code;

        int verify_code = random_number_functions();
        printf("Verification code: %d\n", verify_code);

        printf("Please enter your username:");
        scanf("%s", input_username);
        printf("Please enter your password:");
        scanf("%s", input_password);
        printf("Please enter the verification code:");
        scanf("%d", &input_verify_code);

        for (int i = 0; i < num_teachers; i++) {
            if (strcmp(input_username, teachers[i].username) == 0 &&
                strcmp(input_password, teachers[i].password) == 0 &&
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
            printf("Login failed, remaining attempts: %d. Reminder: the system will shut down if you fail three times.\n", 3 - attempts);
        }
    }

    printf("Don't even think about brute-forcing the password. I gave you three tries with a long verification code. Shutting down now, bye.\n");
    shutdown_functions();
}
