import { Inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
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

}
