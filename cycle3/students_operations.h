#pragma once
void students_operations();
char* students_login();
extern Student students[];
extern Course courses[max_courses];

extern int num_courses;
extern int num_students;
extern int** students_course_score;


void students_operations() {
    num_courses = get_num_courses_and_synchronise_from_txt_to_courses_array_and_create_chain(courses);
    num_students = get_students_number();

    printf("Launching student-side program\n");
    char* username = NULL;
    username = students_login();
    printf("Welcome to CUC One-Stop Service Platform\n");
    printf("You are logged in as %s\n", username);
    int choice;

    printf("Please select a module:\n");
    printf("1. Change password\n");
    printf("2. Campus email\n");
    printf("3. CUC Walnut Forest Forum\n");
    printf("4. Course selection\n");
    printf("5. Exit\n");
    printf("6. View selected credits and transcript\n");
    printf("7. Drop course\n");
    
    do {
        scanf("%d", &choice);
        switch (choice) {
        case 1:
            printf("%s, you are about to change your password\n", username);
            printf("After changing, please restart the computer for it to take effect\n");
            change_password_students(username);
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
            printf("%s, you have entered the course selection module\n", username);
            int student_order;
            student_order = -1;
            for (int i = 0; i < num_students; i++) {
                if (strcmp(students[i].username, username) == 0) {
                    student_order = i;
                }
            }


            printf("You have not selected the following courses:\n");




            for (int i = 0; i < num_courses; i++) {
                if (*(*(students_course_score + student_order) + i) == -2) {

                    printf("%d %s %s %s %d\n", i, courses[i].course_code, courses[i].teacher, courses[i].course_name, courses[i].course_credit);

                }
            }
            printf("Unselected subjects:\n");
            for (int i = 0; i < num_courses; i++) {
                if (students_course_score[student_order][i] == -2) {
                    printf("Index: %d, Subject: %s Name: %s Credits: %d\n", i, courses[i].course_code, courses[i].course_name, courses[i].course_credit);
                }
            }



            printf("How many subjects do you want to choose?\n");
            int subjects;
            scanf("%d", &subjects);
            for (int i = 1; i <= subjects; i++) {
                printf("Enter the index of the subject you want to select:\n");
                int courses_order;
                scanf("%d", &courses_order);

                if (students_course_score[student_order][courses_order] == -2) {
                    students_course_score[student_order][courses_order] = -1;
                    printf("Course selection successful\n");
                }
                else { printf("You can't change your grade like this\n"); }


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
        case 5:
            printf("Thank you for using! Goodbye.\n");
            break;

        case 6:
            printf("View selected courses, transcript, and GPA\n");
            printf("Graduation credit requirement: 30 credits\n");
            int student_orderr;
            student_orderr = -1;
            for (int i = 0; i < num_students; i++) {
                if (strcmp(students[i].username, username) == 0) {
                    student_orderr = i;
                }
            }
            printf("Subjects with grades obtained:\n");
            for (int i = 0; i < num_courses; i++) {
                if (students_course_score[student_orderr][i] >= 0) {
                    printf("Subject: %s Name: %s Credits: %d Grade: %d\n", courses[i].course_code, courses[i].course_name, courses[i].course_credit, students_course_score[student_orderr][i]);
                }
            }



            printf("Subjects selected but not yet graded:\n");
            for (int i = 0; i < num_courses; i++) {
                if (students_course_score[student_orderr][i] == -1) {
                    printf("Subject: %s Name: %s Credits: %d Grade: Not yet graded\n", courses[i].course_code, courses[i].course_name, courses[i].course_credit);
                }
            }

            printf("Unselected subjects:\n");
            for (int i = 0; i < num_courses; i++) {
                if (students_course_score[student_orderr][i] == -2) {
                    printf("Index: %d, Subject: %s Name: %s Credits: %d\n", i, courses[i].course_code, courses[i].course_name, courses[i].course_credit);
                }
            }

            break;
        case 7:

        {

            printf("You have chosen to drop a course:\n");
            int student_orderrr;
            student_orderrr = -1;
            for (int i = 0; i < num_students; i++) {
                if (strcmp(students[i].username, username) == 0) {
                    student_orderrr = i;
                    break;
                }
            }
            
            printf("Only courses not yet graded can be dropped!\n");
            printf("Subjects selected but not yet graded:\n");
            for (int i = 0; i < num_courses; i++) {
                if (students_course_score[student_orderrr][i] == -1) {
                    printf("Index: %d Subject: %s Name: %s Credits: %d Grade: Not yet graded\n", i, courses[i].course_code, courses[i].course_name, courses[i].course_credit);

                }
            }
                int students_course_will_delete;
                students_course_will_delete = -1;
                printf("Enter the index of the course you want to drop:\n");
                scanf("%d", &students_course_will_delete);
                if (students_course_score[student_orderrr][students_course_will_delete] == -1) {
                    students_course_score[student_orderrr][students_course_will_delete] = -2;
                    

                    FILE* file;
                    file = fopen("students_course_score.txt", "w");


                    for (int i = 0; i < num_students; i++) {
                        for (int j = 0; j < num_courses; j++) {
                            fprintf(file, "%d ", students_course_score[i][j]);
                        }
                        fprintf(file, "\n");
                    }

                    fclose(file);
                    printf("Course dropped successfully!\n");

                    break;

                }
                else {
                    printf("Invalid index!\n");
                    break;
                }
            
        

        
        default:
            printf("Invalid choice, please re-enter.\n");


            }

        }
    } while (choice != 5);

}
    


// Login function
char* students_login() {
    printf("Please login. The computer will shut down after three incorrect attempts:\n");
    int attempts = 0;
    int correct = 0;
    int num_students = get_students_number();

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

        for (int i = 0; i < num_students; i++) {
            if (strcmp(input_username, students[i].username) == 0 &&
                strcmp(input_password, students[i].password) == 0 &&
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
            printf("Login failed, remaining attempts: %d. Reminder: the computer will shut down when attempts run out\n", 3 - attempts);
        }
    }

    printf("Don't even think about trying to brute-force the password. I gave you three chances and a verification code to prevent you from doing so. Shutting down now, bye.\n");
    shutdown_functions();
}
