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
    const params = {status: 'pending'}
    this.http.post(' https://gorest.co.in/public/v2/todos',  params)
    .subscribe(data => {
      console.log(data)
    })
    return this.http.get(`http://127.0.0.1:5000/main_page`);
  }

  getListWithFilters(params) {
    return this.http.post(`http://127.0.0.1:5000/main_page`, params);
  }

  makeDoneOrder(params) {
    return this.http.post(`http://127.0.0.1:5000/main_page`, params);
  }
}
