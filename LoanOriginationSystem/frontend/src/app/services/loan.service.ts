import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';

export interface Loan {
  _id?: string;
  borrowerInfo?: {
    firstName: string;
    lastName: string;
    email: string;
    phone: string;
    dob: string;
    ssn: string;
    address: {
      street: string;
      city: string;
      state: string;
      zipCode: string;
    };
    creditScore: number;
  };
  milestone: string;
  createdAt?: string;
  updatedAt?: string;
}

@Injectable({
  providedIn: 'root'
})
export class LoanService {
  private apiUrl = 'http://localhost:8000/api/loans';

  constructor(private http: HttpClient) { }

  getLoans(): Observable<Loan[]> {
    return this.http.get<Loan[]>(this.apiUrl)
      .pipe(
        catchError(this.handleError<Loan[]>('getLoans', []))
      );
  }

  getLoan(id: string): Observable<Loan> {
    const url = `${this.apiUrl}/${id}`;
    return this.http.get<Loan>(url)
      .pipe(
        catchError(this.handleError<Loan>(`getLoan id=${id}`))
      );
  }

  createLoan(borrowerInfo: any): Observable<Loan> {
    return this.http.post<Loan>(this.apiUrl, { borrowerInfo })
      .pipe(
        tap((newLoan: Loan) => console.log(`Created loan w/ id=${newLoan._id}`)),
        catchError(this.handleError<Loan>('createLoan'))
      );
  }

  updateMilestone(id: string, milestone: string): Observable<any> {
    const url = `${this.apiUrl}/${id}/milestone`;
    return this.http.put(url, { milestone })
      .pipe(
        catchError(this.handleError<any>('updateMilestone'))
      );
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