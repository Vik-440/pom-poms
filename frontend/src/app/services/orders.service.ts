import { HttpClient } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
@Injectable({
    providedIn: 'root',
})
export class CreateOrderService {
    url = `http://127.0.0.1:5000/order`;

    constructor(private http: HttpClient, @Inject('API_URL') private apiUrl: string) {}

    getOrder(id) {
        return this.http.get(`${this.url}/${id}`);
    }

    getInfoForOrder(params) {
        return this.http.post('http://127.0.0.1:5000/new_order', params);
    }

    saveOrder(params) {
        return this.http.post(`${this.url}/`, params);
    }

}
