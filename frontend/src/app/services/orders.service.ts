import { HttpClient } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
@Injectable({
    providedIn: 'root',
})
export class CreateOrderService {
    url = `${this._apiUrl}/order`;

    constructor(private _http: HttpClient, @Inject('API_URL') private _apiUrl: string) {}

    getOrder(id) {
        return this._http.get(`${this.url}/${id}`);
    }

    saveOrder(params) {
        return this._http.post(`${this.url}`, params);
    }

    editOrder(params, id) {
        return this._http.put(`${this.url}/${id}`, params);
    }

}
