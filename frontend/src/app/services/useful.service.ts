import { HttpClient } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
@Injectable({
    providedIn: 'root',
})
export class UsefulService {
    url = `http://127.0.0.1:5000/order`;

    constructor(private http: HttpClient, @Inject('API_URL') private apiUrl: string) {}

    getAutofill(params) {
        return this.http.get('http://127.0.0.1:5000/autofill', {params});
    }
}
