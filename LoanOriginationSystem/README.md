# Loan Origination System

A full-stack web application for managing the loan origination process, from application to funds disbursement.

## Features

- Role-based access control (Sales, Processor, Underwriter, Closer, Manager)
- Milestone tracking (PreApplication → Submitted → IRR → FRR → Closing Docs Generated → Funds Disbursed)
- Document upload and management
- Compliance checking
- Loan pricing and closing fees calculation
- Consent document management
- Admin dashboard for loan management

## Tech Stack

### Frontend
- Angular 13+
- TailwindCSS (with custom red and white theme)
- Responsive design for mobile and desktop
- Form validation and error handling

### Backend
- Python Flask RESTful API
- MongoDB Atlas for database
- Document storage and processing
- Swagger API documentation

## Project Structure

### Frontend
- Angular components for each step of the loan process
- Services for API communication
- Models for type safety
- TailwindCSS for styling

### Backend
- Flask RESTful API with modular structure
- MongoDB Atlas integration
- Document upload and processing
- User management and role-based access control

## Setup and Installation

### Prerequisites
- Node.js and npm
- Angular CLI
- Python 3.8+
- MongoDB Atlas account

### Frontend Setup
1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   