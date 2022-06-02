import { HttpClient } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
@Injectable({
  providedIn: 'root'
})
export class CreateOrderService {

  url = `${this.apiUrl}/main_page`;

  constructor(private http: HttpClient, @Inject('API_URL') private apiUrl: string) {
  }

  getListMaterial() {
    return this.http.get(`http://127.0.0.1:5000/new_order`);
  }

  getInfoForOrder(params) {
    return this.http.post(`http://127.0.0.1:5000/new_order`, params);
  }

  saveOrder(params) {
    return this.http.post(`http://127.0.0.1:5000/new_order`, params);
  }
}
