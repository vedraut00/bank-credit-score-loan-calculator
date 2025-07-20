# 🏦 Bank Credit Score and Loan Calculator

A comprehensive full-stack web application for credit analysis and loan approval management. Built with Django, featuring real-time credit scoring, Excel data import, and an intuitive user interface. **Fully deployed and accessible worldwide.**

## 🌟 **Live Demo**

**🚀 [View Live Application](https://bank-credit-score-loan-calculator.vercel.app)**

## ✨ **Features**

### **📊 Dashboard & Analytics**
- Real-time system statistics
- Credit score distribution charts
- Recent activity tracking
- Quick action buttons

### **👥 Customer Management**
- Add, edit, and delete customers
- Bulk import via Excel files
- Customer search and pagination
- Detailed customer profiles
- Credit score calculation

### **💰 Loan Management**
- Create and manage loans
- Loan approval status checking
- Payment tracking and analytics
- Risk assessment algorithms

### **📁 Excel Data Import**
- Drag & drop file upload
- Support for customer and loan data
- Automatic data validation
- Error handling and feedback
- Sample templates provided

### **🗑️ Data Management**
- Individual record deletion
- Bulk data cleanup
- Confirmation dialogs
- Safe deletion with cascade

## 🛠️ **Technologies Used**

### **Backend**
- **Django 4.2.7**: Web framework
- **Django REST Framework**: API endpoints
- **SQLite/PostgreSQL**: Database
- **Pandas**: Excel file processing
- **OpenPyXL**: Excel file handling

### **Frontend**
- **Bootstrap 5**: Responsive UI framework
- **Font Awesome**: Icons
- **Chart.js**: Data visualization
- **jQuery**: JavaScript interactions
- **AJAX**: Real-time updates

### **Deployment**
- **Vercel**: Hosting platform
- **WhiteNoise**: Static file serving
- **Gunicorn**: WSGI server
- **Environment Variables**: Configuration management

## 🚀 **Quick Start**

### **Local Development**

1. **Clone the repository**
   ```bash
   git clone https://github.com/vedraut00/bank-credit-score-loan-calculator.git
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

4. **Start the development server**
   ```bash
   python manage.py runserver
   ```

5. **Access the application**
   ```
   http://localhost:8000/loans/
   ```

### **Environment Variables**

Create a `.env` file in the root directory:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 📁 **Project Structure**

```
bank-credit-score-loan-calculator/
├── credit_system/          # Django project settings
├── loans/                  # Main application
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── urls.py            # URL routing
│   ├── utils.py           # Credit scoring algorithms
│   ├── serializers.py     # API serializers
│   └── templates/         # HTML templates
├── static/                # Static files (CSS, JS)
├── requirements.txt       # Python dependencies
├── vercel.json           # Vercel deployment config
└── README.md             # This file
```

## 🎯 **Key Features Explained**

### **Credit Score Calculation**
The system calculates credit scores based on:
- Payment history
- Debt-to-income ratio
- Credit utilization
- Loan history
- Age and income factors

### **Loan Approval Algorithm**
Loans are approved based on:
- Credit score threshold
- Debt-to-income ratio limits
- Loan amount vs. approved limit
- Payment history analysis

### **Excel Import System**
- Supports both customer and loan data
- Automatic column detection
- Data validation and error handling
- Progress feedback and success messages

## 📊 **Screenshots**

### **Dashboard**
![Dashboard](screenshots/dashboard.png)

### **Customer Management**
![Customer List](screenshots/customers.png)

### **Excel Upload**
![Excel Upload](screenshots/excel-upload.png)

### **Loan Analysis**
![Loan Detail](screenshots/loan-detail.png)

## 🔧 **API Endpoints**

### **Credit Score API**
```
POST /loans/api/credit-score/{customer_id}/
```

### **Loan Approval API**
```
POST /loans/api/loan-approval/{loan_id}/
```

### **Customer Data API**
```
GET /loans/api/customers/
```

### **Loan Data API**
```
GET /loans/api/loans/
```

## 🚀 **Deployment**

This application is deployed on **Vercel** for easy access and professional presentation.

### **Deployment Features**
- ✅ **HTTPS**: Secure connections
- ✅ **Global CDN**: Fast worldwide access
- ✅ **Auto-scaling**: Handles traffic spikes
- ✅ **Custom Domain**: Professional URLs
- ✅ **Environment Variables**: Secure configuration

## 📈 **Resume Impact**

This project demonstrates:
- **Full-Stack Development**: Django backend + Bootstrap frontend
- **Data Processing**: Excel file handling and analysis
- **Real-time Features**: AJAX updates and calculations
- **Production Deployment**: Live application on Vercel
- **User Experience**: Intuitive interface and workflows
- **Data Management**: CRUD operations and bulk operations

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 👨‍💻 **Author**

**Ved Raut**
- GitHub: [@vedraut00](https://github.com/vedraut00)
- LinkedIn: [Ved Raut](https://linkedin.com/in/vedraut00)
- Portfolio: [Ved Raut Portfolio](https://vedraut00.github.io)

## 📝 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- Django community for the excellent framework
- Bootstrap team for the responsive UI components
- Vercel for the seamless deployment platform
- All contributors and testers

---

**⭐ Star this repository if you found it helpful!**

**🔗 [Live Demo](https://bank-credit-score-loan-calculator.vercel.app) | [GitHub Repository](https://github.com/vedraut00/bank-credit-score-loan-calculator)**
