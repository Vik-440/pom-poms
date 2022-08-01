import { HttpClient } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
@Injectable({
  providedIn: 'root'
})
export class FinancesPageService {

  url = `http://127.0.0.1:5000/finance`;

  constructor(private http: HttpClient, @Inject('API_URL') private apiUrl: string) {
  }

  getFinances() {
    return this.http.get(`http://127.0.0.1:5000/finance`);
  }

  getFilters(params) {
    return this.http.post(`http://127.0.0.1:5000/finance`, params);
  }

  editPayment(params) {
    return this.http.post(`http://127.0.0.1:5000/finance`, params);
  }

  savePayment(params) {
    return this.http.post(`http://127.0.0.1:5000/finance/payment`, params);
  }
}
