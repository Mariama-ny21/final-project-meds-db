# Comparative Medicines Database Capstone Project

## 🩺 Introduction

Comparative Medicines Database is a capstone project designed to make medicine information more accessible and transparent for everyone—patients and healthcare professionals. By providing advanced search, comparison tools, and clear data, this web app helps users to quickly find and compare essential information about medicines. The goal is to support informed choices and improve access to essential medicine information in a user-friendly, modern platform.

## 🎓 About This Project

This project is my final capstone for the Fullstack Bootcamp. It demonstrates my ability to design and build a full-stack Django web application with real-world features such as CRUD operations, session-based shopping cart, and Stripe payment integration. While the app uses real medicine names and manufacturers' names, **all features, data, and payments are for educational and demonstration purposes only**. No clinical, commercial, or production use is intended. **Ratings shown in the app are not real or clinically validated—they are randomly generated for demonstration only.**

A Django web application for browsing, searching, and purchasing medicines, with full CRUD (Create, Read, Update, Delete) functionality, a shopping cart, and Stripe Test Mode payment integration. This project is designed for educational and demonstration purposes.


## 🗂️ Database Schema

The following diagram shows the relationships between the main models in the project:

```mermaid
erDiagram
    MEDICINE ||--o{ ORDERITEM : ordered_in
    ORDER ||--o{ ORDERITEM : contains
    User ||--o{ ORDER : places

    MEDICINE {
        int id PK
        
        string medicine_name
        string formula
        string dose & qty
        string manufacturer
        decimal price
        float rating
        string emc_leaflet_url
    }
    ORDER {
        int id PK
        int user_id FK
        string status
        datetime ordered_at
    }
    ORDERITEM {
        int id PK
        int order_id FK
        int medicine_id FK
        int quantity
    }
```

## 🚀 Features

- **Browse Medicines:** View a list of medicines with NHS-based prices, formulas, manufacturers, and demo ratings.
- **Advanced Search & Filter:** Search by name or formula, filter by manufacturer or minimum rating, and sort by name, price, formula, manufacturer, or rating—all in one place for powerful, flexible results.
- **Medicine Details:** Click a medicine name to view detailed information, including a link to the official EMC patient leaflet and a list of similar medicines.
- **Shopping Cart:** Add one or more medicines to a session-based cart. View, update, or remove items before checkout.
- **Stripe Test Payments:** Pay for all items in the cart using Stripe in Test Mode. No real money is charged. See `Stripe_Card_Payments.txt` for test card numbers.
- **CRUD for Medicines:** Admin users can add, edit, and delete medicines via the Django admin interface. All CRUD actions are also available via the web UI for demonstration.
- **User Registration & Login:** Users can register, log in, and log out. (Authentication is required for some actions.)
- **Responsive UI:** Clean, modern Bootstrap interface for desktop and mobile.

## 🛠️ Credentials

- **Admin:** Set your own credentials using Django's `createsuperuser` command.
- **Stripe Test Cards:** See `Stripe_Card_Payments.txt` for valid test card numbers and instructions.

## ⚡ Quick Start

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd final-project-meds-db
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   # Or: source .venv/bin/activate  # On Mac/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   - Create a `.env` file in the project root with your Stripe keys:
     ```env
     STRIPE_SECRET_KEY=sk_test_...
     STRIPE_PUBLISHABLE_KEY=pk_test_...
     ```

5. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

7. **(Optional) Import medicines from CSV:**
   ```bash
   python manage.py import_medicines path/to/your/medicines.csv
   ```

8. **Run the development server:**
   ```bash
   python manage.py runserver
   ```


9. **Access the app:**
   - Main site: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

## 🎨 UX Design Process

The user experience (UX) design process for this project followed a structured, user-centered approach to ensure the application is intuitive, accessible, and visually appealing. The process included:

- **User Research & Requirements:** Identified primary user groups (patients and healthcare professionals) and their needs through research and feedback from peers and mentors.

### 🏭 Features: Rationale and Scope

For this capstone project, the implemented features focus on patient and healthcare professional needs (search, comparison, and purchasing). Manufacturer-specific features were considered but not prioritized, as the project requirements allowed for flexibility and the core user flows were best served by focusing on the main user groups. This approach ensured a more focused, high-quality experience for the primary users while leaving room for future expansion.

- **Wireframes:** Created low-fidelity wireframes for key pages (Home, Medicine List, Medicine Detail, Cart, Checkout, Login/Register) using pen-and-paper sketches and digital tools (e.g., Figma, Balsamiq). These wireframes focused on layout, navigation, and core user flows.

---
#### Home Page

```
+--------------------------------------------------------------------------------+
| [Logo]   [Home]   [Medicines]   [Cart]   [About]   [Contact]   [Login]   [Sign Up] |
+--------------------------------------------------------------------------------+
|   Welcome message / App description                                            |
|
|   Who is this for?                                                             |
|
|   [Browse Medicines]   [About]   [Contact]                                     |
+--------------------------------------------------------------------------------+
```

#### Medicine List Page
----------------------------------------------------
| [Search bars]                   |
|---------------------------------------------------|
| Name      | Formula   | Price | Rating | [Apply]  |
|---------------------------------------------------|
| [Medicine Card]   [Medicine Card]   [Medicine Card]                |
----------------------------------------------------

```
---------------------------------------------------------------------
| [Search bars]                                                     |
|-------------------------------------------------------------------|
| Search Medicine or Formula | Manufacturer | Min. Rating | Sort By |Apply
|-------------------------------------------------------------------|
| [Medicine Card]       [Medicine Card]       [Medicine Card]       |
---------------------------------------------------------------------
```

#### Medicine Detail Page

```
+---------------------------------------------------+
| Medicine Name                                     |
| Formula: ...                                      |
| Manufacturer: ...                                 |
| Price: £...    Rating: ...                        |
| [EMC Leaflet Link]                                |
|---------------------------------------------------|
| Similar Medicines:                                |
| - ...                                             |
|                                                   |
| [Add to Cart]   [Buy Now]                         |
+---------------------------------------------------+
```


#### Cart Page

```
 +--------------------------------------------------------------------------------+
| [Logo]   [Home]   [Medicines]   [Cart]   [About]   [Contact]   [Login]   [Sign Up] |
 +--------------------------------------------------------------------------------+
|                                                   |
| Medicine   Formula   Manufacturer   Price   Quantity   Subtotal   Remove |
|--------------------------------------------------------------------------|
| Benylin   Dextromethorphan   Johnson & Johnson   £6.80   1   £6.80   Remove|
|----------------------------------------------------------------------------|
| Total: £6.80                                                                |
| [Continue Shopping] [Proceed to Checkout]                                   |
+-----------------------------------------------------------------------------+
```

#### Checkout Page

```
| Stripe Payment Form (Test Mode)                   |
|
| [Pay]                                             |  
|
----------------------------------------------------+
```
| [Dashboard Analytics & Charts]                   |
| [Recent Orders]   [Top Medicines]                |
| [User Stats]                                     |

#### Healthcare Dashboard (Restricted Access)

```
---------------------------------------------------+
| [Welcome, username!] (info alert)               |
---------------------------------------------------+
| Medicine Analytics                              |
|  - Total Medicines                              |
|  - Average Price                                |
|  - Lowest Price (name)                          |
|  - Highest Price (name)                         |
|  - Average Rating                               |
---------------------------------------------------+
| [Top 3 Manufacturers Bar Chart]   [Ratings Pie Chart] |
---------------------------------------------------+
| Top Manufacturers List (numbered)               |
---------------------------------------------------+
| [Tip: Use this dashboard to review trends...]   |
---------------------------------------------------+
```
*Note: Access to the Healthcare Dashboard is restricted to authorized users (e.g., admin or healthcare professional staff).* 
---


#### Login/Register Page

```
---------------------------------------------------+
| [Login Form]   or   [Register Form]               |
---------------------------------------------------+
```

---
- **Mockups & Prototypes:** Created high-fidelity mockups to finalize color schemes, typography, spacing, and UI components. Refined designs based on usability and accessibility best practices.
- **Design Rationale:**
  - Chose a clean, modern Bootstrap-based interface for familiarity and responsiveness.
  - Used green and blue as primary colors to convey trust and health.
  - Prioritized clear navigation, large buttons, and readable fonts for accessibility.
  - Included demo-only warnings and clear labels to avoid user confusion.
- **Implementation:**
  - Translated wireframes and mockups into Django templates and Bootstrap components.
  - Used custom CSS for branding and to address specific UI needs (e.g., green headings, responsive tables).
  - Ensured all features (search, filter, cart, checkout) matched the planned user flows.
  - Performed iterative user testing and made adjustments based on feedback (e.g., improving navbar visibility, spacing, and mobile responsiveness).
- **Documentation:**
  - Included screenshots of wireframes and final UI in the project documentation (see `/docs` or below).
  - Provided rationale for key design decisions and described how user needs were addressed.


## 👩‍⚕️ User Stories

### User Story 1
**As a healthcare professional, I want to browse a list of UK medicines so that I can quickly view available medicines and their details.**

**Acceptance Criteria:**
- A search bar is available on the main page
- Users can enter a medicine name or formula
- The search results display all medicines matching the query
- If no results are found, a message is shown to the user

**Tasks:**
- Add a search bar to the main page or medicines list page
- Update the view to filter medicines by name or formula using the search query
- Update the template to display search results and a "no results" message if needed
- Write tests to ensure search works for both name and formula

---
### User Story 2
**As a healthcare professional, I want to click on a medicine from the search results so that I can view all its related details.**

**Acceptance Criteria:**
- Clicking a medicine in the search results opens a detail page
- The detail page displays the medicine’s name, formula, dose, manufacturer, price, and rating
- The detail page is accessible via a unique URL for each medicine

**Tasks:**
- Create a detail view for medicines
- Add a URL pattern for the medicine detail page
- Update the search results template to link each medicine to its detail page
- Design the detail template to show all relevant fields
- Write tests to ensure the detail page displays correct information

---

### User Story 3
As a **patient**, I want to **search and refine my search results by sorting medicines based on price and quality ratings** so that **I can easily compare and choose the best option for my needs.**

**Acceptance Criteria:**
- After searching, users can sort medicines by price (ascending or descending)
- Users can filter medicines by quality rating (e.g., show only 5-star or 4-star medicines)
- Sorting and filtering options are available on the search results page
- The list updates dynamically based on the selected sorting and filtering criteria
- If no medicines match the selected filters, a clear message is displayed

**Tasks:**
- Add sorting controls (e.g., dropdown or buttons) for price (asc/desc) on the search results page
- Add filtering controls for quality ratings (e.g., checkboxes or dropdown)
- Update the view to handle sorting and filtering parameters from the user
- Update the template to display medicines according to the selected sort and filter
- Show a message if no medicines match the current filters
- Write tests to ensure sorting and filtering work as expected

---

### User Story 4

As a **healthcare professional**, I want to **sign up and create an account** so that **I can log in and access additional features of the Medicines Database.**

**Acceptance Criteria:**
- There is a "Sign Up" or "Register" link on the login page and/or main navigation
- The sign up form collects at least a username, email, and password (with password confirmation)
- The system validates that the username and email are unique and that the password meets minimum requirements
- After successful registration, the user is redirected to the login page or logged in automatically
- The user receives a confirmation message that their account waCs created
- If registration fails (e.g., duplicate username, weak password), the user sees a clear error message

**Tasks:** 
- Add a "Sign Up" or "Register" link to the login page and/or navigation
- Create a registration form for username, email, password, and password confirmation
- Validate unique username and email, and enforce password requirements
- Implement registration view and template
- Redirect user to login or log them in after successful registration
- Display confirmation and error messages as appropriate
---

This process ensured that the final implementation closely matched the original design intent, resulting in a user-friendly and accessible web application.

## 📝 Usage Guide

- **Browsing:** Use the homepage or "Medicines" link to browse all medicines. Use the search bar and filters to refine results.
- **Viewing Details:** Click a medicine name to see its details, similar medicines, and options to add to cart or buy now.
- **Shopping Cart:** Add medicines to your cart from the list or detail page. View your cart, remove items, or proceed to checkout.
- **Checkout:** Click "Proceed to Checkout" in the cart to pay for all items using Stripe Test Mode. Use any test card from `Stripe_Card_Payments.txt`.
- **Admin CRUD:** Log in as an admin to add, edit, or delete medicines. You can also demonstrate CRUD via the web UI.
- **User Registration:** Register a new account or log in to access user features.

## 💳 Stripe Test Payments

- No real money is charged. Use the test cards in `Stripe_Card_Payments.txt`.
- Any valid future expiry date and any CVC will work.
- For more test scenarios, see: https://stripe.com/docs/testing#international-cards

## 🧪 Testing

- **Unit Tests:** Run all Django unit tests with:
  ```bash
  python manage.py test
  ```
- **Manual Testing:**
  - Registered users and logged in/out to verify authentication flows.
  - Checked sorting, searching, and filtering features for accuracy.
  - Ensured the UI is responsive on desktop and mobile.
- **Sample Data:**
  - Used a small sample of medicines for initial testing to ensure features worked as expected before scaling up.
  - Manually checked edge cases, such as empty cart, duplicate items, and invalid form submissions.
 
## Lighthouse Reports
Home
<img width="1565" height="836" alt="Home_Lighthouse_Screenshot" src="https://github.com/user-attachments/assets/9ebf77b5-ec7b-4542-9f03-411af6463338" />
Medicines List
<img width="1518" height="835" alt="Medicines List_Lighthouse_Screenshot" src="https://github.com/user-attachments/assets/38e3b7b8-b432-4fd0-86e5-1dcf445360d4" />
Similar Medicines
<img width="1555" height="831" alt="Similar_Meds_Lighthouse_Screenshot" src="https://github.com/user-attachments/assets/17d0ccdb-fbad-411d-82b6-22c56386e0d4" />
Shopping Cart
<img width="1511" height="833" alt="Cart_Lighthouse_Screenshot" src="https://github.com/user-attachments/assets/75a9d29b-83b5-4b98-839e-ccf0478add40" />
Healthcare Dashboard
<img width="1542" height="838" alt="Healthcare_Dashboard_Screenshot" src="https://github.com/user-attachments/assets/0577330e-221c-419b-b3cd-04d0a25cbc1a" />
Login
<img width="1557" height="842" alt="Login_Lighthouse_Screenshot" src="https://github.com/user-attachments/assets/521ef160-a0f2-4c52-b59b-a06e7b254a54" />
Sign Up
<img width="1507" height="807" alt="Sign-UP_Lighthouse_Screenshot" src="https://github.com/user-attachments/assets/fd402194-1759-4b8e-afac-edd7ff866799" />

## 🤖 AI Usage
Artificial Intelligence (AI) was utilized throughout the development of this project to accelerate coding, improve code quality, and enhance documentation. Specifically:

- **Code Generation:** AI-assisted tools (such as GitHub Copilot and ChatGPT) were used to scaffold Django views, forms, templates, and management commands, reducing development time and minimizing boilerplate.
- **Debugging & Refactoring:** AI suggestions helped identify and resolve bugs, optimize logic, and refactor code for clarity and maintainability.
- **Documentation:** AI was used to draft and refine README content, usage instructions, and inline code comments, ensuring clear and comprehensive project documentation.
- **Feature Planning:** AI provided guidance on best practices for implementing features such as session-based carts, Stripe integration, and CRUD operations.

All AI-generated code and documentation were reviewed and tested to ensure correctness and suitability for the project’s goals.

## 🧩 Overcoming Challenges

- **Stripe Integration:** Integrated Stripe in Test Mode to allow safe payment demonstrations without real transactions or business account activation.
- **Data Import:** Developed custom management commands to import and update medicine data from OpenPrescribing and EMC sources, handling data inconsistencies and missing fields.
- **Session Cart:** Implemented a session-based shopping cart to avoid user account dependencies and simplify the demo flow.
- **Demo Ratings:** Used randomly generated ratings for medicines to provide a realistic UI while making it clear these are not clinical scores.
- **User Experience:** Focused on a clean, Bootstrap-based UI for clarity and ease of use, with clear notes about demo/test status throughout the app.

## 🙏 Credits

- **NHS OpenPrescribing:** Medicine price and spending data provided by [OpenPrescribing](https://openprescribing.net/), which sources its data from the NHS Business Services Authority.
- **EMC (Electronic Medicines Compendium):** Patient leaflet links provided via [medicines.org.uk/emc](https://www.medicines.org.uk/emc).
- **Stripe:** Payment processing powered by [Stripe Test Mode](https://stripe.com/docs/testing).
- **Django:** Built with the [Django](https://www.djangoproject.com/) web framework.
- **Bootstrap:** UI styled with [Bootstrap](https://getbootstrap.com/).
- **Other Libraries:** See `requirements.txt` for a full list of Python dependencies.

## 📝 Notes

- This app is for educational, demonstration, and capstone project purposes only.
- All medicine data, prices, and company names are for demo/learning use and do not represent clinical or commercial advice.
- Ratings are randomly generated and are not real or clinically validated.
- Stripe is in Test Mode—no real payments are processed, and no business account is required.
- The app can be safely deployed or shared for educational review, but is **not intended for real-world medical, pharmaceutical, or e-commerce use**.

## 📄 License

MIT License

