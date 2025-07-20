# Bank Credit Score Loan Calculator

A Django-based credit approval system that calculates credit scores and loan eligibility based on customer data and loan history.

## 🚀 Live Demo
**Live Application:** [https://bank-credit-score-loan-calculator.vercel.app](https://bank-credit-score-loan-calculator.vercel.app)

## 📋 Features

- **Customer Management**: Store and manage customer information
- **Loan Tracking**: Track loan applications and repayment history
- **Credit Score Calculation**: Automated credit scoring algorithm
- **Loan Eligibility**: Determine loan approval based on credit scores
- **Data Import**: Excel file upload for bulk data ingestion
- **REST API**: Full API endpoints for integration
- **Modern UI**: Clean, responsive web interface

## 🛠️ Technology Stack

- **Backend**: Django 4.2.7
- **Database**: SQLite (development) / PostgreSQL (production)
- **API**: Django REST Framework
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Vercel
- **Static Files**: WhiteNoise

## 📊 Data Models

### Customer
- Customer ID, Name, Age, Phone
- Monthly Salary, Approved Limit
- Current Debt, Credit Score

### Loan
- Loan ID, Amount, Tenure
- Interest Rate, Monthly Repayment
- EMIs Paid on Time, Start/End Dates

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/ved-raut/bank-credit-score-loan-calculator.git
   cd bank-credit-score-loan-calculator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Start development server**
   ```bash
   python manage.py runserver
   ```

5. **Access the application**
   - Main Dashboard: http://localhost:8000/
   - Admin Panel: http://localhost:8000/admin/

### Data Import

1. **Place Excel files in project root:**
   - `customer_data.xlsx` - Customer information
   - `loan_data.xlsx` - Loan history data

2. **Run data ingestion:**
   ```bash
   python manage.py ingest_data
   ```

## 🔧 API Endpoints

- `GET /api/customers/` - List all customers
- `GET /api/customers/{id}/` - Get customer details
- `GET /api/loans/` - List all loans
- `GET /api/loans/{id}/` - Get loan details
- `POST /api/calculate-credit-score/` - Calculate credit score

## 📈 Credit Score Algorithm

The system calculates credit scores based on:
- **Payment History** (40%): EMIs paid on time
- **Credit Utilization** (30%): Current debt vs approved limit
- **Income Stability** (20%): Monthly salary consistency
- **Loan History** (10%): Previous loan performance

## 🎯 Usage

1. **Import Data**: Upload customer and loan data via Excel files
2. **View Dashboard**: See overview of customers and loans
3. **Calculate Scores**: Generate credit scores for customers
4. **Check Eligibility**: Determine loan approval status
5. **API Integration**: Use REST endpoints for external systems

## 🔒 Security Features

- CSRF protection enabled
- Secure headers configured
- Input validation and sanitization
- SQL injection prevention

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

**Ved Raut**
- GitHub: [@ved-raut](https://github.com/ved-raut)
- Project: Bank Credit Score Loan Calculator

---

**Last Updated:** July 20, 2024 - Deployment Fix Applied
