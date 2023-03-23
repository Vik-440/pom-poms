import { HttpClient } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
@Injectable({
    providedIn: 'root',
})
export class CreateOrderService {
    url = `${this.apiUrl}/main_page`;

    constructor(private http: HttpClient, @Inject('API_URL') private apiUrl: string) {}

    getListMaterial() {
        return this.http.get(`http://127.0.0.1:5000/new_order`);
    }

    getInfoForOrder(params) {
        return this.http.post(`http://127.0.0.1:5000/new_order`, params);
    }

    saveClient(params) {
        return this.http.post('http://127.0.0.1:5000/create_client/', params)
    }

    editClient(params, id) {
        return this.http.put(`http://127.0.0.1:5000/edit_client/${id}`, params)
    }

    saveOrder(params) {
        return this.http.post(`http://127.0.0.1:5000/new_order`, params);
    }
}
