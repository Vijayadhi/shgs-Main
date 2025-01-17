# **SRI HAYAGIRIVA GROUP of SERVICES (SHGs Main)**

## **Overview**  
The **SRI HAYAGIRIVA GROUP of SERVICES (SHGs Main)** is a comprehensive platform designed to streamline and manage the operations of self-help groups. The system enables administrators to manage members, services, blogs, galleries, and applications, fostering an organized and efficient workflow for SHG operations. It empowers SHGs to serve their communities effectively by offering a user-friendly interface and customizable features.

---

## **Key Features**  
- **Service Management**: Admins can manage multiple services provided to members.  
- **Member Management**: Easy tracking of SHG members and their participation.  
- **Application System**: Allows members to apply for services directly through the platform.  
- **Content Customization**: Create and manage blogs, galleries, and announcements to engage members.  
- **Dashboard**: Centralized admin dashboard for managing all system features.  

---

## **Technologies Used**  
- **Frontend**: HTML, CSS, Bootstrap  
- **Backend**: Python, Django  
- **Database**: SQLite/MySQL  
- **Additional Tools**: Django Admin Panel for easy management  

---

## **Installation Instructions**  

### **Prerequisites**  
1. Python 3.x installed on your system  
2. SQLite (pre-installed with Python) or MySQL for database support  
3. Virtual environment setup (recommended)

### **Steps to Run the Project**  

#### **Backend Setup**  
1. **Clone the Repository**  
   ```bash  
   git clone https://github.com/your-repo/shgs-main.git  
   cd shgs-main  
   ```  

2. **Set Up Virtual Environment**  
   ```bash  
   python -m venv venv  
   source venv/bin/activate   # On Windows: venv\Scripts\activate  
   ```  

3. **Install Dependencies**  
   ```bash  
   pip install -r requirements.txt  
   ```  

4. **Configure the Database**  
   - Modify `settings.py` to configure the database (SQLite for development, MySQL for production).  
   - Run migrations to create the database schema:  
     ```bash  
     python manage.py migrate  
     ```  

5. **Run the Development Server**  
   ```bash  
   python manage.py runserver  
   ```  
   Access the application at `http://127.0.0.1:8000/`.

---

## **Usage**  

### **Admin Portal**  
- Manage members and assign them to specific services.  
- Add and update content, including blogs, galleries, and announcements.  
- Monitor and process service applications submitted by members.  

### **Member Portal**  
- Apply for services and track application status.  
- Access blogs, galleries, and other community updates.

---

## **Future Enhancements**  
- Integration with payment gateways for service fee management.  
- Add multi-language support for a broader user base.  
- Implement notification systems for service updates and announcements.  
- Introduce advanced analytics for tracking service utilization and community impact.  

---

## **Contributing**  
Contributions are welcome! Feel free to fork the repository and submit pull requests.

---

## **License**  
This project is licensed under the MIT License.  

---

## **Contact**  
**Developer**: Vigneshwaran J  
- **Email**: [venerablevignesh@gmail.com](mailto:venerablevignesh@gmail.com)  
- **GitHub**: [https://github.com/Vijayadhi](https://github.com/Vijayadhi)
- **Portfolio**: [https://portfolio-vigneshwaran.netlify.app](https://portfolio-vigneshwaran.netlify.app)
