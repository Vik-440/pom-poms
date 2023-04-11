import { HttpClient } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
@Injectable({
    providedIn: 'root',
})
export class ProductsService {
    url = `http://127.0.0.1:5000/product`;

    constructor(private http: HttpClient, @Inject('API_URL') private apiUrl: string) {}

    getProduct(id) {
      return this.http.get(`${this.url}/${id}`);
    }

    saveProduct(params) {
      return this.http.post(`${this.url}`, params);
    }

    editProduct(id, params) {
      return this.http.put(`${this.url}/${id}`, params);
    }
}
