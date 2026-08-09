Library Management System
A comprehensive, enterprise-grade software application designed to digitize and automate the entire lifecycle of library operations. Built with high performance and accessibility in mind, this system streamlines cataloging, member engagement, circulation workflows, fine collection, and inventory analytics for academic, public, and private institutions.

📸 Interface Preview

✨ Key Features

📚 Catalog & Inventory Management
Rich Metadata Support: Index physical books, eBooks, research journals, and multimedia with full support for ISBN-10, ISBN-13, Dewey Decimal System, title, author, and publisher data.
Batch Operations: Bulk import and export catalog items using CSV, JSON, or Excel templates.
Real-time Inventory Tracking: Track individual item conditions, physical shelf locations, and live availability statuses (Available, Issued, On Hold, Under Maintenance).

👥 Member & User Management
Role-Based Access Control (RBAC): Granular authorization matrix supporting multi-tier administration (Super Admin, Librarian, Staff, Member).
Profile & Borrowing History: Maintain comprehensive records including contact information, active borrowing quotas, historical checkout logs, and account standing.
Self-Service Portal: Allow members to manage reservations, view due dates, renew active loans, and request new titles.

🔄 Circulation & Automated Workflow
Express Checkout & Return: Fast-track desk issuance and returns using barcode, QR code, or manual ID entry.
Hold & Reservation Queue: Automated queue management when checking in requested or popular books, notifying the next queued member instantly.
Automated Fine Engine: Real-time late fee computation based on configurable daily fine rates, grace periods, and maximum cap limits.

🔍 Advanced Search & OPAC
Multi-Filter Querying: Instantly search across thousands of records using fuzzy search parameters (Title, Author, Genre, Publication Year, or Tag).
Live Catalog Status: Public Access Catalog interface showing immediate availability without requiring user authentication.

📊 Analytics & Reporting
Visual Dashboards: Track active loans, overdue returns, peak borrowing hours, and monthly fine collections.
Exportable Audit Logs: Generate system compliance logs and financial summary reports in PDF or CSV format.

🛠️ Tech Stack & Architecture
Frontend
* HTML5 & CSS3:Structured layout with custom styling (`static/css/style.css`).
* Tailwind CSS:Modern utility-first CSS framework for responsive UI components and dark-mode styling.
* Jinja2 Templating:Dynamic server-side rendering for template views (`dashboard.html`, `home.html`, `login.html`).
Backend
* Python (Flask):Micro-web framework handling routing, session management, and request processing (`app.py`).
Database & Data Persistence
JSON File Storage:Lightweight file-based persistence for storing structured entities (`data/books.json`, `data/members.json`, `data/transactions.json`).
Version Control
Git & GitHub:Source code management and repository hosting.

📁 Repository Structure
Plaintext
library-management-system/
├── data/
│   ├── books.json          # Stores catalog book records
│   ├── members.json        # Stores registered member details
│   └── transactions.json   # Logs borrowing and returning transactions
├── static/
│   └── css/
│       └── style.css       # Custom stylesheet rules
├── templates/
│   ├── dashboard.html      # Main administrative dashboard view
│   ├── home.html           # Landing / home page template
│   └── login.html          # Authentication / login page template
├── app.py                  # Main Flask / Python backend entry point
└── README.md               # Project documentation
