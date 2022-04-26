import { Inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
@Injectable({
  providedIn: 'root'
})
export class MainPage {

  url = `${this.apiUrl}/mainpage`;

  constructor(private http: HttpClient, @Inject('API_URL') private apiUrl: string) {
  }

  getList() {
    console.log(this.apiUrl)
    return this.http.get(`http://172.17.0.3:5000/mainpage`);
  }
}