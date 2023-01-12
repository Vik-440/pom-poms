import { HttpClient } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
@Injectable({
    providedIn: 'root',
})
export class MainPageService {
    url = `${this.apiUrl}/main_page`;

    constructor(private http: HttpClient, @Inject('API_URL') private apiUrl: string) {}

    getListMain() { //залишати
        return this.http.get(`http://127.0.0.1:5000/main_page`);
    }

    getListWithFilters(params) {
        return this.http.post(`http://127.0.0.1:5000/main_page`, params);
    }

    makeDoneOrder(params) {
        return this.http.post(`http://127.0.0.1:5000/main_page`, params);
    }

    changePase(params) {
        return this.http.post(`http://127.0.0.1:5000/main_page`, params);
    }

    sendPhase(id, params) {
        return this.http.put(`http://127.0.0.1:5000/main_page/phase/${id}`, params);
    }
}
