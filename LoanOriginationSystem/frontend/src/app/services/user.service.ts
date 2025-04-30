import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';

export interface User {
  _id?: string;
  username: string;
  firstName: string;
  lastName: string;
  email: string;
  role: string;
  createdAt?: string;
  updatedAt?: string;
}

export enum UserRole {
  SALES = 'Sales',
  PROCESSOR = 'Processor',
  UNDERWRITER = 'Underwriter',
  CLOSER = 'Closer',
  MANAGER = 'Manager'
}

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private apiUrl = 'http://localhost:8000/api/users';

  // Observable for current role
  private currentRoleSubject = new BehaviorSubject<string>('Sales');
  public currentRole$: Observable<string> = this.currentRoleSubject.asObservable();

  constructor(private http: HttpClient) { }

  setCurrentRole(role: string): void {
    this.currentRoleSubject.next(role);
  }

  getCurrentRole(): string {
    return this.currentRoleSubject.value;
  }

  getUsers(): Observable<User[]> {
    return this.http.get<User[]>(this.apiUrl)
      .pipe(
        catchError(this.handleError<User[]>('getUsers', []))
      );
  }

  getUser(id: string): Observable<User> {
    const url = `${this.apiUrl}/${id}`;
    return this.http.get<User>(url)
      .pipe(
        catchError(this.handleError<User>(`getUser id=${id}`))
      );
  }

  getUsersByRole(role: string): Observable<User[]> {
    const url = `${this.apiUrl}/role/${role}`;
    return this.http.get<User[]>(url)
      .pipe(
        catchError(this.handleError<User[]>(`getUsersByRole role=${role}`, []))
      );
  }

  createUser(user: User): Observable<User> {
    return this.http.post<User>(this.apiUrl, user)
      .pipe(
        tap((newUser: User) => console.log(`Created user w/ id=${newUser._id}`)),
        catchError(this.handleError<User>('createUser'))
      );
  }

  updateUser(id: string, user: User): Observable<any> {
    const url = `${this.apiUrl}/${id}`;
    return this.http.put(url, user)
      .pipe(
        catchError(this.handleError<any>('updateUser'))
      );
  }

  hasPermission(requiredRole: string): boolean {
    const currentRole = this.getCurrentRole();
    
    // Map roles to numeric values for comparison
    const roleValues = {
      'Sales': 1,
      'Processor': 2,
      'Underwriter': 3,
      'Closer': 4,
      'Manager': 5
    };
    
    // Get numeric values for the current and required roles
    const currentRoleValue = roleValues[currentRole as keyof typeof roleValues] || 0;
    const requiredRoleValue = roleValues[requiredRole as keyof typeof roleValues] || 0;
    
    // Manager has access to everything
    if (currentRole === 'Manager') {
      return true;
    }
    
    // Check if the current role has enough permission
    return currentRoleValue >= requiredRoleValue;
  }

  /**
   * Handle Http operation that failed.
   * Let the app continue.
   * @param operation - name of the operation that failed
   * @param result - optional value to return as the observable result
   */
  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
      console.error(`${operation} failed: ${error.message}`);
      
      // Let the app keep running by returning an empty result
      return of(result as T);
    };
  }
}