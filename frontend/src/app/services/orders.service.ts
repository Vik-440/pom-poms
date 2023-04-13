import { HttpClient } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
@Injectable({
    providedIn: 'root',
})
export class CreateOrderService {
    url = `${this.apiUrl}/order`;

    constructor(private http: HttpClient, @Inject('API_URL') private apiUrl: string) {}

    getOrder(id) {
        return this.http.get(`${this.url}/${id}`);
    }

    saveOrder(params) {
        return this.http.post(`${this.url}`, params);
    }

    editOrder(params, id) {
        return this.http.put(`${this.url}/${id}`, params);
    }

}
