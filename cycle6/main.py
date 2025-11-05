"""
Komodo Hub - Main Application
Main application with usage examples
"""

from datetime import datetime, date
from database import db
from models.user_models import User, Organization, OrganizationMember, UserProfile
from models.class_models import Class, ClassEnrollment, Activity, Submission, Assessment
from models.program_models import (Program, ProgramEnrollment, ContentLibrary,
                                   SpeciesSighting, CreativeCanvas, Message, Note)
from models.analytics_models import AccessLog, BusinessAnalytics
from services import (PermissionService, TeacherService, StudentService,
                      PrincipalService, PublicService)


class KomodoHub:
    """Komodo Hub main application class"""

    def __init__(self):
        self.db = db
        print("🦎 Komodo Hub System Initialized")
        print("=" * 50)

    def initialize_database(self):
        """Initialize database connection"""
        try:
            self.db.connect()
            print("✅ Database connected successfully")
            return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False

    def close(self):
        """Close database connection"""
        self.db.close()
        print("Database connection closed")

    # ==================== Example usage scenarios ====================

    def example_user_registration(self):
        """Example: user registration process"""
        print("\n📝 Example: User Registration")
        print("-" * 50)

        try:
            # Create users of different types
            admin_id = User.create_user(
                username="admin_komodo",
                email="admin@komodo.org",
                password="secure_password",
                user_type=User.ADMIN
            )
            print(f"✅ Admin created with ID: {admin_id}")

            principal_id = User.create_user(
                username="principal_khairunnisa",
                email="khairunnisa@school.edu",
                password="principal_pass",
                user_type=User.PRINCIPAL,
                user_image="3"
            )
            print(f"✅ Principal created with ID: {principal_id}")

            teacher_id = User.create_user(
                username="teacher_bintang",
                email="bintang@school.edu",
                password="teacher_pass",
                user_type=User.TEACHER,
                user_image="5"
            )
            print(f"✅ Teacher created with ID: {teacher_id}")

            student_id = User.create_user(
                username="student_adi",
                email="adi@student.edu",
                password="student_pass",
                user_type=User.STUDENT,
                user_image="7"
            )
            print(f"✅ Student created with ID: {student_id}")

            return {
                'admin': admin_id,
                'principal': principal_id,
                'teacher': teacher_id,
                'student': student_id
            }

        except Exception as e:
            print(f"❌ Error in registration: {e}")
            return None

    def example_school_setup(self, principal_id: int):
        """Example: school setup process"""
        print("\n🏫 Example: School Setup")
        print("-" * 50)

        try:
            # Create school organization
            school_id = Organization.create_organization(
                org_type=Organization.SCHOOL,
                org_name="Green Valley International School",
                org_profile="A leading school in environmental education",
                is_public=True,
                subscription_status=Organization.ACTIVE
            )
            print(f"✅ School created with ID: {school_id}")

            # Add principal to the organization
            OrganizationMember.add_member(
                org_id=school_id,
                user_id=principal_id,
                role=OrganizationMember.PRINCIPAL
            )
            print(f"✅ Principal added to school")

            # Update subscription status
            Organization.update_subscription(
                school_id,
                Organization.ACTIVE,
                date.today()
            )
            print(f"✅ Subscription activated")

            return school_id

        except Exception as e:
            print(f"❌ Error in school setup: {e}")
            return None

    def example_class_creation(self, school_id: int, teacher_id: int):
        """Example: class creation process"""
        print("\n📚 Example: Class Creation")
        print("-" * 50)

        try:
            # Add teacher to school
            OrganizationMember.add_member(
                org_id=school_id,
                user_id=teacher_id,
                role=OrganizationMember.TEACHER
            )
            print(f"✅ Teacher added to school")

            # Create class
            class_id = Class.create_class(
                org_id=school_id,
                teacher_id=teacher_id,
                class_name="Introduction to Biodiversity",
                syllabus="Study of ecosystem diversity and endangered species"
            )
            print(f"✅ Class created with ID: {class_id}")

            return class_id

        except Exception as e:
            print(f"❌ Error in class creation: {e}")
            return None

    def example_student_enrollment(self, school_id: int, class_id: int,
                                   student_id: int, principal_id: int):
        """Example: student enrollment process"""
        print("\n👨‍🎓 Example: Student Enrollment")
        print("-" * 50)

        try:
            # Add student to school
            OrganizationMember.add_member(
                org_id=school_id,
                user_id=student_id,
                role=OrganizationMember.STUDENT
            )
            print(f"✅ Student added to school")

            # Generate access code
            access_code = PrincipalService.generate_student_access_code(
                principal_id, school_id, student_id
            )
            print(f"✅ Access code generated: {access_code}")

            # Student enrolls in class
            enrollment_id = ClassEnrollment.enroll_student(class_id, student_id)
            print(f"✅ Student enrolled in class with ID: {enrollment_id}")

            # Create student profile (private)
            profile_id = UserProfile.create_profile(
                user_id=student_id,
                color_scheme="blue",
                bio="Passionate about wildlife conservation",
                is_public=False  # Student profile is not public
            )
            print(f"✅ Student profile created (private)")

            return enrollment_id

        except Exception as e:
            print(f"❌ Error in student enrollment: {e}")
            return None

    def example_teaching_workflow(self, teacher_id: int, class_id: int):
        """Example: teaching workflow"""
        print("\n👨‍🏫 Example: Teaching Workflow")
        print("-" * 50)

        try:
            # Create conservation program
            program_id = Program.create_program(
                program_name="Komodo Dragon Conservation",
                program_type=Program.LOCAL,
                description="Local conservation effort for Komodo dragons"
            )
            print(f"✅ Program created with ID: {program_id}")

            # Create class activity
            activity_id = Activity.create_activity(
                program_id=program_id,
                activity_name="Field Survey Report",
                activity_type=Activity.ASSESSMENT,
                created_by=teacher_id,
                class_id=class_id,
                description="Submit a report on local wildlife observations"
            )
            print(f"✅ Activity created with ID: {activity_id}")

            # Get teacher dashboard
            dashboard = TeacherService.get_teacher_dashboard(teacher_id)
            print(f"✅ Teacher dashboard loaded:")
            print(f"   - Total classes: {dashboard['total_classes']}")
            print(f"   - Total students: {dashboard['total_students']}")
            print(f"   - Pending submissions: {dashboard['pending_submissions']}")

            return activity_id

        except Exception as e:
            print(f"❌ Error in teaching workflow: {e}")
            return None

    def example_student_workflow(self, student_id: int, activity_id: int):
        """Example: student learning workflow"""
        print("\n📝 Example: Student Learning Workflow")
        print("-" * 50)

        try:
            # Student submits assignment
            submission_id = StudentService.submit_assignment(
                student_id=student_id,
                activity_id=activity_id,
                submission_data="Observed 3 Komodo dragons near the coastal area..."
            )
            print(f"✅ Assignment submitted with ID: {submission_id}")

            # Student reports species sighting
            sighting_id = SpeciesSighting.create_sighting(
                species_name="Varanus komodoensis",
                location="Komodo National Park - Beach Area",
                date_time=datetime.now(),
                reported_by=student_id,
                description="Three adult Komodo dragons observed hunting"
            )
            print(f"✅ Species sighting reported with ID: {sighting_id}")

            # Get student dashboard
            dashboard = StudentService.get_student_dashboard(student_id)
            print(f"✅ Student dashboard loaded:")
            print(f"   - Total classes: {dashboard['total_classes']}")
            print(f"   - Total programs: {dashboard['total_programs']}")
            print(f"   - Total submissions: {dashboard['total_submissions']}")

            return submission_id

        except Exception as e:
            print(f"❌ Error in student workflow: {e}")
            return None

    def example_grading_workflow(self, teacher_id: int, submission_id: int):
        """Example: grading workflow"""
        print("\n📊 Example: Grading Workflow")
        print("-" * 50)

        try:
            # Teacher grades assignment
            assessment_id = TeacherService.grade_submission(
                teacher_id=teacher_id,
                submission_id=submission_id,
                grade="A",
                feedback="Excellent observation! Your report shows great attention to detail."
            )
            print(f"✅ Assignment graded with assessment ID: {assessment_id}")

            # Teacher adds note
            note_id = Note.create_note(
                teacher_id=teacher_id,
                target_type=Note.TARGET_SUBMISSION,
                target_id=submission_id,
                note_text="Student shows strong fieldwork skills"
            )
            print(f"✅ Note added with ID: {note_id}")

            return assessment_id

        except Exception as e:
            print(f"❌ Error in grading workflow: {e}")
            return None

    def example_content_library(self, student_id: int, school_id: int):
        """Example: content library operation"""
        print("\n📖 Example: Content Library")
        print("-" * 50)

        try:
            # Student uploads work to school library
            content_id = ContentLibrary.create_content(
                title="My Wildlife Photography Collection",
                content_type=ContentLibrary.PHOTO,
                created_by=student_id,
                content_data="Photos of local endangered species",
                org_id=school_id,
                is_public=True  # School library is public
            )
            print(f"✅ Content uploaded to library with ID: {content_id}")

            # Public browses school library
            public_content = PublicService.get_public_content(
                content_type=ContentLibrary.PHOTO,
                limit=10
            )
            print(f"✅ Public can view {len(public_content)} public content items")

            return content_id

        except Exception as e:
            print(f"❌ Error in content library: {e}")
            return None

    def example_analytics_dashboard(self):
        """Example: business analytics dashboard"""
        print("\n📊 Example: Analytics Dashboard")
        print("-" * 50)

        try:
            # Generate dashboard data
            dashboard = BusinessAnalytics.generate_dashboard_data()

            print(f"✅ Dashboard generated:")
            print(f"\n📈 User Demographics:")
            for user_type, count in dashboard['user_demographics'].items():
                print(f"   - {user_type}: {count}")

            print(f"\n📊 Subscription Statistics:")
            for org_type, stats in dashboard['subscription_stats'].items():
                print(f"   - {org_type}:")
                for status, count in stats.items():
                    print(f"     * {status}: {count}")

            print(f"\n🌟 Popular Programs:")
            for program in dashboard['program_popularity'][:5]:
                print(f"   - {program['program_name']}: {program['enrollment_count']} enrollments")

            print(f"\n👥 Daily Active Users: {dashboard['daily_active_users']}")

            return dashboard

        except Exception as e:
            print(f"❌ Error in analytics: {e}")
            return None

    def example_community_workflow(self):
        """Example: community workflow"""
        print("\n🌍 Example: Community Workflow")
        print("-" * 50)

        try:
            # Create community member
            member_id = User.create_user(
                username="community_besoeki",
                email="besoeki@community.org",
                password="community_pass",
                user_type=User.COMMUNITY_MEMBER
            )
            print(f"✅ Community member created with ID: {member_id}")

            # Create community organization
            community_id = Organization.create_organization(
                org_type=Organization.COMMUNITY,
                org_name="Flores Conservation Network",
                org_profile="Community-led conservation initiative",
                is_public=True
            )
            print(f"✅ Community created with ID: {community_id}")

            # Add member to community
            OrganizationMember.add_member(
                org_id=community_id,
                user_id=member_id,
                role=OrganizationMember.MEMBER
            )
            print(f"✅ Member added to community")

            # Create public profile
            profile_id = UserProfile.create_profile(
                user_id=member_id,
                bio="Environmental activist and wildlife photographer",
                is_public=True  # Community member profile is public
            )
            print(f"✅ Public profile created")

            # Contribute article to community library
            article_id = ContentLibrary.create_content(
                title="The Importance of Coral Reef Conservation",
                content_type=ContentLibrary.ARTICLE,
                created_by=member_id,
                content_data="Coral reefs are vital ecosystems...",
                org_id=community_id,
                is_public=True
            )
            print(f"✅ Article published to community library")

            # Public browses community
            community_data = PublicService.get_community_library(community_id)
            print(f"✅ Public can view community:")
            print(f"   - Content items: {len(community_data['content'])}")
            print(f"   - Public members: {len(community_data['members'])}")

            return community_id

        except Exception as e:
            print(f"❌ Error in community workflow: {e}")
            return None

    def run_complete_demo(self):
        """Run complete demonstration"""
        print("\n" + "=" * 50)
        print("🦎 KOMODO HUB - COMPLETE DEMONSTRATION")
        print("=" * 50)

        # Initialize database
        if not self.initialize_database():
            return

        try:
            # 1. User registration
            users = self.example_user_registration()
            if not users:
                return

            # 2. School setup
            school_id = self.example_school_setup(users['principal'])
            if not school_id:
                return

            # 3. Create class
            class_id = self.example_class_creation(school_id, users['teacher'])
            if not class_id:
                return

            # 4. Student enrollment
            self.example_student_enrollment(
                school_id, class_id, users['student'], users['principal']
            )

            # 5. Teaching workflow
            activity_id = self.example_teaching_workflow(users['teacher'], class_id)
            if not activity_id:
                return

            # 6. Student learning workflow
            submission_id = self.example_student_workflow(users['student'], activity_id)
            if not submission_id:
                return

            # 7. Grading workflow
            self.example_grading_workflow(users['teacher'], submission_id)

            # 8. Content library operation
            self.example_content_library(users['student'], school_id)

            # 9. Community workflow
            self.example_community_workflow()

            # 10. Analytics dashboard
            self.example_analytics_dashboard()

            print("\n" + "=" * 50)
            print("✅ COMPLETE DEMONSTRATION FINISHED SUCCESSFULLY!")
            print("=" * 50)

        except Exception as e:
            print(f"\n❌ Demo failed: {e}")
            import traceback
            traceback.print_exc()

        finally:
            self.close()


def main():
    """Main function"""
    app = KomodoHub()

    # Run complete demonstration
    app.run_complete_demo()


if __name__ == "__main__":
    main()
