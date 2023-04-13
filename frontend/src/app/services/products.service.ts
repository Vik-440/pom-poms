import { HttpClient } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
@Injectable({
    providedIn: 'root',
})
export class ProductsService {
    url = `${this._apiUrl}/product`;

    constructor(private _http: HttpClient, @Inject('API_URL') private _apiUrl: string) {}

    getProduct(id) {
      return this._http.get(`${this.url}/${id}`);
    }

    saveProduct(params) {
      return this._http.post(`${this.url}`, params);
    }

    editProduct(id, params) {
      return this._http.put(`${this.url}/${id}`, params);
    }
}
