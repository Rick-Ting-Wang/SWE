#pragma once
void assistants_operations();
char* assistants_login();
extern Assistant assistants[];
extern Course courses[];


extern Student students[];


extern int num_courses;
extern int num_students;
extern int** students_course_score;


void assistants_operations() {
    num_students = get_students_number();
    num_courses = get_num_courses_and_synchronise_from_txt_to_courses_array_and_create_chain(courses);

    FILE* file_students_course_score_read;
    file_students_course_score_read = fopen("students_course_score.txt", "r");


    for (int i = 0; i < num_students; i++) {
        for (int j = 0; j < num_courses; j++) {
            fscanf(file_students_course_score_read, "%d", &students_course_score[i][j]);
        }
    }

    fclose(file_students_course_score_read);

    printf("Launching assistant-side program\n");
    char* username = NULL;
    username = assistants_login();
    printf("Welcome to the CUC One-Stop Service Platform\n");
    printf("You have logged in as %s\n", username);
    int choice;
    {
        printf("Please select a module:\n");
        printf("1. Change password\n");
        printf("2. Campus email\n");
        printf("3. CUC Walnut Forest Forum\n");
        printf("4. View academic warning list\n");
        printf("5. Exit\n");
        printf("6. Add course and notify students via email\n");
        printf("7. Delete course and notify teachers and students via email\n");


        do {
            scanf("%d", &choice);
            switch (choice) {
            case 1:
                printf("%s, you are about to change your password\n", username);
                printf("After changing, please restart the computer for it to take effect\n");
                change_password_assistants(username);
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
                printf("%s, you are about to view the academic warning list\n", username);
                num_students = get_students_number();
                num_courses = get_num_courses_and_synchronise_from_txt_to_courses_array_and_create_chain(courses);

                FILE* file_students_course_score_readd;
                file_students_course_score_readd = fopen("students_course_score.txt", "r");


                for (int i = 0; i < num_students; i++) {
                    for (int j = 0; j < num_courses; j++) {
                        fscanf(file_students_course_score_readd, "%d", &students_course_score[i][j]);
                    }
                }


                fclose(file_students_course_score_readd);

                printf("List of students who failed:\n");
                for (int i = 0; i < num_students; i++) {
                    for (int j = 0; j < num_courses; j++) {
                        if (students_course_score[i][j] >= 0 && students_course_score[i][j] < 60) {

                            printf("Course code: %s Course name: %s Student name: %s Credits: %d Score: %d\n", courses[j].course_code, courses[j].course_name, students[i].username, courses[j].course_credit, students_course_score[i][j]);
                        }
                    }
                }


                break;
            case 5:
                printf("Thank you for using! Goodbye.\n");
                break;
            case 6:

                printf("Executing add course module!\n");
                printf("Please enter the number of courses to be added this time:\n");
                int add_course_num;

                scanf("%d", &add_course_num);
                FILE* file;
                file = fopen("emails.txt", "a");
                for (int i = 0; i < num_students; i++) {
                    fprintf(file, "%s %s Notice %d new courses %lf\n", username, students[i].username, add_course_num, return_current_time_for_later_comparison());
                }
                for (int i = 1; i <= add_course_num; i++) {
                    Course newcourse[1];
                    printf("Please enter course code:\n");
                    scanf("%s", newcourse[0].course_code);
                    printf("Please select the course teacher:\n");
                    for (int j = 0; j < num_teachers; j++) {
                        printf("%s\n", teachers[j].username);
                    }
                    scanf("%s", newcourse[0].teacher);
                    printf("Please enter the course name:\n");
                    scanf("%s", newcourse[0].course_name);
                    printf("Please enter course credits:\n");
                    scanf("%d", &newcourse[0].course_credit);
                    FILE* file_newcourse;
                    file_newcourse = fopen("course.txt", "a");
                    if (file_newcourse != NULL) {
                        fprintf(file_newcourse, "%s %s %s %d\n", newcourse[0].course_code, newcourse[0].teacher, newcourse[0].course_name, newcourse[0].course_credit);
                        fclose(file_newcourse);
                        printf("Course has been added successfully.\n");
                    }
                    else {
                        printf("Unable to open file for writing.\n");
                    }
                    num_courses++;

                    students_course_score[num_students] = (int*)malloc(num_courses * sizeof(int));





                    for (int i = 0; i < num_students; i++) {
                        students_course_score[num_students] = (int*)malloc(num_courses * sizeof(int));
                        students_course_score[i][num_courses - 1] = -2;
                    }

                    FILE* file_students_course_score_write;
                    file_students_course_score_write = fopen("students_course_score.txt", "w");


                    for (int i = 0; i < num_students; i++) {
                        for (int j = 0; j < num_courses; j++) {
                            fprintf(file_students_course_score_write, "%d ", students_course_score[i][j]);
                        }
                        fprintf(file_students_course_score_write, "\n");
                    }

                    fclose(file_students_course_score_write);

                }


                break;
            case 7:
                printf("Executing delete course operation:\n");
                printf("The following courses currently exist:\n");

                num_students = get_students_number();
                num_courses = get_num_courses_and_synchronise_from_txt_to_courses_array_and_create_chain(courses);

                FILE* file_students_course_score_readdd;
                file_students_course_score_readdd = fopen("students_course_score.txt", "r");


                for (int i = 0; i < num_students; i++) {
                    for (int j = 0; j < num_courses; j++) {
                        fscanf(file_students_course_score_readdd, "%d", &students_course_score[i][j]);
                    }
                }
                fclose(file_students_course_score_readdd);

                //
                for (int i = 0; i < num_courses; i++) {
                    printf("%s %s Teacher: %s Credits: %d ", courses[i].course_code, courses[i].teacher, courses[i].course_name, courses[i].course_credit);
                    int count = 0;
                    for (int j = 0; j < num_students; j++) {

                        if (students_course_score[j][i] > -2) {
                            count++;
                        }

                    }
                    printf("Number of students enrolled: %d\n", count);
                }

                printf("How many courses do you want to delete?\n");
                int num_course_to_delete;
                scanf("%d", &num_course_to_delete);

                for (int i = 1; i <= num_course_to_delete; i++) {
                    printf("Please enter the name of course No.%d to be deleted\n", i);
                    char coursename[100];
                    scanf("%s", coursename);
                    int courses_to_delete = -1;
                    for (int j = 0; j < num_courses; j++) {

                        if (strcmp(courses[j].course_name, coursename) == 0) {
                            courses_to_delete = j;
                            break;
                        }
                    }


                    if (courses_to_delete != -1) {
                        FILE* file_emails;

                        // Edit email to notify teacher
                        file_emails = fopen("emails.txt", "a");
                        fprintf(file_emails, "%s %s Notice Course %s is cancelled due to insufficient enrollment %lf\n", username, courses[courses_to_delete].teacher, courses[courses_to_delete].course_name, return_current_time_for_later_comparison());
                        for (int i = courses_to_delete; i < num_courses - 1; i++) {
                            courses[i] = courses[i + 1];
                        }
                        num_courses--;

                        Course* head = &courses[0];
                        Course* p = head;
                        for (int i = 0; i < num_courses - 1; i++) {
                            courses[i].next = &courses[i + 1];
                        }
                        courses[num_courses - 1].next = NULL;

                        FILE* file = fopen("course.txt", "w");


                        for (int i = 0; i < num_courses; i++) {
                            fprintf(file, "%s %s %s %d\n", courses[i].course_code,
                                courses[i].teacher,
                                courses[i].course_name,
                                courses[i].course_credit);

                        }
                        fclose(file);

                        printf("Course %s and related information have been deleted\n", coursename);

                        // Edit email to notify students

                        for (int i = 0; i < num_students; i++) {
                            fprintf(file_emails, "%s %s Notice %d course(s) have been deleted %lf\n", username, students[i].username, num_course_to_delete, return_current_time_for_later_comparison());
                        }


                        fclose(file);
                        // Update grades table
                        for (int j = 0; j < num_students; j++) {
                            for (int k = courses_to_delete; k < num_courses; k++) {
                                students_course_score[j][k] = students_course_score[j][k + 1];
                            }
                            students_course_score[j] = (int*)realloc(students_course_score[j], (num_courses) * sizeof(int));
                        }

                        FILE* file_students_course_score_write;
                        file_students_course_score_write = fopen("students_course_score.txt", "w");

                        for (int j = 0; j < num_students; j++) {
                            for (int k = 0; k < num_courses; k++) {
                                fprintf(file_students_course_score_write, "%d ", students_course_score[j][k]);
                            }
                            fprintf(file_students_course_score_write, "\n");
                        }

                        fclose(file_students_course_score_write);




                    }
                    else {
                        printf("Course %s was not found\n", coursename);
                    }
                }



                break;



            }
        } while (choice != 5);


        }
    }

// Login function
char* assistants_login() {
    printf("Please log in, the computer will shut down after three failed attempts:\n");

    int attempts = 0;
    int correct = 0;

    int num_assistants = get_assistants_number();

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
        for (int i = 0; i < num_assistants; i++) {
            if (strcmp(input_username, assistants[i].username) == 0 &&
                strcmp(input_password, assistants[i].password) == 0 &&
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
