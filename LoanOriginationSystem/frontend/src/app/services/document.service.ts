import { Injectable } from '@angular/core';
import { HttpClient, HttpEvent, HttpRequest } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError } from 'rxjs/operators';

export interface Document {
  _id?: string;
  loanId: string;
  documentType: string;
  filename: string;
  originalFilename: string;
  fileSize: number;
  mimeType: string;
  uploadDate?: string;
  uploadedBy?: string;
  contentExtracted?: boolean;
  complianceScore?: number;
  extractedContent?: string;
}

@Injectable({
  providedIn: 'root'
})
export class DocumentService {
  private apiUrl = 'http://localhost:8000/api/documents';

  constructor(private http: HttpClient) { }

  uploadDocument(loanId: string, documentType: string, file: File): Observable<HttpEvent<any>> {
    const formData: FormData = new FormData();
    formData.append('file', file);
    formData.append('loanId', loanId);
    formData.append('documentType', documentType);

    const req = new HttpRequest('POST', this.apiUrl, formData, {
      reportProgress: true,
      responseType: 'json'
    });

    return this.http.request(req);
  }

  getDocumentsByLoanId(loanId: string): Observable<Document[]> {
    return this.http.get<Document[]>(`${this.apiUrl}/loan/${loanId}`)
      .pipe(
        catchError(this.handleError<Document[]>('getDocumentsByLoanId', []))
      );
  }

  getDocument(id: string): Observable<Document> {
    return this.http.get<Document>(`${this.apiUrl}/${id}`)
      .pipe(
        catchError(this.handleError<Document>('getDocument'))
      );
  }

  downloadDocument(id: string): Observable<Blob> {
    return this.http.get(`${this.apiUrl}/${id}/download`, { responseType: 'blob' })
      .pipe(
        catchError(this.handleError<Blob>('downloadDocument'))
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