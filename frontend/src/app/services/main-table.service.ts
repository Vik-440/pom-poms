import { Inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
@Injectable({
  providedIn: 'root'
})
export class MainPage {

  url = `${this.apiUrl}/main_page`;

  constructor(private http: HttpClient, @Inject('API_URL') private apiUrl: string) {
  }

  getListMain() {
    return this.http.get(`http://127.0.0.1:5000/main_page`);
  }
}
