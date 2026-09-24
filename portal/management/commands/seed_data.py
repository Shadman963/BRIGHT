from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.utils import timezone
from core.models import Testimonial, FAQ
from universities.models import University, Program, Scholarship
from portal.models import (
    StudentProfile,
    StudentApplication,
    ApplicationDocument,
    ApplicationTimeline
)

class Command(BaseCommand):
    help = "Seeds database with initial users, Chinese universities, programs, scholarships, and sample student application tracking."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Starting database seeding for Bright Edu Consultancy..."))

        # 1. Create Superuser (Admin)
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@brighteduconsultancy.com',
                'first_name': 'Chief',
                'last_name': 'Administrator',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created Superuser: admin / admin123"))
        else:
            self.stdout.write("Admin superuser already exists.")

        # 2. Create Staff Counselor
        counselor_user, created = User.objects.get_or_create(
            username='counselor',
            defaults={
                'email': 'counselor@brighteduconsultancy.com',
                'first_name': 'Senior',
                'last_name': 'Counselor',
                'is_staff': True,
            }
        )
        if created:
            counselor_user.set_password('counselor123')
            counselor_user.save()
            self.stdout.write(self.style.SUCCESS("Created Counselor Staff: counselor / counselor123"))

        # 3. Create Demo Student
        student_user, created = User.objects.get_or_create(
            username='student@brightedu.com',
            defaults={
                'email': 'student@brightedu.com',
                'first_name': 'Tariqul',
                'last_name': 'Islam',
            }
        )
        if created:
            student_user.set_password('student123')
            student_user.save()
            StudentProfile.objects.create(
                user=student_user,
                phone='+880 1711 987654',
                nationality='Bangladesh',
                passport_number='A09876543',
                current_address='House 14, Road 5, Dhanmondi, Dhaka-1209'
            )
            self.stdout.write(self.style.SUCCESS("Created Demo Student: student@brightedu.com / student123"))

        # 4. Seed Scholarships
        sch_csc_b, _ = Scholarship.objects.get_or_create(
            name="Chinese Government Scholarship (CSC Type B - High-Level Postgraduate)",
            defaults={
                'scholarship_type': 'csc_type_b',
                'coverage': '100% Tuition Waiver + Free Campus Apartment + Comprehensive Medical Insurance',
                'monthly_stipend': '3,000 RMB/month (Master), 3,500 RMB/month (PhD)',
                'eligibility': 'Bachelor degree holders under 35 with minimum CGPA 3.2/4.0',
                'description': 'Direct university nomination for master and doctoral candidates in engineering, science, and AI.'
            }
        )

        sch_provincial, _ = Scholarship.objects.get_or_create(
            name="Zhejiang Provincial Government International Student Scholarship",
            defaults={
                'scholarship_type': 'provincial',
                'coverage': '100% Full Tuition Waiver + Free University Accommodation',
                'monthly_stipend': '2,000 RMB/month for 10 months/year',
                'eligibility': 'High school graduates with minimum 75% marks or CGPA 4.5/5.0',
                'description': 'Sponsored by Zhejiang provincial government for undergraduate and master students.'
            }
        )

        sch_belt_road, _ = Scholarship.objects.get_or_create(
            name="Belt and Road Silk Road Scholarship",
            defaults={
                'scholarship_type': 'belt_road',
                'coverage': 'Full Tuition Waiver + Free Campus Dormitory',
                'monthly_stipend': '2,500 RMB/month',
                'eligibility': 'Citizens of Belt and Road partner countries with strong academic records',
                'description': 'Encourages cross-cultural technological and trade education.'
            }
        )

        sch_president, _ = Scholarship.objects.get_or_create(
            name="University Presidential Excellence Award",
            defaults={
                'scholarship_type': 'university',
                'coverage': '100% Tuition Fee Waiver for All 4 Years',
                'monthly_stipend': '1,500 RMB/month',
                'eligibility': 'Undergraduate and Master applicants with outstanding English proficiency and leadership.',
                'description': 'University-funded grant for exceptional international applicants.'
            }
        )

        # 5. Seed Top Universities
        unis_data = [
            {
                'name': 'Tsinghua University',
                'chinese_name': '清华大学',
                'slug': 'tsinghua-university',
                'city': 'Beijing',
                'province': 'Beijing',
                'ranking_national': 1,
                'ranking_world': 14,
                'has_csc_scholarship': True,
                'has_provincial_scholarship': True,
                'is_featured': True,
                'established_year': 1911,
                'cover_image_url': 'https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=1000&auto=format&fit=crop&q=80',
                'description': 'Ranked #1 in China and #14 in the world, Tsinghua University is an elite C9 League institution celebrated globally for engineering, artificial intelligence, computer science, and international policy programs.',
                'campus_highlights': 'Sprawling royal garden campus in northwest Beijing with state-of-the-art supercomputing centers, modern single dormitories for international scholars, and Olympic-grade sports complexes.'
            },
            {
                'name': 'Peking University',
                'chinese_name': '北京大学',
                'slug': 'peking-university',
                'city': 'Beijing',
                'province': 'Beijing',
                'ranking_national': 2,
                'ranking_world': 17,
                'has_csc_scholarship': True,
                'has_provincial_scholarship': True,
                'is_featured': True,
                'established_year': 1898,
                'cover_image_url': 'https://images.unsplash.com/photo-1562774053-701939374585?w=1000&auto=format&fit=crop&q=80',
                'description': 'Peking University (PKU) is China’s oldest national comprehensive university, famous for humanities, physical sciences, medicine, and international economics.',
                'campus_highlights': 'Scenic Weiming Lake, traditional classical Chinese pavilions, Boya Tower, and the largest university library in East Asia.'
            },
            {
                'name': 'Zhejiang University',
                'chinese_name': '浙江大学',
                'slug': 'zhejiang-university',
                'city': 'Hangzhou',
                'province': 'Zhejiang',
                'ranking_national': 3,
                'ranking_world': 44,
                'has_csc_scholarship': True,
                'has_provincial_scholarship': True,
                'is_featured': True,
                'established_year': 1897,
                'cover_image_url': 'https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=1000&auto=format&fit=crop&q=80',
                'description': 'Located in picturesque Hangzhou, home of Alibaba and Chinese tech innovation, Zhejiang University is a powerhouse for English-medium Clinical Medicine (MBBS), Computer Science, and Civil Engineering.',
                'campus_highlights': 'Zijingang Campus features modern laboratories, scenic canals, international student halls with en-suite bathrooms, and direct high-speed rail access to Shanghai.'
            },
            {
                'name': 'Fudan University',
                'chinese_name': '复旦大学',
                'slug': 'fudan-university',
                'city': 'Shanghai',
                'province': 'Shanghai',
                'ranking_national': 4,
                'ranking_world': 50,
                'has_csc_scholarship': True,
                'has_provincial_scholarship': True,
                'is_featured': True,
                'established_year': 1905,
                'cover_image_url': 'https://images.unsplash.com/photo-1592280771190-3e2e4d571952?w=1000&auto=format&fit=crop&q=80',
                'description': 'Situated in cosmopolitan Shanghai, Fudan University is a prestigious C9 League member renowned for International Business, Economics, Public Health, and English-taught MBBS.',
                'campus_highlights': 'Twin Guanghua Towers landmark, international student cafes, close proximity to Shanghai financial district and major multinational corporate headquarters.'
            },
            {
                'name': 'Harbin Institute of Technology',
                'chinese_name': '哈尔滨工业大学',
                'slug': 'harbin-institute-of-technology',
                'city': 'Harbin',
                'province': 'Heilongjiang',
                'ranking_national': 10,
                'ranking_world': 210,
                'has_csc_scholarship': True,
                'has_provincial_scholarship': True,
                'is_featured': True,
                'established_year': 1920,
                'cover_image_url': 'https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=1000&auto=format&fit=crop&q=80',
                'description': 'A world pioneer in aerospace, robotics, software, and mechanical engineering. HIT has trained many of China’s space program commanders and offers extensive full CSC scholarships.',
                'campus_highlights': 'World-class robotics testing arena, central indoor heated athletic dome, and vibrant international student community.'
            },
            {
                'name': 'Wuhan University',
                'chinese_name': '武汉大学',
                'slug': 'wuhan-university',
                'city': 'Wuhan',
                'province': 'Hubei',
                'ranking_national': 8,
                'ranking_world': 194,
                'has_csc_scholarship': True,
                'has_provincial_scholarship': True,
                'is_featured': True,
                'established_year': 1893,
                'cover_image_url': 'https://images.unsplash.com/photo-1576495199011-eb94736d05d6?w=1000&auto=format&fit=crop&q=80',
                'description': 'Widely acclaimed as the most beautiful university in China with Luojia Mountain scenery, famous for English-taught Clinical Medicine (MBBS), Software Engineering, and International Law.',
                'campus_highlights': 'Cherry blossom campus gardens, historic early 20th-century castle-like lecture halls, modern hospital attachments for medical interns.'
            },
        ]

        uni_objs = {}
        for ud in unis_data:
            uni, _ = University.objects.get_or_create(slug=ud['slug'], defaults=ud)
            uni_objs[ud['slug']] = uni

        self.stdout.write(self.style.SUCCESS(f"Seeded {len(uni_objs)} top Chinese universities."))

        # 6. Seed Academic Programs
        programs_data = [
            # Zhejiang University Programs
            {
                'university': uni_objs['zhejiang-university'],
                'title': 'Clinical Medicine (MBBS) English Taught',
                'slug': 'mbbs-clinical-medicine-english',
                'degree_level': 'Bachelor',
                'discipline': 'Medicine',
                'language_of_instruction': 'English',
                'duration_years': 6.0,
                'annual_tuition_cny': 42800,
                'intake': 'September',
                'application_deadline': 'May 30, 2026',
                'is_popular': True,
                'requirements': 'High School diploma with high grades in Biology, Chemistry, and Physics. English Medium certificate or IELTS 6.0.',
                'curriculum_overview': 'Fully accredited 6-year English MBBS including 1 year of clinical internship at top affiliated tertiary hospitals in Hangzhou. Recognized by WHO, BMDC, PMDC, and ECFMG.',
                'scholarships': [sch_provincial, sch_president]
            },
            {
                'university': uni_objs['zhejiang-university'],
                'title': 'Computer Science & Artificial Intelligence',
                'slug': 'computer-science-and-ai-master',
                'degree_level': 'Master',
                'discipline': 'Computer Science',
                'language_of_instruction': 'English',
                'duration_years': 2.5,
                'annual_tuition_cny': 36800,
                'intake': 'September',
                'application_deadline': 'April 15, 2026',
                'is_popular': True,
                'requirements': 'Bachelor in Computer Science, Software, or Mathematics with CGPA >= 3.2. Two academic recommendation letters.',
                'curriculum_overview': 'Advanced neural networks, big data architectures, computer vision, robotics, and collaborative research with Hangzhou tech enterprises.',
                'scholarships': [sch_csc_b, sch_provincial]
            },
            # Tsinghua University Programs
            {
                'university': uni_objs['tsinghua-university'],
                'title': 'Civil & Environmental Engineering',
                'slug': 'civil-and-environmental-engineering-phd',
                'degree_level': 'PhD',
                'discipline': 'Engineering',
                'language_of_instruction': 'English',
                'duration_years': 4.0,
                'annual_tuition_cny': 40000,
                'intake': 'September',
                'application_deadline': 'March 15, 2026',
                'is_popular': True,
                'requirements': 'Master degree in Civil/Structural/Environmental Engineering. Research proposal and professor recommendation letters.',
                'curriculum_overview': 'Doctoral research in smart resilient mega-structures, sustainable green construction, and urban water resources.',
                'scholarships': [sch_csc_b, sch_belt_road]
            },
            # Fudan University Programs
            {
                'university': uni_objs['fudan-university'],
                'title': 'International Business & Trade (BBA)',
                'slug': 'international-business-and-trade-bachelor',
                'degree_level': 'Bachelor',
                'discipline': 'Business',
                'language_of_instruction': 'English',
                'duration_years': 4.0,
                'annual_tuition_cny': 32000,
                'intake': 'September',
                'application_deadline': 'May 10, 2026',
                'is_popular': True,
                'requirements': 'High school certificate with strong Mathematics and English grades.',
                'curriculum_overview': 'Global finance, Asian supply chains, corporate strategy, digital commerce, with internships across Shanghai multinational corporations.',
                'scholarships': [sch_president, sch_belt_road]
            },
            # Harbin Institute of Technology
            {
                'university': uni_objs['harbin-institute-of-technology'],
                'title': 'Mechanical & Robotics Engineering',
                'slug': 'mechanical-and-robotics-engineering-bachelor',
                'degree_level': 'Bachelor',
                'discipline': 'Engineering',
                'language_of_instruction': 'English',
                'duration_years': 4.0,
                'annual_tuition_cny': 26000,
                'intake': 'September',
                'application_deadline': 'June 15, 2026',
                'is_popular': True,
                'requirements': 'High school marks in Mathematics & Physics >= 70%.',
                'curriculum_overview': 'Mechatronics, automated manufacturing, drone navigation systems, CAD/CAM prototyping.',
                'scholarships': [sch_csc_b, sch_president]
            },
            # Wuhan University
            {
                'university': uni_objs['wuhan-university'],
                'title': 'Intensive Chinese Language & Culture Program',
                'slug': 'chinese-language-culture-program',
                'degree_level': 'Language',
                'discipline': 'Chinese Language',
                'language_of_instruction': 'Chinese',
                'duration_years': 1.0,
                'annual_tuition_cny': 15000,
                'intake': 'Both',
                'application_deadline': 'July 10, 2026',
                'is_popular': False,
                'requirements': 'High school completion. Open to beginners with zero prior Chinese knowledge.',
                'curriculum_overview': 'Comprehensive HSK 1 to HSK 5 preparation, oral communicative Chinese, Chinese calligraphy, and business etiquette.',
                'scholarships': [sch_president]
            },
        ]

        for pdata in programs_data:
            schs = pdata.pop('scholarships', [])
            prog, _ = Program.objects.get_or_create(
                university=pdata['university'],
                slug=pdata['slug'],
                defaults=pdata
            )
            prog.scholarships.set(schs)

        self.stdout.write(self.style.SUCCESS("Seeded academic programs across universities."))

        # 7. Seed Sample Student Application for Demo Student
        app, created = StudentApplication.objects.get_or_create(
            student=student_user,
            defaults={
                'application_id': 'BEC-2026-89201',
                'target_degree': 'Bachelor',
                'preferred_university': uni_objs['zhejiang-university'],
                'preferred_program_name': 'Clinical Medicine (MBBS) English Taught',
                'target_intake': 'Autumn 2026',
                'scholarship_preference': 'Provincial',
                'highest_qualification': 'Higher Secondary Certificate (HSC) Science',
                'institute_name': 'Notre Dame College, Dhaka',
                'graduation_year': 2025,
                'cgpa_or_percentage': 'GPA 5.00 / 5.00',
                'english_proficiency': 'English Medium Instruction Certificate',
                'status': 'Document Checking',
                'status_note': 'Your uploaded High School certificates and transcripts are currently being checked and verified by our senior admissions counselor.',
                'has_missing_documents': False,
            }
        )

        if created:
            # Seed application documents
            sample_docs = [
                ('passport', 'Passport Bio Page Scan', 'verified', 'Clear passport scan valid till 2030 verified.'),
                ('certificate', 'HSC Graduation Certificate', 'verified', 'Official board certificate verified.'),
                ('transcript', 'Official Academic Marksheet', 'verified', 'Transcripts checked and verified.'),
                ('cv', 'Student Academic CV', 'pending', ''),
                ('photo', 'Passport Size Photo', 'pending', ''),
            ]

            for doc_type, title, status, feedback in sample_docs:
                doc = ApplicationDocument(
                    application=app,
                    doc_type=doc_type,
                    title=title,
                    status=status,
                    counselor_feedback=feedback
                )
                doc.file.save(f"{doc_type}_sample.pdf", ContentFile(b"Sample PDF Content for Demonstration"), save=True)

            # Seed timeline history
            ApplicationTimeline.objects.create(
                application=app,
                status='Submitted',
                title='Application Form & Initial Files Submitted',
                note='Student completed online submission for MBBS at Zhejiang University. ID: BEC-2026-89201',
                created_at=timezone.now() - timezone.timedelta(days=3),
                performed_by=student_user
            )
            ApplicationTimeline.objects.create(
                application=app,
                status='Document Checking',
                title='Document Checking Stage Commenced',
                note='Counselor team verified passport and HSC certificate. Academic evaluation underway.',
                created_at=timezone.now() - timezone.timedelta(days=1),
                performed_by=counselor_user
            )
            self.stdout.write(self.style.SUCCESS("Seeded sample student application with documents & timeline."))

        # 8. Seed Testimonials
        testimonials_data = [
            {
                'student_name': 'Rahimul Hasan',
                'home_country': 'Bangladesh',
                'university_admitted': 'Tsinghua University',
                'program_name': 'MSc in Computer Science & AI',
                'degree_level': 'Master',
                'scholarship_received': 'Chinese Government Scholarship (CSC Type B) Full Fund',
                'quote': 'Bright Edu Consultancy managed everything from my CSC scholarship nomination to my JW202 visa processing. Their online tracking portal gave me peace of mind every single week!',
                'rating': 5,
                'intake_year': '2025',
                'is_featured': True,
                'display_order': 1,
            },
            {
                'student_name': 'Anika Tabassum',
                'home_country': 'Bangladesh',
                'university_admitted': 'Zhejiang University',
                'program_name': 'Clinical Medicine (MBBS English Medium)',
                'degree_level': 'Bachelor',
                'scholarship_received': 'Zhejiang Provincial Full Tuition Scholarship',
                'quote': 'Studying MBBS at Zhejiang University was my childhood dream. The counselors helped notarize my documents, prepare my SOP, and the Shanghai branch team picked me up from Pudong airport!',
                'rating': 5,
                'intake_year': '2025',
                'is_featured': True,
                'display_order': 2,
            },
            {
                'student_name': 'Sabbir Ahmed',
                'home_country': 'Bangladesh',
                'university_admitted': 'Harbin Institute of Technology',
                'program_name': 'PhD in Robotics & Aerospace Engineering',
                'degree_level': 'PhD',
                'scholarship_received': 'Silk Road Belt & Road Full Scholarship',
                'quote': 'Bright Edu is by far the most transparent education consultancy in South Asia. No false hopes, realistic guidance, and their counselors respond promptly on WhatsApp.',
                'rating': 5,
                'intake_year': '2024',
                'is_featured': True,
                'display_order': 3,
            },
        ]

        for td in testimonials_data:
            Testimonial.objects.get_or_create(student_name=td['student_name'], defaults=td)

        # 9. Seed FAQs
        faqs_data = [
            {
                'category': 'china',
                'question': 'What are the main benefits of studying in China?',
                'answer': 'China boasts world-leading universities (Tsinghua, Peking, Zhejiang), affordable tuition fees, full CSC government scholarships with living stipends, cutting-edge research facilities, unmatched personal safety, and thriving career opportunities.',
                'display_order': 1
            },
            {
                'category': 'scholarships',
                'question': 'How much is the CSC monthly living allowance?',
                'answer': 'Under CSC Full Scholarship, Bachelor students receive 2,500 RMB/month, Master students receive 3,000 RMB/month, and PhD scholars receive 3,500 RMB/month, in addition to free university apartments and 100% tuition waivers.',
                'display_order': 2
            },
            {
                'category': 'application',
                'question': 'What is the Unique Application ID used for?',
                'answer': 'Each student receives a unique Application ID (e.g. BEC-2026-89201). This allows you to track your 7-stage application progress live, check verified documents, receive counselor notes, and communicate with our admissions team.',
                'display_order': 3
            },
            {
                'category': 'visa',
                'question': 'What is the JW202 form and how do I get it?',
                'answer': 'The JW202 (or JW201/DQ form) is the official Visa Application Notice issued by the Chinese Ministry of Education. Once your university admission is approved, the university dispatches this form, which our team uses to lodge your X1 student visa with the Chinese Embassy.',
                'display_order': 4
            },
        ]

        for fd in faqs_data:
            FAQ.objects.get_or_create(question=fd['question'], defaults=fd)

        self.stdout.write(self.style.SUCCESS("All seed data created successfully! Ready for launch."))
