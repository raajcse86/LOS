import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { UserService } from '../../services/user.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  loginForm: FormGroup;
  errorMessage = '';
  isSubmitting = false;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private userService: UserService,
    private router: Router
  ) {
    this.loginForm = this.fb.group({
      username: ['', [Validators.required]],
      password: ['', [Validators.required]]
    });
  }

  ngOnInit(): void {
    // Check if already logged in
    if (localStorage.getItem('currentUser')) {
      this.router.navigate(['/admin-panel']);
    }
  }

  onSubmit(): void {
    if (this.loginForm.invalid) {
      return;
    }

    this.isSubmitting = true;
    this.errorMessage = '';

    const { username, password } = this.loginForm.value;

    this.authService.login(username, password).subscribe(
      (response) => {
        this.isSubmitting = false;
        
        // Store user info
        localStorage.setItem('currentUser', JSON.stringify(response));
        
        // Set role
        this.userService.setCurrentRole(response.role);
        
        // Navigate to dashboard page
        this.router.navigate(['/loans']);
      },
      (error) => {
        this.isSubmitting = false;
        this.errorMessage = 'Invalid username or password. Please try again.';
        console.error('Login error', error);
      }
    );
  }
}