#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define max_students 1000
#define max_teachers 100
#define max_assistants 10
#define max_administrators 10
#define max_emails 10000
#define max_forums 10000
#define max_courses 100

#include"type_define.h"
#include"common_functions.h"
#include"students_operations.h"
#include"teachers_operations.h"
#include"assistants_operations.h"
#include"administrators_operations.h"
#include"visitors_operations.h"


Student students[max_students];
Teacher teachers[max_teachers];
Assistant assistants[max_assistants];
Administrator administrators[max_administrators];

Email emails[max_emails];

Forum forums[max_forums];

Course courses[max_courses];


int num_courses;

int** students_course_score = (int**)malloc(num_students * sizeof(int*));


int main() {
	synchronise_from_txt_to_students_array(students);
	synchronise_from_txt_to_teachers_array(teachers);
	synchronise_from_txt_to_assistants_array(assistants);
	synchronise_from_txt_to_administrators_array(administrators);
    
	int num_students = get_students_number();
	int num_teachers = get_teachers_number();
	int num_assistants = get_assistants_number();
	int num_administrators = get_administrators_number();
    int num_emails = get_num_emails_and_synchronise_from_txt_to_emails_array(emails);
    int num_forums = get_num_forums_and_synchronise_from_txt_to_forums_array_and_create_chain(forums);
    
    int num_courses = get_num_courses_and_synchronise_from_txt_to_courses_array_and_create_chain(courses);
    
    /*int students_courses_score[num_students][num_courses];*/

    
    for (int i = 0; i < num_students; i++) {
        students_course_score[i] = (int*)malloc(num_courses * sizeof(int));
    }

    FILE* file = fopen("students_course_score.txt", "r");
    

    for (int i = 0; i < num_students; i++) {
        for (int j = 0; j < num_courses; j++) {
            fscanf(file, "%d", &students_course_score[i][j]);
        }
    }



    fclose(file);


       
	printf("**********************************\n");
	printf("Welcome to Communication University of China One-stop Service Platform\n");
	printf("**********************************\n");
   
    
    int user_type_chosen_in_the_main_menu;


    while (1) {
        
        printf("Please select user type:\n");
        printf("1. Student\t2. Teacher\t3. Academic Assistant\n4. Administrator\t5. Visitor (including unregistered freshmen, new staff, all new members of CUC)\n6. Exit\n");
        scanf("%d", &user_type_chosen_in_the_main_menu);
        switch (user_type_chosen_in_the_main_menu) {
        // Student operations
        case 1:
            students_operations();
            break;
        // Teacher operations
        case 2:
            teachers_operations();
            break;
        // Academic assistant operations
        case 3:
            assistants_operations();
            break;
        // Administrator operations
        case 4:
            administrators_operations();
            break;
        // Visitor operations
        case 5:
            visitors_operations();
            break;
        case 6:
            printf("Exited\n");
            exit(0);
        default:
            printf("Invalid user type entered\n");
            printf("Please re-enter:\n");
            break;
        }
        if ((user_type_chosen_in_the_main_menu >= 1 && user_type_chosen_in_the_main_menu <= 6)) {
            break;
        }
    }


    // Free memory
    for (int i = 0; i < num_students; i++) {
        free(students_course_score[i]);
    }
    free(students_course_score);



    return 0;
}
