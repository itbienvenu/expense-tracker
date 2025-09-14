<h1>Expense Tracker Database Model</h1>
<h2>Overview</h2>
This database model represents a personal finance management system that allows users to track transactions, categorize them, and manage their financial data. The system supports income and expense tracking with flexible categorization.

<h2>Entities and Relationships</h2>
<h2>1. Users Table (users)</h2>
Stores user account information and authentication details.

<b>Columns:</b>
<ul>
<li><b>id</b> (UUID, Primary Key): Unique identifier for the user (auto-generated)

<li><b>username</b> (VARCHAR, Unique): User's login username

<li><b>email</b> (VARCHAR, Unique): User's email address

<li><b>hashed_password</b> (VARCHAR): Securely stored password hash

<li><b>created_at</b> (TIMESTAMP): Account creation timestamp (auto-generated)

<b>Relationships:</b>

<li>One-to-Many: One user can have many transactions

<li>One-to-Many: One user can have many categories
</ul>
2. Categories Table (categories)
Stores user-defined transaction categories.

Columns:

id (UUID, Primary Key): Unique identifier for the category (auto-generated)

name (VARCHAR): Category name (e.g., "Groceries", "Salary")

user_id (UUID, Foreign Key): Reference to the user who owns this category

Relationships:

Many-to-One: Many categories can belong to one user (user_id → users.id)

Many-to-Many: Many categories can be associated with many transactions (through transaction_category)

3. Transactions Table (transactions)
Stores financial transactions with amount, date, and categorization.

Columns:

id (UUID, Primary Key): Unique identifier for the transaction (auto-generated)

title (VARCHAR): Transaction description or title

amount (FLOAT): Transaction amount (positive = income, negative = expense)

date (DATE): Transaction date

user_id (UUID, Foreign Key): Reference to the user who owns this transaction

Relationships:

Many-to-One: Many transactions can belong to one user (user_id → users.id)

Many-to-Many: Many transactions can be associated with many categories (through transaction_category)

4. Transaction-Category Association Table (transaction_category)
Junction table for the many-to-many relationship between transactions and categories.

Columns:

transaction_id (UUID, Foreign Key): Reference to transaction

category_id (UUID, Foreign Key): Reference to category

Composite Primary Key: (transaction_id, category_id)

Key Features
Flexible Categorization
Many-to-Many Relationship: Transactions can have multiple categories

User-Specific Categories: Each user maintains their own set of categories

Cascade Deletion: User deletion automatically removes their transactions and categories

Financial Tracking