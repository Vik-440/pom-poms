import { HttpClient } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
@Injectable({
  providedIn: 'root',
})
export class UsefulService {
  url = `${this.apiUrl}`;

  constructor(private http: HttpClient, @Inject('API_URL') private apiUrl: string) {}

  getAutofill(params) {
    return this.http.get(`${this.url}/autofill`, { params });
  }
}
