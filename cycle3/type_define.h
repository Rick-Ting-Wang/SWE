#pragma once

typedef struct Student{
    char username[10];
    char password[10];
	Student* next;
} Student;



typedef struct {
    char username[10];
    char password[10];
} Teacher;


typedef struct {
    char username[10];
    char password[10];
} Assistant;


typedef struct {
    char username[10];
    char password[10];
} Administrator;

// One-stop platform uses student/employee number to send and receive emails, character length does not exceed 50
typedef struct {
    char sender[10];
    char receiver[10];
    char topic[10];    
    char content[50];
    double time;
} Email;


typedef struct Forum {
	char writer[10];
	char topic[10];
	char content[50];
	double time;
	struct Forum* next;  
} Forum;

typedef struct Course {
	char course_code[20];
	char teacher[10];
	char course_name[50];
	int course_credit;
	struct Course* next;
	struct Student* choose_this_course;
} Course;


extern int num_students;
extern int num_courses;
extern int** students_course_score;



void add_new_student();
void add_new_teacher();
void add_new_assistant();
void add_new_administrator();

int get_students_number();
int get_teachers_number();
int get_assistants_number();
int get_administrators_number();

void synchronise_from_txt_to_students_array(Student students[]);
void synchronise_from_txt_to_teachers_array(Teacher teachers[]);
void synchronise_from_txt_to_assistants_array(Assistant assistants[]);
void synchronise_from_txt_to_administrators_array(Administrator administrators[]);

int get_num_emails_and_synchronise_from_txt_to_emails_array(Email emails[]);
int get_num_forums_and_synchronise_from_txt_to_forums_array_and_create_chain(Forum forums[]);
int get_num_courses_and_synchronise_from_txt_to_courses_array_and_create_chain(Course courses[]);


extern Course courses[max_courses];

// Add new user: student, teacher, assistant, administrator
void add_new_student() {
	num_students = get_students_number();
	num_courses = get_num_courses_and_synchronise_from_txt_to_courses_array_and_create_chain(courses);

	FILE* file_students_course_score_read;
	file_students_course_score_read	= fopen("students_course_score.txt", "r");


	for (int i = 0; i < num_students; i++) {
		for (int j = 0; j < num_courses; j++) {
			fscanf(file_students_course_score_read, "%d", &students_course_score[i][j]);
		}
	}

	fclose(file_students_course_score_read);

	FILE* file;
	Student newstudent[1];


	file = fopen("students.txt", "a");
	printf("Please enter the new student ID:\n");
	scanf("%s", newstudent[0].username);
	printf("Please enter the new student password (initial password is name):\n");
	scanf("%s", newstudent[0].password);
	fprintf(file, "%s %s\n", newstudent[0].username, newstudent[0].password);

	fclose(file);
	printf("Entry successful!\n");
	num_students++;
	students_course_score = (int**)realloc(students_course_score, num_students * sizeof(int*));
	students_course_score[num_students - 1] = (int*)malloc(num_courses * sizeof(int));


	for (int i = 0; i < num_students - 1; i++) {
		for (int j = 0; j < num_courses; j++) {
			students_course_score[num_students - 1][j] = students_course_score[i][j];
		}
	}

	
	for (int j = 0; j < num_courses; j++) {
		students_course_score[num_students - 1][j] = -2;
	}
	
	FILE* file_students_course_score;

	file_students_course_score = fopen("students_course_score.txt", "w");

	for (int i = 0; i < num_students; i++) {
		for (int j = 0; j < num_courses; j++) {
			fprintf(file_students_course_score, "%d ",students_course_score[i][j]);
		}
		fprintf(file_students_course_score, "\n");
	}
	
	fclose(file_students_course_score);
	
}

void add_new_teacher() {
	FILE* file;
	Teacher newteacher[1];
	file = fopen("teachers.txt", "a");
	printf("Please enter the new teacher ID:\n");
	scanf("%s", newteacher[0].username);
	printf("Please enter the new teacher password (initial password is name):\n");
	scanf("%s", newteacher[0].password);
	fprintf(file, "%s %s\n", newteacher[0].username, newteacher[0].password);
	fclose(file);
	printf("Entry successful!\n");
}

void add_new_assistant() {
	FILE* file;
	Assistant newassistant[1];
	file = fopen("assistants.txt", "a");
	printf("Please enter the new assistant ID:\n");
	scanf("%s", newassistant[0].username);
	printf("Please enter the new assistant password (initial password is name):\n");
	scanf("%s", newassistant[0].password);
	fprintf(file, "%s %s\n", newassistant[0].username, newassistant[0].password);
	fclose(file);
	printf("Entry successful!\n");
}

void add_new_administrator() {
	FILE* file;
	Administrator newadministrator[1];
	file = fopen("administrators.txt", "a");
	printf("Please enter the new administrator ID:\n");
	scanf("%s", newadministrator[0].username);
	printf("Please enter the new administrator password (initial password is name):\n");
	scanf("%s", newadministrator[0].password);
	fprintf(file, "%s %s\n", newadministrator[0].username, newadministrator[0].password);
	fclose(file);
	printf("Entry successful!\n");
}


// View the number of four types of users
int get_students_number() {
	FILE* file;
	file = fopen("students.txt", "r");
	int num_students = 0;
	char line[100];
	while (fgets(line, sizeof(line), file) != NULL) {
		num_students++;
	}
	fclose(file);
	return(num_students);
	
}

int get_teachers_number() {
	FILE* file;
	file = fopen("teachers.txt", "r");
	int num_teachers = 0;
	char line[100];
	while (fgets(line, sizeof(line), file) != NULL) {
		num_teachers++;
	}
	fclose(file);
	return(num_teachers);
}

int get_assistants_number() {
	FILE* file;
	file = fopen("assistants.txt", "r");
	int num_assistants = 0;
	char line[100];
	while (fgets(line, sizeof(line), file) != NULL) {
		num_assistants++;
	}
	fclose(file);
	return(num_assistants);
}

int get_administrators_number() {
	FILE* file;
	file = fopen("administrators.txt", "r");
	int num_administrators = 0;
	char line[100];
	while (fgets(line, sizeof(line), file) != NULL) {
		num_administrators++;
	}
	fclose(file);
	return(num_administrators);
}



// Synchronize to the struct array of four types of users
void synchronise_from_txt_to_students_array(Student students[]) {
	FILE* file;
	file = fopen("students.txt", "r");
	int num_students = 0;
	while (fscanf(file, "%s %s", students[num_students].username, students[num_students].password) == 2) {
		num_students++;
	}
}

void synchronise_from_txt_to_teachers_array(Teacher teachers[]) {
	FILE* file;
	file = fopen("teachers.txt", "r");
	int num_teachers = 0;
	while (fscanf(file, "%s %s", teachers[num_teachers].username, teachers[num_teachers].password) == 2) {
		num_teachers++;
	}
}

void synchronise_from_txt_to_assistants_array(Assistant assistants[]) {
	FILE* file;
	file = fopen("assistants.txt", "r");
	int num_assistants = 0;
	while (fscanf(file, "%s %s", assistants[num_assistants].username, assistants[num_assistants].password) == 2) {
		num_assistants++;
	}

}

void synchronise_from_txt_to_administrators_array(Administrator administrators[]) {
	FILE* file;
	file = fopen("administrators.txt", "r");
	int num_administrators = 0;
	while (fscanf(file, "%s %s", administrators[num_administrators].username, administrators[num_administrators].password) == 2) {
		num_administrators++;
	}
}

// Email synchronization and return the number of emails
int get_num_emails_and_synchronise_from_txt_to_emails_array(Email emails[]) {
	FILE* file;
	file = fopen("emails.txt", "r");
	int num_emails=0;
	while (fscanf(file, "%s %s %s %s %lf", emails[num_emails].sender, 
		emails[num_emails].receiver,
		emails[num_emails].topic,
		emails[num_emails].content,
		&emails[num_emails].time
		) == 5) {
		num_emails++;
	}
	

	return(num_emails);
}

// Forum synchronization, return the number of posts and create a linked list
int get_num_forums_and_synchronise_from_txt_to_forums_array_and_create_chain(Forum forums[]) {
	FILE* file;
	file = fopen("forums.txt", "r");
	int num_forums = 0;
	while (fscanf(file, "%s %s %s %lf", forums[num_forums].writer,
		forums[num_forums].topic,
		forums[num_forums].content,
		&forums[num_forums].time
	) == 4) {
		num_forums++;
	}
	fclose(file);
	Forum* head = &forums[0];

	
	for (int i = 0; i < num_forums - 1; i++) {
		forums[i].next = &forums[i + 1];
	}
	forums[num_forums - 1].next = NULL;
	return(num_forums);
}

int get_num_courses_and_synchronise_from_txt_to_courses_array_and_create_chain(Course courses[]){
	FILE* file;
	file = fopen("course.txt", "r");
	int num_courses = 0;
	while (fscanf(file, "%s %s %s %d", courses[num_courses].course_code,
		courses[num_courses].teacher,
		courses[num_courses].course_name,
		&courses[num_courses].course_credit) == 4) {
		num_courses++;
	}
	fclose(file);
	Course* head = &courses[0];

	for (int i = 0; i < num_courses; i++) {
		courses[i].next = &courses[i + 1];
	}
	courses[num_courses - 1].next = NULL;
	return(num_courses);
}
