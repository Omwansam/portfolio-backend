#!/usr/bin/env python3
"""
Education Seed File for Omwansa Portfolio Database
This script will populate the education table with comprehensive education data including:
- Formal Education (Universities, Colleges)
- Certifications (Professional Certificates)
- Online Courses and Bootcamps
"""

import os
import sys
from datetime import date

# Make imports robust whether run as a module or a script
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

try:
    # When executed as a script (python server/seed_education.py)
    from server.app import app
    from server.extensions import db
    from server.models import Education
except ImportError:
    # When executed as a module (python -m server.seed_education)
    from .app import app
    from .extensions import db
    from .models import Education

def clear_education_data():
    """Clear all existing education data"""
    print("🗑️  Clearing existing education data...")
    
    try:
        # Delete all education records
        Education.query.delete()
        db.session.commit()
        print("   ✅ All education records deleted")
    except Exception as e:
        print(f"   ⚠️  Error clearing education data: {str(e)}")
        db.session.rollback()

def create_education_data():
    """Create comprehensive education records"""
    print("🎓 Creating comprehensive education data...")

    education_data = [
        # ===== FORMAL EDUCATION =====
        {
            "institution": "KCA University",
            "degree": "Bachelor of Science in Information Security and Forensics",
            "field_of_study": "Information Security and Forensics",
            "location": "Nairobi, Kenya",
            "start_date": date(2018, 9, 1),
            "end_date": date(2022, 6, 30),
            "current": False,
            "gpa": 3.7,
            "description": (
                "Comprehensive program covering cybersecurity fundamentals, digital forensics, "
                "network security, cryptography, and ethical hacking. "
                "Key coursework: Network Security, Digital Forensics, Cryptography, "
                "Ethical Hacking, Risk Management, Incident Response, "
                "Computer Law and Ethics, Database Security, Operating Systems Security, "
                "Web Application Security, Mobile Security, Cloud Security. "
                "Technologies: Wireshark, Nmap, Metasploit, Burp Suite, OWASP ZAP, "
                "EnCase, FTK, Volatility, Python, C++, Java, SQL, Linux, Windows Server. "
                "Skills: Penetration Testing, Vulnerability Assessment, Digital Evidence Analysis, "
                "Security Policy Development, Compliance Auditing, Threat Modeling."
            ),
        },
        {
            "institution": "Moringa School",
            "degree": "Certificate in Software Engineering",
            "field_of_study": "Software Engineering",
            "location": "Nairobi, Kenya",
            "start_date": date(2021, 1, 1),
            "end_date": date(2021, 6, 30),
            "current": False,
            "gpa": 0.0,
            "description": (
                "Intensive software engineering bootcamp focusing on full-stack development. "
                "Key coursework: Frontend Development, Backend Development, Database Design, "
                "API Development, Testing, DevOps, Agile Methodologies, Project Management. "
                "Technologies: JavaScript, React, Node.js, Express.js, Python, Django, "
                "PostgreSQL, MongoDB, Git, GitHub, Docker, Heroku, AWS. "
                "Skills: Full-Stack Development, RESTful API Design, Database Management, "
                "Version Control, Agile Development, Code Review, Testing, Deployment. "
                "Final project: Built a complete e-commerce platform with payment integration."
            ),
        },
        {
            "institution": "Institute of Software Technologies",
            "degree": "Diploma in Software Development",
            "field_of_study": "Software Development",
            "location": "Nairobi, Kenya",
            "start_date": date(2019, 1, 1),
            "end_date": date(2020, 12, 31),
            "current": False,
            "gpa": 0.0,
            "description": (
                "Comprehensive software development program covering programming fundamentals, "
                "web development, mobile app development, and software engineering principles. "
                "Key coursework: Programming Fundamentals, Object-Oriented Programming, "
                "Data Structures & Algorithms, Web Development, Mobile Development, "
                "Database Design, Software Testing, Project Management, System Analysis. "
                "Technologies: Java, C#, .NET Framework, ASP.NET, HTML/CSS, JavaScript, "
                "SQL Server, MySQL, Visual Studio, Android Studio, Xamarin. "
                "Skills: Software Development Lifecycle, Code Optimization, Debugging, "
                "Database Administration, UI/UX Design, Cross-Platform Development."
            ),
        },

        # ===== PROFESSIONAL CERTIFICATIONS =====
        {
            "institution": "Cisco Systems",
            "degree": "CCNA (Cisco Certified Network Associate)",
            "field_of_study": "Network Administration",
            "location": "Online",
            "start_date": date(2020, 3, 1),
            "end_date": date(2020, 6, 30),
            "current": False,
            "gpa": 0.0,
            "description": (
                "Professional certification in network fundamentals, network access, "
                "IP connectivity, IP services, security fundamentals, and automation. "
                "Key topics: Network Fundamentals, Network Access, IP Connectivity, "
                "IP Services, Security Fundamentals, Automation and Programmability. "
                "Technologies: Cisco IOS, Cisco Packet Tracer, Wireshark, "
                "OSPF, EIGRP, BGP, VLANs, STP, EtherChannel, ACLs, NAT, DHCP, DNS. "
                "Skills: Network Design, Router Configuration, Switch Configuration, "
                "Troubleshooting, Network Security, Automation Scripting, "
                "Network Monitoring, Performance Optimization."
            ),
        },
        {
            "institution": "Microsoft",
            "degree": "Microsoft Certified: Azure Fundamentals",
            "field_of_study": "Cloud Computing",
            "location": "Online",
            "start_date": date(2021, 8, 1),
            "end_date": date(2021, 10, 31),
            "current": False,
            "gpa": 0.0,
            "description": (
                "Fundamental knowledge of cloud services and how those services are provided with Microsoft Azure. "
                "Key topics: Cloud concepts, Azure services, Azure workloads, security and privacy, "
                "Azure pricing and support, governance, compliance, and service-level agreements. "
                "Technologies: Azure Portal, Azure CLI, PowerShell, Azure Resource Manager, "
                "Azure Active Directory, Azure Storage, Azure Virtual Machines, Azure App Service, "
                "Azure Functions, Azure SQL Database, Azure Cosmos DB. "
                "Skills: Cloud Architecture, Infrastructure as Code, Identity Management, "
                "Data Storage Solutions, Serverless Computing, Monitoring and Analytics, "
                "Cost Management, Security Best Practices."
            ),
        },
        {
            "institution": "AWS (Amazon Web Services)",
            "degree": "AWS Certified Cloud Practitioner",
            "field_of_study": "Cloud Computing",
            "location": "Online",
            "start_date": date(2022, 1, 1),
            "end_date": date(2022, 3, 31),
            "current": False,
            "gpa": 0.0,
            "description": (
                "Foundational understanding of AWS Cloud concepts, services, and terminology. "
                "Key areas: AWS Cloud value proposition, AWS services and use cases, "
                "AWS Cloud security and compliance, billing and pricing models, "
                "cloud economics, and support plans. "
                "Technologies: AWS Console, AWS CLI, EC2, S3, RDS, Lambda, "
                "CloudFormation, IAM, VPC, CloudWatch, Route 53, SNS, SQS. "
                "Skills: Cloud Strategy, Service Selection, Cost Optimization, "
                "Security Implementation, Compliance Management, "
                "Performance Monitoring, Disaster Recovery Planning."
            ),
        },
        {
            "institution": "Google",
            "degree": "Google Analytics Certified",
            "field_of_study": "Digital Analytics",
            "location": "Online",
            "start_date": date(2021, 5, 1),
            "end_date": date(2021, 7, 31),
            "current": False,
            "gpa": 0.0,
            "description": (
                "Certification in Google Analytics covering data collection, processing, "
                "and configuration, advanced analysis tools and techniques, "
                "attribution modeling, and conversion optimization. "
                "Key topics: Data Collection, Processing and Configuration, "
                "Advanced Analysis Tools, Attribution Modeling, Conversion Optimization, "
                "E-commerce Tracking, Custom Dimensions and Metrics. "
                "Technologies: Google Analytics 4, Google Tag Manager, Google Data Studio, "
                "Google Ads, Google Search Console, BigQuery, JavaScript, HTML. "
                "Skills: Web Analytics, Data Analysis, Conversion Tracking, "
                "A/B Testing, ROI Measurement, Performance Optimization, "
                "Digital Marketing Analytics, Reporting and Visualization."
            ),
        },

        # ===== ONLINE COURSES AND BOOTCAMPS =====
        {
            "institution": "FreeCodeCamp",
            "degree": "Full Stack Web Development Certification",
            "field_of_study": "Web Development",
            "location": "Online",
            "start_date": date(2020, 1, 1),
            "end_date": date(2020, 12, 31),
            "current": False,
            "gpa": 0.0,
            "description": (
                "Comprehensive free coding bootcamp covering front-end and back-end technologies. "
                "Key coursework: Responsive Web Design, JavaScript Algorithms, Front End Libraries, "
                "Data Visualization, APIs and Microservices, Information Security, "
                "Quality Assurance, Scientific Computing with Python. "
                "Technologies: HTML5, CSS3, JavaScript ES6+, React, Redux, Node.js, "
                "Express.js, MongoDB, PostgreSQL, D3.js, Python, Flask, Django, "
                "Git, GitHub, Heroku, Netlify, Jest, Mocha, Chai. "
                "Skills: Full-Stack Development, API Development, Database Design, "
                "Responsive Design, Data Visualization, Testing, Version Control, "
                "Deployment, Problem Solving, Algorithm Design."
            ),
        },
        {
            "institution": "Coursera - University of Michigan",
            "degree": "Python for Everybody Specialization",
            "field_of_study": "Python Programming",
            "location": "Online",
            "start_date": date(2019, 6, 1),
            "end_date": date(2019, 12, 31),
            "current": False,
            "gpa": 0.0,
            "description": (
                "Five-course specialization covering Python programming fundamentals, "
                "data structures, web scraping, databases, and data visualization. "
                "Key coursework: Programming for Everybody, Python Data Structures, "
                "Using Python to Access Web Data, Using Databases with Python, "
                "Capstone: Retrieving, Processing, and Visualizing Data with Python. "
                "Technologies: Python 3, BeautifulSoup, Requests, SQLite, MySQL, "
                "Matplotlib, Pandas, NumPy, Jupyter Notebooks, XML, JSON, APIs. "
                "Skills: Python Programming, Data Structures, Web Scraping, "
                "Database Management, Data Analysis, Data Visualization, "
                "API Integration, Problem Solving, Algorithm Implementation. "
                "Capstone project: Built a web scraper and data analysis tool."
            ),
        },
        {
            "institution": "Udemy",
            "degree": "Complete React Developer Course",
            "field_of_study": "React Development",
            "location": "Online",
            "start_date": date(2021, 3, 1),
            "end_date": date(2021, 5, 31),
            "current": False,
            "gpa": 0.0,
            "description": (
                "Comprehensive React development course covering modern React features, "
                "hooks, context API, Redux, testing with Jest, and deployment. "
                "Key coursework: React Fundamentals, Hooks, Context API, Redux, "
                "React Router, Testing, Performance Optimization, Deployment. "
                "Technologies: React 17+, JavaScript ES6+, Redux, Redux Toolkit, "
                "React Router, Jest, Enzyme, React Testing Library, Firebase, "
                "Stripe API, Netlify, Heroku, Git, GitHub. "
                "Skills: React Development, State Management, Component Design, "
                "Testing, Performance Optimization, API Integration, "
                "Deployment, Modern JavaScript, UI/UX Implementation. "
                "Built multiple projects including a full e-commerce application."
            ),
        },
        {
            "institution": "Pluralsight",
            "degree": "Node.js Development Path",
            "field_of_study": "Backend Development",
            "location": "Online",
            "start_date": date(2021, 7, 1),
            "end_date": date(2021, 9, 30),
            "current": False,
            "gpa": 0.0,
            "description": (
                "Advanced Node.js development covering Express.js, RESTful APIs, "
                "authentication, database integration, testing, and deployment. "
                "Key coursework: Node.js Fundamentals, Express.js, RESTful API Design, "
                "Authentication & Authorization, Database Integration, Testing, "
                "Performance Optimization, Security, Deployment. "
                "Technologies: Node.js, Express.js, MongoDB, Mongoose, PostgreSQL, "
                "JWT, Passport.js, Jest, Supertest, Docker, AWS, Heroku, "
                "Redis, Socket.io, GraphQL, TypeScript. "
                "Skills: Backend Development, API Design, Database Management, "
                "Authentication, Testing, Performance Optimization, "
                "Security Implementation, DevOps, Microservices Architecture. "
                "Focus on production-ready applications and best practices."
            ),
        },
        {
            "institution": "edX - MIT",
            "degree": "Introduction to Computer Science and Programming",
            "field_of_study": "Computer Science",
            "location": "Online",
            "start_date": date(2018, 9, 1),
            "end_date": date(2019, 1, 31),
            "current": False,
            "gpa": 0.0,
            "description": (
                "MIT's introductory computer science course covering computational thinking, "
                "programming concepts, algorithms, and data structures using Python. "
                "Key coursework: Computational Thinking, Programming Concepts, "
                "Algorithms and Data Structures, Object-Oriented Programming, "
                "Recursion, Testing and Debugging, Complexity Analysis. "
                "Technologies: Python 3, IDLE, Jupyter Notebooks, Git, "
                "NumPy, Matplotlib, Unit Testing Frameworks. "
                "Skills: Computational Thinking, Algorithm Design, Data Structures, "
                "Problem Solving, Debugging, Code Optimization, "
                "Mathematical Modeling, Software Engineering Principles. "
                "Emphasis on problem-solving and algorithmic thinking."
            ),
        },
        {
            "institution": "Codecademy",
            "degree": "Data Science Career Path",
            "field_of_study": "Data Science",
            "location": "Online",
            "start_date": date(2022, 4, 1),
            "end_date": date(2022, 8, 31),
            "current": False,
            "gpa": 0.0,
            "description": (
                "Comprehensive data science program covering Python, SQL, statistics, "
                "machine learning, and data visualization. "
                "Key coursework: Python for Data Science, SQL Fundamentals, "
                "Statistics and Probability, Machine Learning, Data Visualization, "
                "Data Cleaning and Preprocessing, Feature Engineering, Model Evaluation. "
                "Technologies: Python, Pandas, NumPy, Matplotlib, Seaborn, "
                "Scikit-learn, Jupyter Notebooks, SQL, PostgreSQL, "
                "Tableau, Power BI, Git, GitHub. "
                "Skills: Data Analysis, Statistical Modeling, Machine Learning, "
                "Data Visualization, Database Querying, Predictive Analytics, "
                "Data Storytelling, Statistical Inference, A/B Testing. "
                "Projects: Data analysis, predictive modeling, and data storytelling."
            ),
        },
        {
            "institution": "LinkedIn Learning",
            "degree": "Cybersecurity Fundamentals",
            "field_of_study": "Cybersecurity",
            "location": "Online",
            "start_date": date(2020, 9, 1),
            "end_date": date(2020, 11, 30),
            "current": False,
            "gpa": 0.0,
            "description": (
                "Foundational cybersecurity course covering threat landscape, "
                "security frameworks, risk management, and incident response. "
                "Key topics: Threat Landscape Analysis, Security Frameworks (NIST, ISO), "
                "Risk Management, Incident Response, Network Security, "
                "Application Security, Security Operations, Compliance. "
                "Technologies: SIEM Tools, Firewalls, IDS/IPS, Vulnerability Scanners, "
                "Penetration Testing Tools, Security Monitoring Tools, "
                "Encryption Tools, Identity Management Systems. "
                "Skills: Threat Assessment, Risk Analysis, Security Policy Development, "
                "Incident Response, Vulnerability Management, Security Monitoring, "
                "Compliance Management, Security Awareness Training."
            ),
        },
        {
            "institution": "Khan Academy",
            "degree": "Computer Programming",
            "field_of_study": "Programming Fundamentals",
            "location": "Online",
            "start_date": date(2017, 1, 1),
            "end_date": date(2017, 12, 31),
            "current": False,
            "gpa": 0.0,
            "description": (
                "Introduction to computer programming using JavaScript. "
                "Key coursework: Programming Basics, Variables and Functions, "
                "Control Flow, Data Structures, Algorithms, Object-Oriented Programming, "
                "Event Handling, Animation, Game Development. "
                "Technologies: JavaScript, HTML5 Canvas, CSS, Processing.js, "
                "Web APIs, DOM Manipulation, Event Listeners. "
                "Skills: Programming Logic, Problem Solving, Algorithm Design, "
                "Creative Coding, Interactive Design, Game Development, "
                "User Interface Design, Animation Programming. "
                "Built interactive web applications and games."
            ),
        },
    ]

    created = []
    for edu_data in education_data:
        education = Education(**edu_data)
        db.session.add(education)
        created.append(education)
        print(f"   ✅ Added: {edu_data['degree']} from {edu_data['institution']}")

    db.session.commit()
    print(f"\n🎓 Education seeding completed!")
    print(f"   📊 Total education records: {len(created)} records added")
    print(f"   📚 Categories covered:")
    print(f"      • Formal Education: 3 records")
    print(f"      • Professional Certifications: 4 records") 
    print(f"      • Online Courses & Bootcamps: 8 records")
    
    return created

def main():
    """Main function to run the education seed script"""
    print("🌱 Starting Education Database Seeding...")
    print("=" * 60)
    
    with app.app_context():
        try:
            # Clear existing education data first
            clear_education_data()
            
            # Create new education data
            create_education_data()
            
            print("=" * 60)
            print("✅ Education seeding completed successfully!")
            print("🎯 All education data has been populated in the database")
            print("=" * 60)
            
        except Exception as e:
            print(f"❌ Error during education seeding: {str(e)}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    main()
